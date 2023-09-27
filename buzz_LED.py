# Buzzer and LED light
# Purpose: to synchronize video and audio recordings.

import RPi.GPIO as GPIO
import time
import threading
import json

def led_buzzer_control(duration, LED_BUZZER_PIN, buzz_length, buzz_space, buzz_file):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_BUZZER_PIN, GPIO.OUT)

    GPIO.output(LED_BUZZER_PIN, GPIO.LOW)

    timestamps = [] # list to store timestamps

    end_time = time.time() + duration
    while time.time() < end_time:
        current_timestamp = time.time()
        timestamps.append(current_timestamp)

        GPIO.output(LED_BUZZER_PIN, GPIO.HIGH) #turn on
        time.sleep(buzz_length) #on for "buzz_length" time
        GPIO.output(LED_BUZZER_PIN, GPIO.LOW) # turn off

        current_timestamp = time.time()
        timestamps.append(current_timestamp)

        time.sleep(buzz_space-buzz_length) # space between buzzes

    # save timestamps to a JSON file
    with open(buzz_file, 'w') as json_file:
        json.dump(timestamps, json_file)

    GPIO.cleanup()
