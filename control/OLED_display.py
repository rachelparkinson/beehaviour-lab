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

# Initialize I2C communication for the OLED display
i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

def display(data_queue):
    while True: 
        try:
            elapsed_time, temperature, humidity = data_queue.get()
            
            #display data on OLED panel
            display.fill(0)
            display.text(f"{temperature:.1f} C, "{humidity:.1f}% rh, 0, 0, 1)
            display.text(f"{str(elapsed_time)}", 0, 24, 1)
            display.show()
            
        except RuntimeError as e:
            # If there's an error reading data, print the error message
            print(f"Error reading data from DHT sensor: {e}")

    # Wait for 10 seconds before reading data and updating the display again
    time.sleep(10)

    except KeyboardInterrupt:
        print("OLED stopped by user")
        break