# Wait for button function to initiate recordings

import RPi.GPIO as GPIO
import time

def wait_for_button(BUTTON_PIN):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN)
    
    print("waiting for button to initiate...")
    GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)
    print("Button pressed! Starting tasks...")
