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
        if button.is_active and not run:
            print("Started")
            run = True
            start()
            while button.is_active:
                time.sleep(0.1)
        if not button.is_active and run:
            print("Stopped")
            run = False
            while not button.is_active:
                time.sleep(0.1)
 
except KeyboardInterrupt:
    print("Quit")
