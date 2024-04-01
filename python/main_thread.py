
from lettura_encoder import *
import time
from percorso import *
from servo import *



def send_medikit():    
    pwm.start(angle_to_percent(180))
    time.sleep(1)
    pwm.ChangeDutyCycle(angle_to_percent(135))
    time.sleep(1)
    pwm.stop()
    GPIO.cleanup()
    

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
    elif messaggio_da_inviare == "m":
        GPIO.setup(pwm_gpio, GPIO.OUT)
        pwm = GPIO.PWM(pwm_gpio, frequence)
        send_medikit()