import time
import subprocess
import os
import signal
from gpiozero import Button
from MazeClass import *



def move(first):
    print("first visited")
    walls, dati = myMaze.getValues(first)
    right_distance = dati[4]
    left_distance = dati[5]
    if myMaze.isAllVisited():
        print("is all visited")
        myMaze.goToStart()

    else:
        print("distances[r, l]: ", right_distance, left_distance)

        print("fn start")
        print("orientation: ", myMaze.orientation)
        myMaze.emptyRoomsFinding(right_distance, left_distance)
        myMaze.RR()

myMaze = Maze()

button = Button(17)
print("Press Ctrl & C to Quit")

first_run = True
try:
    run = False
    while True:
        if button.is_active and not run:
            print("Started")
            run = True
            move(first_run)
            first_run = False
            while button.is_active:
                time.sleep(0.1)
                move(first_run)
        if not button.is_active and run:
            print("Stopped")
            run = False
            while not button.is_active:
                time.sleep(0.1)
 
except KeyboardInterrupt:
    print("Quit")
