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
import json
from picamera2 import Picamera2, Preview

from load_config import load_config
from mic_search import find_usb_mic

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
    
    # Load the configuration for this Raspberry Pi
    config = load_config()
    
    ####################
    ## METADATA INPUT ##
    ####################
    day = "240202" # Date (YEARMONTHDAY e.g., 240131)
    Rec_time = 300 #recording segment time (s)
    reps = 48 #how many recordings in loop
    spaces = 1500 #space between end of one recording and beginning of next (s)
    
    ################################################################
    ## don't change this:
    Name = config["Name"]
    rPi_num = config["rPi_num"]
    start_time = time.time() #get start time
    ssd_path = config["ssd_path"] # Name folder on SSD to save files
    #################################################################
    

    
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
    
    if not os.path.exists(os.path.join(ssd_path, day)):
        os.makedirs(os.path.join(ssd_path, day))
        
    
    # Check USB mic card & device
    card, device = find_usb_mic()
    print(f"Found USB microphone on card {card}, device {device}")
    
    ###############################
    ## Loop to repeat threads ##
    ############################
    
    for replicate in range(1, reps + 1):
        
        seg_time = time.time()
        
        day_folder = create_incremental_subfolder(os.path.join(ssd_path, day))
        
        # Define metadata for .json file
         metadata = {
            "treatment": config["treatment"],
            "concentration": config["concentration"],
            "unit": config["unit"],
            "species": config["species"],
            "group": config["group"],
            "experimenter": config["experimenter"],
            "day": config["day"],
            "segment length": Rec_time,
            "number segments": reps,
            "time between segments": spaces,
            "rPi_name": Name,
            "rPi start time": start_time,
            "current segment start time": seg_time,
            "current segment number": replicate,
            "Additional description": config["Additional description"]
        }
    
        metadata_name = os.path.join(day_folder, Name + 'metadata.json')
    
        with open(metadata_name, 'w') as file:
            json.dump(metadata, file, indent=4)
        
        GPIO.cleanup()
    
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
        buzz_file = os.path.join(day_folder, day + '_' + Name + '_buzz.json')
        DHT_file = os.path.join(day_folder, day + '_' + Name + '_DHT.json')
        audio_file = os.path.join(day_folder, day + '_' + Name + '_audio.wav')
        video_file = os.path.join(day_folder, day + '_' + Name + '_video.h264')

        #Initialize camera:
        picam2 = Picamera2()
        
        #Create threads for each task, pass relevant parameters
        lights_thread = threading.Thread(target=lights, args=(R_LED_PIN, W_LED_PIN, Rec_time))
        DHT_thread = threading.Thread(target=DHT, args=(DHT_file, data_queue, start_time, seg_time, Rec_time))
        USB_mic_thread = threading.Thread(target=record_audio, args=(duration, audio_file, card, device))
        cam_thread = threading.Thread(target=cam, args=(picam2, framerate, resolution, video_file, duration, start_time))
        time_clapper_thread = threading.Thread(target=time_clapper, args=(rPi_num, BUZZER_PIN, LED_PIN, Rec_time, buzz_file))
        
        #Start threads
        lights_thread.start()
        DHT_thread.start()
        cam_thread.start()
        USB_mic_thread.start()
        time_clapper_thread.start()
        
        # Wait for Rec_time
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
            else
                time.sleep(1)

#clean up pins
GPIO.cleanup()