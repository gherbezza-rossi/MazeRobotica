import RPi.GPIO as GPIO
import time


enc_Al_pin = 13
enc_Ar_pin = 15



GPIO.setup(enc_Al_pin, GPIO.IN)
GPIO.setup(enc_Ar_pin, GPIO.IN)

        
# Loop to make the robot move forward
''' We run the code for 5 seconds. Period is the time that we have to run it for'''
start = time.time()
period = 0.5

last_AA = 0b00
last_BB = 0b00
counter_A = 0
counter_B = 0

outcome = [0,-1,1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]


''' The ChangeDutyCycle() makes the motors rotate at that speed '''
try:
    while True:
      # Encoder reading
      left_A = GPIO.input(enc_Al_pin)
      right_A = GPIO.input(enc_Ar_pin)
 
        
      while True:
        current_aa = (left_A << 1) | right_A
        position = (last_AA << 2) | current_aa
        counter_A += outcome[position]
        last_AA = current_aa
        print('A = ', counter_A)
        
        # stop loop in time = period
        if time.time() > start + period : break
              
         
    
except KeyboardInterrupt:
    pass


GPIO.cleanup()