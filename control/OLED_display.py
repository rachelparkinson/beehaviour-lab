# need to pip install adafruit-circuitpython-ssd1306
# and sudo apt-get install python3-smbus

import board
import busio
import adafruit_ssd1306
import RPi.GPIO as GPIO
import time
import adafruit_dht
import queue

# Set the GPIO mode to BCM (Broadcom SOC channel numbering)
GPIO.setmode(GPIO.BCM)

def OLED(data_queue, start_time, i2c):
    
    # Initialize I2C communication for the OLED display
    display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
    
    while True: 
        try:
            temp, rh = data_queue.get()
            elapsed_time = time.time() - start_time #calculate elapsed time
            
            #display data on OLED panel
            display.fill(0)
            display.text(f"{temp:.1f} C, "{rh:.1f}% rh, 0, 0, 1)
            display.text(f"REC time: {str(elapsed_time)}", 0, 24, 1)
            display.show()
            
        except KeyboardInterrupt:
            break
        
        except RuntimeError as e:
            # If there's an error reading data, print the error message
            print(f"Error reading data from DHT sensor: {e}")

        # Wait for 10 seconds before reading data and updating the display again
        time.sleep(10)