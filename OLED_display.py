# need to pip install adafruit-circuitpython-ssd1306
# and sudo apt-get install python3-smbus

import RPi.GPIO as GPIO
import time
import datetime
import adafruit_ssd1306
import busio
import board
import queue

def OLED(data_queue, Rec_time, start_time, i2c):
    
    # Set the GPIO mode to BCM (Broadcom SOC channel numbering)
    GPIO.setmode(GPIO.BCM)

    # Initialize I2C communication for the OLED display
    display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
    
    display.fill(0)
    display.show()
    
    while time.time() - start_time < Rec_time: 
        try:
            temp, rh = data_queue.get()
            #elapsed_time = time.time() - start_time #calculate elapsed time
            elapsed_time_s = time.time() - start_time
            elapsed_time = datetime.timedelta(seconds=elapsed_time_s)
            hours, remainder = divmod(elapsed_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            elapsed_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            #display data on OLED panel
            display.fill(0)
            display.text(f"{temp:.1f} C, {rh:.1f}% rh", 0, 0, 1)
            display.text(f"REC time: {elapsed_time_str}", 0, 24, 1)
            display.show()
            
        except KeyboardInterrupt:
            break

        # Wait for 10 seconds before reading data and updating the display again
        time.sleep(2)
    
    while time.time() - start_time > Rec_time:
        try:
            # Display "recording finished!" and total Rec_time
            display.fill(0)
            display.text("Done!", 0, 0, 1)
            display.text(f"Rec time: {elapsed_time_str}", 0, 24, 1)
            display.show()
            
        except KeyboardInterrupt:
            break
        