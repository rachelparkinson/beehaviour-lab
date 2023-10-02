import RPi.GPIO as GPIO
import time
import json

def led_buzzer_control(duration, BUZZER_PIN, LED_PIN, buzz_length, buzz_space, buzz_file):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.output(LED_PIN, GPIO.LOW)

    # Setup PWM for buzzer. Let's start with a frequency of 2kHz (2000 Hz)
    pwm = GPIO.PWM(BUZZER_PIN, 440)
    timestamps = []  # list to store timestamps

    end_time = time.time() + duration
    while time.time() < end_time:
        current_timestamp = time.time()
        timestamps.append(current_timestamp)
        

        # Start the PWM for the buzzer with a duty cycle of 30%
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
        #GPIO.cleanup()
        
        current_timestamp = time.time()
        timestamps.append(current_timestamp)

        time.sleep(buzz_space-buzz_length)  # Space between buzzes

    # Save timestamps to a JSON file
    with open(buzz_file, 'w') as json_file:
        json.dump(timestamps, json_file)
        
    GPIO.cleanup()