
import time
import threading
import queue
import busio
import board

from LED_panels import lights
from OLED_display import OLED
from temp_rh import DHT
from MEMs import MEMs
from pi_cam import cam

# main file for the rPi beehaviour box. 
# Setup duration of recordings directly from this file.

if __name__ == "__main__":
    #get date and start time
    current_time = time.localtime()
    day = time.strftime("%y%m%d", current_time)
    start_time = time.time()
    
    # Set up pins and timing for components
    
    #Total recording time (24 hours = 86400s)
    #Rec_time = 24 * 60 * 60
    Rec_time = 60 #one minute tester
    
    #LED panels
    R_LED_PIN = 20
    W_LED_PIN = 21
    LED_hrs = 12
    LED_time = LED_hrs * 3600
    
    LED_time = 5 #test at 30s per LED colour
    
    #DHT pin board.D23
    #DHT_PIN = 'D23'
    DHT_file = day + '_DHT.txt'
    
    #OLED display & MEMs
    i2c = busio.I2C(board.SCL, board.SDA)
    duration = Rec_time
    audio_file = day + '_audio.wav'
    
    #pi cam
    resolution = (1280, 720)
    framerate = 30
    video_file = day + '_video.h264'
    
    #create thread-safe queue
    data_queue = queue.Queue()
    
    #Create threads for each task, pass relevant parameters
    lights_thread = threading.Thread(target=lights, args=(R_LED_PIN, W_LED_PIN, LED_time, start_time, Rec_time))
    DHT_thread = threading.Thread(target=DHT, args=(DHT_file, data_queue, Rec_time, start_time))
    OLED_thread = threading.Thread(target=OLED, args=(data_queue, Rec_time, start_time, i2c))
    #MEMs_thread = threading.Thread(target=MEMs, args=(data_queue, i2c, audio_file, duration, start_time))
    #cam_thread = threading.Thread(target=cam, args=(framerate, resolution, video_file, duration, start_time))
   
    #Start threads
    lights_thread.start()
    DHT_thread.start()
    OLED_thread.start()
    #MEMs_thread.start()
    #cam_thread.start()
    
    # Wait for Rec_time (e.g., 24 hours), plus 15s buffer
    time.sleep(Rec_time + 15)
    
    #Wait for all threads to complete
    lights_thread.join()
    DHT_thread.join()
    OLED_thread.join()
    #MEMs_thread.join()
    #cam_thread.join()
    
    print("All tasks completed")

#clean up pins
#GPIO.cleanup()