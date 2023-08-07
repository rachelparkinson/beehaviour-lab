import RPi.GPIO as GPIO
import time
#first time, pip install adafruit-circuitpython-dht
import adafruit_dht
import board

def DHT(DHT_pin, file_name, data_queue):
    #Initialize DHT22 sensor
    dht_sensor = adafruit_dht.DHT22(DHT_PIN, use_pulseio=False) 

    while True:
        try:
            #Read temp and humidity from sensor
            temp = dht_sensor.temperature
            rh = dht_sensor.humidity
            elapsed_time = time.time() - start_time #calculate elapsed time
            
            #put data into the queue
            data_queue.put((elapsed_time, temp, rh))
            
            with open(file_name, 'a') as file:
                writer = csv.writer(file)
                writer.writerow([elapsed_time, temp, rh])
        
            # Wait for 60 seconds before reading data again
            time.sleep(60)
        
        except KeyboardInterrupt:
            break
            
        except RuntimeError as e:
            #if there's an error reading data, print error message
            print(f"Error reading data from DHT sensor: {e}")
            continue