from MazeClass import Maze
from python.servo import *
from python.led_control import *
user_input = input("hai rimosso il cavo del sensore colori? (yes/no): ")
if user_input.lower() in ["yes", "no"]:
    print("settaggio tof")
    from python.tof import *
    user_input = input("hai ricollegato il sensore? (yes/no): ")
    if user_input.lower() in ["yes", "no"]:
        print("settaggio sensore colori")
        print("settaggio telecamere")
        from python.telecamere import *

        # from python.color_sensor import *
else:
    print("Exiting...")

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm1_gpio, GPIO.OUT)
GPIO.setup(pwm2_gpio, GPIO.OUT)
pwm1 = GPIO.PWM(pwm1_gpio, frequence)
pwm2 = GPIO.PWM(pwm2_gpio, frequence)
pwm1.start(angle_to_percent(135))
pwm2.start(angle_to_percent(135))


myMaze = Maze()

    
        

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

def analyse_victim_right(victim):
    if victim == 'U':
        led_5()
    elif victim == 'S':
        led_5()
        send_medikit_right()
    elif victim == 'H':
        led_5()
        send_medikit_right()
        send_medikit_right()
        
def analyse_victim_left(victim):
    if victim == 'U':
        led_5()
    elif victim == 'S':
        led_5()
        send_medikit_left()
    elif victim == 'H':
        led_5()
        send_medikit_left()
        send_medikit_left()

def getValues(first):
    dati_tof = detect_walls()
    print(dati_tof)
    dati = dati_tof.split()
    print(dati)
    left = dati[0]
    front = dati[1]
    right = dati[3]

    walls = [left, front, right, 0]  # walls = [left, front, right, back]
    if first:
        walls[3] = 1

    myMaze.addBlockData(walls)
    myMaze.assignNumber()

    take_image_right()
    take_image_left()
    lettera_right=read_image_letter_right()
    analyse_victim_right(lettera_right)
    colore_right=find_square_shapes_right()
    lettera_left=read_image_letter_left()
    analyse_victim_left(lettera_left)
    colore_left=find_square_shapes_left()

    return walls, dati


def start(first):
    walls, dati = getValues(first)

    right_distance = dati[4]
    left_distance = dati[5] 

  #-------------------------------------------------------------------------------------------------
    print("fn start")
    print("distances[r, l]: ", right_distance, left_distance)
    print("orientation: ", myMaze.orientation)
    myMaze.emptyRoomsFinding(right_distance, left_distance)
    myMaze.RR()