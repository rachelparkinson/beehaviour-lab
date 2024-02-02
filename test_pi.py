import time
import threading
import queue
import busio
import board
import RPi.GPIO as GPIO
import os
import subprocess
import signal
import sys
import adafruit_ssd1306
from picamera2 import Picamera2, Preview

from threads.LED_panels import lights
from threads.OLED_display import OLED, OLED_wipe
from threads.temp_rh import DHT
from threads.pi_cam import cam
from threads.buzz_LED import led_buzzer_control
from threads.USB_mic import record_audio
from threads.time_clapper import time_clapper

# main file for the rPi beehaviour box. 
# Setup duration of recordings directly from this file.

if __name__ == "__main__":
        
    #Set Name
    Name = "rPi2"
    
    #Set rPi number:
    rPi_num = 2
    
    #get date and start time
    current_time = time.localtime()
    day = time.strftime("%y%m%d", current_time)
    start_time = time.time()
    
    # Name folder on SSD to save files
    ssd_path = '/home/rPi2/myssd/'
    #day_folder = os.path.join(ssd_path, day)
    
    def create_incremental_subfolder(base_folder):
        subfolders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
        
        if not subfolders:
            new_subfolder = "001"
        else:
            last_subfolder = max(subfolders, key=lambda x: int(x))
            new_subfolder = f"{int(last_subfolder) + 1:03d}"
        
        subfolder_path = os.path.join(base_folder, new_subfolder)
        os.makedirs(subfolder_path)
        return subfolder_path
    
    if not os.path.exists(os.path.join(ssd_path, "test")):
        os.makedirs(os.path.join(ssd_path, "test"))
    
    ############################################
        ## Set up PINS ##

    #Total recording time (24 hours = 86400s)
    #Rec_time = 24 * 60 * 60
    Rec_time = 5 #recording segment time (s)
    
    
    ###############################
        ## Loop to repeat threads ##
        ############################
    reps = 2
    spaces = 3
    
    
    for replicate in range(1, reps + 1):
        
        seg_time = time.time()
        
        GPIO.cleanup()
    
        day_folder = create_incremental_subfolder(os.path.join(ssd_path, "test"))
        #LED panels
        R_LED_PIN = 16
        W_LED_PIN = 21
        
        # LED and Buzzer
        BUZZER_PIN = 24
        LED_PIN = 25
        
        #OLED display & MEMs
        i2c = busio.I2C(board.SCL, board.SDA)
        duration = Rec_time
        
        #pi cam
        resolution = (1920, 1080) #max res with high framerate
        framerate = 60 # comes out at ~47.9 fps
        
        #create thread-safe queue
        data_queue = queue.Queue()
        
       #Wipe the OLED screen
        GPIO.setmode(GPIO.BCM)
        display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
        display.fill(0)
        
        OLED_wipe(Name, data_queue, i2c) 
        # Filenames (as per day_folder)
        buzz_file = os.path.join(day_folder, day + Name + '_buzz.json')
        DHT_file = os.path.join(day_folder, day + Name + '_DHT.json')
        audio_file = os.path.join(day_folder, day + Name + '_audio.wav')
        video_file = os.path.join(day_folder, day + Name + '_video.h264')

        #Initialize camera:
        picam2 = Picamera2()
        
        #Wipe the OLED screen
        GPIO.setmode(GPIO.BCM)
        display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
        display.fill(0)
        
        OLED_wipe(Name, data_queue, i2c)
        
        
        #Create threads for each task, pass relevant parameters
        lights_thread = threading.Thread(target=lights, args=(R_LED_PIN, W_LED_PIN, Rec_time))
        DHT_thread = threading.Thread(target=DHT, args=(DHT_file, data_queue, start_time, seg_time, Rec_time))
        #OLED_thread = threading.Thread(target=OLED, args=(Name, data_queue, Rec_time, start_time, i2c))
        USB_mic_thread = threading.Thread(target=record_audio, args=(duration, audio_file))
        cam_thread = threading.Thread(target=cam, args=(picam2, framerate, resolution, video_file, duration, start_time))
        time_clapper_thread = threading.Thread(target=time_clapper, args=(rPi_num, BUZZER_PIN, LED_PIN, Rec_time, buzz_file))
        
        #Start threads
        lights_thread.start()
        DHT_thread.start()
        #OLED_thread.start()
        cam_thread.start()
        #led_buzzer_thread.start()
        USB_mic_thread.start()
        time_clapper_thread.start()
        
        # Wait for Rec_time (e.g., 24 hours), plus 15s buffer
        time.sleep(Rec_time) 
        
        #start a timer
        time1 = time.time()
        
        # join threads
        print("Joining threads...")
        
        #Wait for all threads to complete
        lights_thread.join()
        DHT_thread.join()
        cam_thread.join()
        USB_mic_thread.join()
        time_clapper_thread.join()

        #Check to be sure camera is closed
        picam2.close()
        
        print("All tasks completed")
        
        time2 = time.time()
        runover_time = time2-time1
        print("Elapsed processing time: ", runover_time)
        
        if replicate < reps:
            # Check to see whether there is any time left on counter:
            if runover_time < spaces:
                time.sleep(spaces - runover_time)
            else:
                time.sleep(1)

#clean up pins
GPIO.cleanup()

