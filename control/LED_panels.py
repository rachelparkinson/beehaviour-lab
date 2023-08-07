import RPi.GPIO as GPIO
import time

#Use appropriate GPIO pin, make it a variable for use
R_LED_PIN = 20
W_LED_PIN = 21

#to use standard GPIO numbers:
GPIO.setmode(GPIO.BCM)

#set as output pin (GPIO.IN = input pin)
GPIO.setup(R_LED_PIN, GPIO.OUT)
GPIO.setup(W_LED_PIN, GPIO.OUT)

while True:
    #Turn on white LED panel
    GPIO.output(W_LED_PIN, GPIO.HIGH)

    #wait 5s
    time.sleep(5)

    #Turn off white LED panel, turn on red LEDs
    GPIO.output(W_LED_PIN, GPIO.LOW)
    GPIO.output(R_LED_PIN, GPIO.HIGH)

    #wait 5s
    time.sleep(5)

    #turn off red LEDs
    GPIO.output(R_LED_PIN, GPIO.LOW)

#reset default mode "cleanup"
GPIO.cleanup()

exit
