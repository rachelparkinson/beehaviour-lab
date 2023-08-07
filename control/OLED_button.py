# need to pip install adafruit-circuitpython-ssd1306
# and sudo apt-get install python3-smbus

import board
import busio
import adafruit_ssd1306
import RPi.GPIO as GPIO
import time
import adafruit_dht

# Set the GPIO mode to BCM (Broadcom SOC channel numbering)
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin number for the DHT22 sensor
DHT_PIN = board.D23  # GPIO23 (you can change this to the desired GPIO pin number)

# Initialize I2C communication for the OLED display
i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Configure DHT22 sensor
#dht_sensor = adafruit_dht.DHT22(DHT_PIN)
dht_sensor = adafruit_dht.DHT22(DHT_PIN, use_pulseio=False) 

counter = 1

try:
    while True:
        try:
            # Read temperature and humidity from the sensor
            temperature = dht_sensor.temperature
            humidity = dht_sensor.humidity

            # Clear the display and show the measurements
            display.fill(0)
            display.text(f"{temperature:.1f} C, {humidity:.1f}% rh", 0, 0, 1)
            #display.text(f"Humidity: {humidity:.1f}%", 0, 12, 1)
            display.text(f"{str(counter)}", 0, 24, 1)
            display.show()
            counter = counter + 1

        except RuntimeError as e:
            # If there's an error reading data, print the error message
            print(f"Error reading data from DHT sensor: {e}")

        # Wait for 10 seconds before reading data and updating the display again
        time.sleep(1)

except KeyboardInterrupt:
    # Clean up the GPIO, DHT sensor, and display on Ctrl+C exit
    GPIO.cleanup()
    dht_sensor.exit()
    display.fill(0)
    display.show()