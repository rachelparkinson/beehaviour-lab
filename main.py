
import time
import threading
from LED_panels.py import lights



# main file for the rPi beehaviour box. 
# Setup duration of recordings directly from this file.

if __name__ == "__main__":
    # Set up pins and timing for components

    #LED panels
    R_LED_PIN = 20
    W_LED_PIN = 21
    LED_hrs = 12
    LED_time = LED_hrs * 3600
    
    #Create threads for each task, pass relevant parameters
    lights_thread = threading.Thread(target=lights, args=(R_LED_PIN, W_LED_PIN, LED_time,))
    
    #Start threads
    lights_thread.start()
    
    #Wait for all threads to complete
    lights_thread.join()
    
    print("All tasks completed")




