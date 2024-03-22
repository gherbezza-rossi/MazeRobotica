import time
import subprocess, os
import signal
from gpiozero import Button

button = Button(17)
print("  Press Ctrl & C to Quit")

try:
    
   run = 0
   while True :
      if button.is_pressed and run == 0:
         print("  Started")
         rpistr = "python3 /home/sirio/Desktop/robot_git/MazeSirio/main.py"
         p=subprocess.Popen(rpistr,shell=True, preexec_fn=os.setsid)
         run = 1
         while button.is_pressed:
             time.sleep(0.1)
      if not button.is_pressed and run == 1:
         print("  Stopped ")
         run = 0
         os.killpg(p.pid, signal.SIGTERM)
         while button==0:
             time.sleep(0.1)
       

except KeyboardInterrupt:
  print("  Quit")