
from serial_test import *
import time
from percorso import *
from tof import *


while True:
    print(detect_walls())
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