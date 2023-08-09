import RPi.GPIO as GPIO
import time

def lights(R_LED_PIN, W_LED_PIN, LED_time, start_time, Rec_time):

    #set as output pin (GPIO.IN = input pin)
    GPIO.setup(R_LED_PIN, GPIO.OUT)
    GPIO.setup(W_LED_PIN, GPIO.OUT)
    
    while time.time() - start_time < Rec_time:
        #Turn on white LED panel
        GPIO.output(W_LED_PIN, GPIO.HIGH)

        #wait "LED_time" duration
        time.sleep(LED_time)

        #Turn off white LED panel, turn on red LEDs
        GPIO.output(W_LED_PIN, GPIO.LOW)
        GPIO.output(R_LED_PIN, GPIO.HIGH)

        #Wait LED_time duration
        time.sleep(LED_time)

        #turn off red LEDs
        GPIO.output(R_LED_PIN, GPIO.LOW)