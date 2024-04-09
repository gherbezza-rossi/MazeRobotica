from MazeClass import Maze
from python.servo import *
from python.led_control import *
from python.tof import *
from python.telecamere import *
from python.led_control import *
# from python.color_sensor import *

myMaze = Maze()

def initFunction():
    user_input = input("hai rimosso il cavo del sensore colori? (yes/no): ")
    if user_input.lower() in ["yes", "no"]:
        print("settaggio tof")
        user_input = input("hai ricollegato il sensore? (yes/no): ")
        if user_input.lower() in ["yes", "no"]:
            print("settaggio sensore colori")
            print("settaggio telecamere")
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pwm1_gpio, GPIO.OUT)
            GPIO.setup(pwm2_gpio, GPIO.OUT)
            pwm1 = GPIO.PWM(pwm1_gpio, frequence)
            pwm2 = GPIO.PWM(pwm2_gpio, frequence)
            pwm1.start(angle_to_percent(135))
            pwm2.start(angle_to_percent(135))
    else:
       print("Exiting...")

def send_medikit_right(): 
    pwm1.ChangeDutyCycle(angle_to_percent(180))
    time.sleep(1)
    pwm1.ChangeDutyCycle(angle_to_percent(135))
    time.sleep(0.5)
    GPIO.output(pwm1_gpio, GPIO.LOW)

def send_medikit_left(): 
    pwm2.ChangeDutyCycle(angle_to_percent(180))
    time.sleep(1)
    pwm2.ChangeDutyCycle(angle_to_percent(135))
    time.sleep(0.5)
    GPIO.output(pwm2_gpio, GPIO.LOW)

def getValues(first):
    dati_tof = detect_walls()
    print(dati_tof)
    dati = dati_tof.split()
    left = dati[0]
    front = dati[1]
    right = dati[2]

    walls = [left, front, right, 0]  # walls = [left, front, right, back]
    if first:
        walls[3] = 1

    myMaze.addBlockData(walls)
    myMaze.assignNumber()

    #take_image_right()
    #lettera_right=read_image_letter_right()
    #colore_right=find_square_shapes_right()
    return walls, dati


def start(first):
    walls, dati = getValues(first)

    right_distance = dati[4]
    left_distance = dati[5]
  # ----------------------------  altre cose che deve fare robot ---------------------------------

 # dati_camera1 = take_image_right()
 # close_camera_right()
  #print(dati_camera1[0])
  #if dati_camera1[0] == "U":
  #    mao=0
  #    print("letteraaaa")
  #    for mao in range(5):
  #        led_on()
#         time.sleep(0.25)
#         led_off()
#         time.sleep(0.25)
#         mao=mao+0.5
  #dati_camera2 = take_image_left()
  #close_camera_left()
#  dati_camera2=dati_camera2.replace(" ", "")
#  print(dati_camera2)
#  if dati_camera2 == "U":
#      mao=0
#      print("letteraaaa")
#      for mao in range(5):
#          led_on()
#           time.sleep(0.25)
#          led_off()
#          time.sleep(0.25)
#          mao=mao+0.5

  #-------------------------------------------------------------------------------------------------
    print("fn start")
    print("distances[r, l]: ", right_distance, left_distance)
    print("orientation: ", myMaze.orientation)
    myMaze.emptyRoomsFinding(right_distance, left_distance)
    myMaze.RR()


initFunction()