
from lettura_encoder import *
import time
from percorso import *
from servo import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm1_gpio, GPIO.OUT)
pwm1 = GPIO.PWM(pwm1_gpio, frequence)
pwm1.start(angle_to_percent(135))
def send_medikit_right(): 
    pwm1.ChangeDutyCycle(angle_to_percent(180))
    time.sleep(1)
    pwm1.ChangeDutyCycle(angle_to_percent(135))
    time.sleep(0.5)
    GPIO.output(pwm1_gpio, GPIO.LOW)
    

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
    elif messaggio_da_inviare == "mr":
        send_medikit_right()