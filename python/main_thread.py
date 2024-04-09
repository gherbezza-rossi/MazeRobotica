
from lettura_encoder import *
import time
from percorso import *
from servo import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm1_gpio, GPIO.OUT)
GPIO.setup(pwm2_gpio, GPIO.OUT)
pwm1 = GPIO.PWM(pwm1_gpio, frequence)
pwm2 = GPIO.PWM(pwm2_gpio, frequence)
pwm1.start(angle_to_percent(180))
pwm2.start(angle_to_percent(180))


def send_medikit_right(): 
    pwm1.ChangeDutyCycle(angle_to_percent(135))
    time.sleep(2)
    pwm1.ChangeDutyCycle(angle_to_percent(180))
    time.sleep(0.2)
    GPIO.output(pwm1_gpio, GPIO.LOW)
    
def send_medikit_left(): 
    pwm2.ChangeDutyCycle(angle_to_percent(135))
    time.sleep(2)
    pwm2.ChangeDutyCycle(angle_to_percent(180))
    time.sleep(0.2)
    GPIO.output(pwm2_gpio, GPIO.LOW)

while True:
    messaggio_da_inviare = input("Inserisci il messaggio da inviare: ")
    if messaggio_da_inviare == "a":
        calcolo_posizione("a")
        send_serial(messaggio_da_inviare)
    elif messaggio_da_inviare == "w":
        send_serial(messaggio_da_inviare)
    elif messaggio_da_inviare == "q":
        send_serial(messaggio_da_inviare)
    elif messaggio_da_inviare == "s":
        send_serial(messaggio_da_inviare)
    elif messaggio_da_inviare == "d":
        send_serial(messaggio_da_inviare)
    elif messaggio_da_inviare == "r":
        send_serial(messaggio_da_inviare)
    elif messaggio_da_inviare == "mr":
        send_medikit_right()
    elif messaggio_da_inviare == "ml":
        send_medikit_left()