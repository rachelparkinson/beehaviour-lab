
import time
from datetime import date
import threading
import queue
from control/LED_panels.py import lights
from control/OLED_display.py import OLED
from sensors/temp_rh.py import DHT
from sensors/MEMs.py import MEMs
from sensors/pi_cam.py import cam

# main file for the rPi beehaviour box. 
# Setup duration of recordings directly from this file.

if __name__ == "__main__":
    #get date and start time
    day = today.strftime("%y%m%d")
    start_time = time.time()
    
    # Set up pins and timing for components
    
    #Total recording time (24 hours = 86400s)
    Rec_time = 24 * 60 * 60

    #LED panels
    R_LED_PIN = 20
    W_LED_PIN = 21
    LED_hrs = 12
    LED_time = LED_hrs * 3600
    
    #DHT pin
    DHT_PIN = 23
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
    lights_thread = threading.Thread(target=lights, args=(R_LED_PIN, W_LED_PIN, LED_time, start_time,))
    DHT_thread = threading.Thread(target=DHT, args=(DHT_PIN, DHT_file, data_queue, start_time,))
    OLED_thread = threading.Thread(target=OLED, args=(data_queue, start_time, i2c,))
    MEMs_thread = threading.Thread(target=MEMs, args=(data_queue, i2c, audio_file, duration, start_time,))
    cam_thread = threading.Thread(target=cam, args=(framerate, resolution, video_file, duration, start_time, ))
   
    #Start threads
    lights_thread.start()
    DHT_thread.start()
    OLED_thread.start()
    MEMs_thread.start()
    cam_thread.start()
    
    # Wait for Rec_time (e.g., 24 hours)
    time.sleep(Rec_time + 60)
    
    # Stop threads
    stop_event.set()
    
    #Wait for all threads to complete
    lights_thread.join()
    DHT_thread.join()
    OLED_thread.join()
    MEMs_thread.join()
    cam_thread.join()
    
    print("All tasks completed")

#clean up pins
GPIO.cleanup()

