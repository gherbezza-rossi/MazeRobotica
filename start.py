import time
import subprocess
import os
import signal
from gpiozero import Button
from main import *

button = Button(17)
print("Press Ctrl & C to Quit")

try:
    run = False
    while True:
        if button.is_pressed and not run:
            print("Started")
            start()
            run = True
            while button.is_pressed:
                time.sleep(0.1)
        if not button.is_pressed and run:
            print("Stopped")
            run = False
            while not button.is_pressed:
                time.sleep(0.1)
 
except KeyboardInterrupt:
    print("Quit")
