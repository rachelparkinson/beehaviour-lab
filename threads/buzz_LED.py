import RPi.GPIO as GPIO
import time
import json

def led_buzzer_control(duration, BUZZER_PIN, LED_PIN, buzz_length, buzz_space, buzz_file):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.IN)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)
    
    timestamps = []  # list to store timestamps
    
    time.sleep(5) #wait for 5s from recording start time before buzzer goes
    
    current_timestamp = time.time()
    timestamps.append(current_timestamp)
    
    # Start the PWM for the buzzer with a duty cycle of 30%
    # Setup PWM for buzzer. Let's start with a frequency of 2kHz (2000 Hz)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    pwm = GPIO.PWM(BUZZER_PIN, 440)
    pwm.start(30)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    
    GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Turn Buzzer on
    GPIO.output(LED_PIN, GPIO.HIGH) # Turn LED on
    time.sleep(buzz_length)
    
    # Stop the PWM and turn off the buzzer
    pwm.stop()
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.setup(BUZZER_PIN, GPIO.IN) #set buzzer pin to IN
    
    current_timestamp = time.time()
    timestamps.append(current_timestamp)

    # Save timestamps to a JSON file
    with open(buzz_file, 'w') as json_file:
        json.dump(timestamps, json_file)

