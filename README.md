# BeehaviourLab

This project is for the BeehaviourLab, a raspberry pi-based behavioural arena for recording the behaviour of insects using video and sound. Project is written for a Raspberry Pi Model 4B.

# components
1. Raspberry Pi Model 4B 4 GB
2. Raspberry Pi Camera Module V2 NoIR
2. DHT22 / AM2302 temperature and humidity probe
3. White LED panel (optional)
4. Red LED panel
5. Røde SmartLav+ microphone
6. 0.96" OLED display (I2C)
7. Time clapper: buzzer & single LEDs

# programme
Program is intended to run for 24 hours (can be adjusted on config.json) using GPIO pins as set out on config.json. Camera and microphone record continuously. Measurements are taken from the DHT22 every 30 seconds. White LEDs are on for the first 12 hours, and red LEDs for the subsequent 12 hours (time is adjustable). OLED displays the temp, humidity, and elapsed recording time. Data from DHT22 is saved on a .csv file alongside elapsed time. Audio is saved as a .wav file. 

Metadata is saved alongside recordings containing information from config.json file

Written and designed by Rachel Parkinson.

# aparatus
Template files for laser cutting the aparatus stand and cages. Stand is laser cut from 5 mm perspex, and boxes may be cut from either 3 mm or 3 mm clear perspex. Template files designed and created by Rachel Parkinson and Jennifer Scott.
