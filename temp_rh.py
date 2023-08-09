import time
#first time, pip install adafruit-circuitpython-dht
import adafruit_dht
import board
import csv
import datetime


def DHT(DHT_file, data_queue, start_time, Rec_time):
    #Initialize DHT22 sensor
    dht_sensor = adafruit_dht.DHT22(board.D23, use_pulseio=False) 
    last_temp = None
    last_rh = None
    
    while time.time() - start_time < Rec_time:
        try:
            #Read temp and humidity from sensor
            temp = dht_sensor.temperature
            rh = dht_sensor.humidity
            if temp is not None and rh is not None:
                last_temp = temp
                last_rh = rh
                
                print(f"Temp: {temp:.1f} °C, Humidity: {rh:.1f}%")
            
                elapsed_time = time.time() - start_time #calculate elapsed time
                timex = datetime.datetime.fromtimestamp(elapsed_time)
                formatted_time = timex.strftime('%H:%M:%S')
                #put data into the queue
                data_queue.put((temp, rh))
            
                with open(DHT_file, 'a') as file:
                    writer = csv.writer(file)
                    writer.writerow([formatted_time, temp, rh])
                    
            else:
                print("Failed to retrieve data from sensor.")
                
        except Exception as e:
            print("An error occurred:", str(e))
            
            #Print values to console
            #print(f"Temp: {temp:.1f} °C, Humidity: {rh:.1f}%") 

        #except RuntimeError as e:
        #    print(f"Error reading data from DHT sensor: {e}")

        # Wait for 2 seconds before reading data again
        time.sleep(2)
