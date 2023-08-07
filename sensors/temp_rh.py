import RPi.GPIO as GPIO

#pre-clean
GPIO.cleanup()

import RPi.GPIO as GPIO
import time
#first time, pip install adafruit-circuitpython-dht
import adafruit_dht
import board



DHT_PIN = 23

#Initialize DHT22 sensor
dht_sensor = adafruit_dht.DHT22(board.D23, use_pulseio=False) 
#dht_sensor = adafruit_dht.DHT22(DHT_PIN)

while True:
    try:
        #Read temp and humidity from sensor
        temp = dht_sensor.temperature
        rh = dht_sensor.humidity
        
        #Print values to console
        print(f"Temp: {temp:.1f} °C, Humidity: {rh:.1f}%")
    
    except RuntimeError as e:
        #if there's an error reading data, print error message
        print(f"Error reading data from DHT sensor: {e}")

    # Wait for 10 seconds before reading data again
    time.sleep(10)

# Clean uip
GPIO.cleanup()
dht_sensor.exit()
display.fill(0)
display.show()
