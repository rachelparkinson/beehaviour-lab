import RPi.GPIO as GPIO
import time
from itertools import product
import threading

def time_clapper(rPi_num, BUZZER_PIN, LED_PIN, Rec_time, buzz_file):
    # GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.IN)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)
    
    timestamps = []  # list to store timestamps

    # Function to activate the LED and buzzer
    def activate_components(duration):
        GPIO.output(LED_PIN, GPIO.HIGH)
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

    # Generate permutations
    permutations = list(product([0, 1], repeat=5))

    # Get the specific permutation
    selected_permutation = permutations[rPi_num - 1]
    
    # Wait time before first buzz
    time.sleep(5) 
    
    # Start the PWM for the buzzer with a duty cycle of 30%
    # Setup PWM for buzzer. Let's start with a frequency of 2kHz (2000 Hz)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    pwm = GPIO.PWM(BUZZER_PIN, 440)
    pwm.start(30)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    
    current_timestamp = time.time()
    timestamps.append(current_timestamp)
    
    # Control the LED and buzzer using the selected permutation
    for digit in selected_permutation:
        if digit == 0:
            activate_components(0.25)
        else:
            activate_components(0.5)
        time.sleep(0.25)

    # Stop the PWM and turn off the buzzer
    pwm.stop()
    GPIO.setup(BUZZER_PIN, GPIO.IN) #set buzzer pin to IN
    
    current_timestamp = time.time()
    timestamps.append(current_timestamp)
    
    # Wait time before SECOND buzz (half way through recording)
    time.sleep(Rec_time/2) 
    
    # Start the PWM for the buzzer with a duty cycle of 30%
    # Setup PWM for buzzer. Let's start with a frequency of 2kHz (2000 Hz)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    pwm = GPIO.PWM(BUZZER_PIN, 440)
    pwm.start(30)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    
    current_timestamp = time.time()
    timestamps.append(current_timestamp)
    
    # Control the LED and buzzer using the selected permutation
    for digit in selected_permutation:
        if digit == 0:
            activate_components(0.25)
        else:
            activate_components(0.5)
        time.sleep(0.25)

    # Stop the PWM and turn off the buzzer
    pwm.stop()
    GPIO.setup(BUZZER_PIN, GPIO.IN) #set buzzer pin to IN
    
    current_timestamp = time.time()
    timestamps.append(current_timestamp)
    
    # Wait time before THIRD buzz (10s before end of recording)
    time.sleep(Rec_time/2-15) 
    
    # Start the PWM for the buzzer with a duty cycle of 30%
    # Setup PWM for buzzer. Let's start with a frequency of 2kHz (2000 Hz)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    pwm = GPIO.PWM(BUZZER_PIN, 440)
    pwm.start(30)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    
    current_timestamp = time.time()
    timestamps.append(current_timestamp)
    
    # Control the LED and buzzer using the selected permutation
    for digit in selected_permutation:
        if digit == 0:
            activate_components(0.25)
        else:
            activate_components(0.5)
        time.sleep(0.25)

    # Stop the PWM and turn off the buzzer
    pwm.stop()
    GPIO.setup(BUZZER_PIN, GPIO.IN) #set buzzer pin to IN
    
    current_timestamp = time.time()
    timestamps.append(current_timestamp)
    
    # Cleanup
    GPIO.cleanup()
