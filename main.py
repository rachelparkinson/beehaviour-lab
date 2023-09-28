import time
import threading
import queue
import busio
import board
import RPi.GPIO as GPIO
import os

from LED_panels import lights
from OLED_display import OLED
from temp_rh import DHT
from MEMs import MEMs
from pi_cam import cam
from buzz_LED import led_buzzer_control
from button_wait import wait_for_button

# main file for the rPi beehaviour box. 
# Setup duration of recordings directly from this file.

if __name__ == "__main__":
    
    #get date and start time
    current_time = time.localtime()
    day = time.strftime("%y%m%d", current_time)
    start_time = time.time()
    
    # Name folder on SSD to save files
    ssd_path = '/home/rPi1/myssd/'
    day_folder = os.path.join(ssd_path, day)
    
    #Check if folder exists. If not, create it.
    if not os.path.exists(day_folder):
        os.makedirs(day_folder)
        
    # Set up pins and timing for components
    
    #Total recording time (24 hours = 86400s)
    #Rec_time = 24 * 60 * 60
    Rec_time = 60 #one minute tester
    
    # Push button pin
    BUTTON_PIN = 5 #GPIO5
    
    #LED panels
    R_LED_PIN = 20
    W_LED_PIN = 21
    LED_hrs = 12
    LED_time = LED_hrs * 3600
    
    LED_time = 5 #test at 30s per LED colour
    
    # LED and Buzzer
    LED_BUZZER_PIN = 24
    buzz_length = 1 # duration of buzz
    buzz_space = 5 # time to wait until next buzz
    buzz_file = os.path.join(day_folder, day + '_buzz.json')
    
    #DHT pin board.D23
    #DHT_PIN = 'D23'
    DHT_file = os.path.join(day_folder, day + '_DHT.json')
    
    #OLED display & MEMs
    i2c = busio.I2C(board.SCL, board.SDA)
    duration = Rec_time
    audio_file = os.path.join(day_folder, day + '_audio.wav')
    
    #pi cam
    resolution = (1280, 720)
    framerate = 30
    video_file = os.path.join(day_folder, day + '_video.h264')
    
    #create thread-safe queue
    data_queue = queue.Queue()
    
    #Use button to initialize programme:
    wait_for_button(BUTTON_PIN)
    
    #Create threads for each task, pass relevant parameters
    lights_thread = threading.Thread(target=lights, args=(R_LED_PIN, W_LED_PIN, LED_time, start_time, Rec_time))
    DHT_thread = threading.Thread(target=DHT, args=(DHT_file, data_queue, Rec_time, start_time))
    OLED_thread = threading.Thread(target=OLED, args=(data_queue, Rec_time, start_time, i2c))
    MEMs_thread = threading.Thread(target=MEMs, args=(data_queue, i2c, audio_file, duration, start_time))
    cam_thread = threading.Thread(target=cam, args=(framerate, resolution, video_file, duration, start_time))
    led_buzzer_thread = threading.Thread(target=led_buzzer_control, args=(duration, LED_BUZZER_PIN, buzz_length, buzz_space, buzz_file))
    
    #Start threads
    lights_thread.start()
    DHT_thread.start()
    OLED_thread.start()
    MEMs_thread.start()
    cam_thread.start()
    led_buzzer_thread.start()
    
    # Wait for Rec_time (e.g., 24 hours), plus 15s buffer
    time.sleep(Rec_time + 15)
    
    #Wait for all threads to complete
    lights_thread.join()
    DHT_thread.join()
    OLED_thread.join()
    MEMs_thread.join()
    cam_thread.join()
    led_buzzer_thread.join()
    
    print("All tasks completed")

#clean up pins
GPIO.cleanup()