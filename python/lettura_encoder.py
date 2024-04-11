#!/usr/bin/env python3
import serial
import time
import numpy as np
import RPi.GPIO as GPIO
from color_sensor import *
from ..MazeClass import getNero

ppr = 300.8 
tstop = 20  
tsample = 0.01
tdisp = 0.5
anglecurr = 0
tprev = 0
tcurr = 0
angolo_mao=0
prev_encoder_steps=0
tstart = time.perf_counter()


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

enc_Al_pin = 27
enc_Ar_pin = 22



GPIO.setup(enc_Al_pin, GPIO.IN)
GPIO.setup(enc_Ar_pin, GPIO.IN)

start = time.time()
period = 0.5

last_AA = 0b00
counter_A = 0

outcome = [0,-1,1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]




ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.01)
ser.setDTR(False)
time.sleep(1)
ser.flushInput()
ser.setDTR(True)
time.sleep(1)

def send_serial(a): # todo restituisce 1 quando trova nero, 1 se è salita/discesa
    global last_AA, counter_A
    if a=="w":
        a=a.encode('utf-8')
        ser.write(a)
        miao=""
        while True:
            # Encoder reading
            left_A = GPIO.input(enc_Al_pin)
            right_A = GPIO.input(enc_Ar_pin)
        
                
            while True:
                current_aa = (left_A << 1) | right_A
                position = (last_AA << 2) | current_aa
                counter_A += outcome[position]
                last_AA = current_aa
                nero=getNero()
                casella_nera=read_sensor_color_black(nero)
                if casella_nera:
                    q=str("q")
                    ser.write(q.encode('utf-8'))
                    time.sleep(0.5)
                    s=str("s")
                    ser.write(s.encode('utf-8'))
                    while True:
                        current_aa = (left_A << 1) | right_A
                        position = (last_AA << 2) | current_aa
                        counter_A -= outcome[position]
                        last_AA = current_aa
                        if(counter_A>0): #serve 1.44 per arrivare a 30cm, cioè un giro completo più 0.44 giri
                            q=str("q")
                            ser.write(q.encode('utf-8'))
                            time.sleep(1)
                            counter_A=0
                            last_AA=0
                            miao="finito"
                            break
                    break
                elif(counter_A<-2160): #serve 1.44 per arrivare a 30cm, cioè un giro completo più 0.44 giri
                    line = ser.readline().decode("utf-8")
                    print(line)
                    if line.strip() == "inclinato":
                        while True:
                            line = ser.readline().decode("utf-8")
                            if line.strip() == "completata salita":
                                time.sleep(0.5)
                                break
                        q=str("q")
                        ser.write(q.encode('utf-8'))
                        time.sleep(1)
                        counter_A=0
                        last_AA=0
                        miao="finito"
                        inclinato=True
                        break
                    else:
                        q=str("q")
                        ser.write(q.encode('utf-8'))
                        time.sleep(1)
                        counter_A=0
                        last_AA=0
                        miao="finito"
                        inclinato=False
                        break
        
                # stop loop in time = period
                if time.time() > start + period : break
            if miao =="finito" : 
                break
    
        return inclinato, casella_nera
    
            
    elif a=="s":
        a=a.encode('utf-8')
        ser.write(a)
        miao=""
        while True:
            # Encoder reading
            left_A = GPIO.input(enc_Al_pin)
            right_A = GPIO.input(enc_Ar_pin)
        
                
            while True:
                current_aa = (left_A << 1) | right_A
                position = (last_AA << 2) | current_aa
                counter_A += outcome[position]
                last_AA = current_aa
                if(counter_A>2160): #serve 1.44 per arrivare a 30cm, cioè un giro completo più 0.44 giri
                    q=str("q")
                    ser.write(q.encode('utf-8'))
                    time.sleep(1)
                    counter_A=0
                    last_AA=0
                    miao="finito"
                    break
        
                # stop loop in time = period
                if time.time() > start + period : break
            if miao =="finito" : 
                break


    elif a=="a" or a=="d" or a=="r":
        a=a.encode('utf-8')
        ser.write(a)
        while True:
            line = ser.readline().decode("utf-8")
            if line.strip() == "Complete":
                break
              