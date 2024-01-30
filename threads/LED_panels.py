import RPi.GPIO as GPIO
import time

def lights(R_LED_PIN, W_LED_PIN, Rec_time):

    #set as output pin (GPIO.IN = input pin)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(R_LED_PIN, GPIO.OUT)
    GPIO.setup(W_LED_PIN, GPIO.OUT)
    GPIO.setup(W_LED_PIN, GPIO.LOW)
    
    #Turn on white LED panel
    GPIO.output(R_LED_PIN, GPIO.HIGH)

    #wait "LED_time" duration
    time.sleep(Rec_time)

    #turn off red LEDs
    GPIO.output(R_LED_PIN, GPIO.LOW)
    GPIO.output(W_LED_PIN, GPIO.LOW)
