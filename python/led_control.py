import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.OUT)


def led_on():
    GPIO.output(4,GPIO.HIGH)
    
def led_off():
    GPIO.output(4,GPIO.LOW)