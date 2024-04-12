import RPi.GPIO as GPIO
from BlockClass import Block
from python.servo import *
from python.tof import *
from python.telecamere import *
from python.lettura_encoder import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwm1_gpio, GPIO.OUT)
GPIO.setup(pwm2_gpio, GPIO.OUT)
pwm1 = GPIO.PWM(pwm1_gpio, frequence)
pwm2 = GPIO.PWM(pwm2_gpio, frequence)
pwm1.start(angle_to_percent(180))
pwm2.start(angle_to_percent(180))

MAX_Y = 500
MAX_X = 500
MAX_VALUE = 1000000

class Maze(object):
    mapMaze = [[Block() for _ in range(MAX_X)] for _ in range(MAX_Y)]
    currentX = int(MAX_X / 2)
    currentY = MAX_Y - 2
    orientation = 0
        # 0 => lC=lA, fC=fA, rC=rA, bC=bA
        # 1 (90 to the right) => lA=bC, fA= lC, rA=fC, bA=rC
        # 2 (180) => lA=rC, fA=bC, rA=lC, bA=fC
        # 3 (270 to the right) => lA=fC, fA=rC, rA=bC, bA=lC


#--------------------------------------------- WALLS

    def hasCurrentRightWall(self):
        if self.orientation == 0:
            return self.currentBlock().hasRightWall()
        elif self.orientation == 1:
            return self.currentBlock().hasBackWall()
        elif self.orientation == 2:
            return self.currentBlock().hasLeftWall()
        elif self.orientation == 3:
            return self.currentBlock().hasFrontWall()

    def hasCurrentFrontWall(self):
        if self.orientation == 0:
            return self.currentBlock().hasFrontWall()
        elif self.orientation == 1:
            return self.currentBlock().hasRightWall()
        elif self.orientation == 2:
            return self.currentBlock().hasBackWall()
        elif self.orientation == 3:
            return self.currentBlock().hasLeftWall()

    def hasCurrentLeftWall(self):
        if self.orientation == 0:
            return self.currentBlock().hasLeftWall()
        elif self.orientation == 1:
            return self.currentBlock().hasFrontWall()
        elif self.orientation == 2:
            return self.currentBlock().hasRightWall()
        elif self.orientation == 3:
            return self.currentBlock().hasBackWall()

    def hasCurrentBackWall(self):
        if self.orientation == 0:
            return self.currentBlock().hasBackWall()
        elif self.orientation == 1:
            return self.currentBlock().hasLeftWall()
        elif self.orientation == 2:
            return self.currentBlock().hasFrontWall()
        elif self.orientation == 3:
            return self.currentBlock().hasRightWall()

#--------------------------------------------- BLOCKS
    def currentBlock(self):
        return self.mapMaze[self.currentX][self.currentY]

    def getRightBlock(self):
        if self.orientation == 0 and self.currentX+1<MAX_X:
            return self.mapMaze[self.currentX+1][self.currentY] #
        elif self.orientation == 1 and self.currentY+1>MAX_Y:
            return self.mapMaze[self.currentX][self.currentY+1] #
        elif self.orientation == 2  and self.currentX-1>=0:
            return self.mapMaze[self.currentX-1][self.currentY] #
        elif self.orientation == 3 and self.currentY-1>=0:
            return self.mapMaze[self.currentX][self.currentY-1] #
        else:
            return None

    def getLeftBlock(self):
        if self.orientation == 0 and self.currentX-1>=0:
            return self.mapMaze[self.currentX-1][self.currentY] #
        elif self.orientation == 1 and self.currentY-1>=0:
            return self.mapMaze[self.currentX][self.currentY-1] #
        elif self.orientation == 2 and self.currentX+1<MAX_X:
            return self.mapMaze[self.currentX+1][self.currentY] #
        elif self.orientation == 3 and self.currentY+1<MAX_Y:
            return self.mapMaze[self.currentX][self.currentY+1] #
        else:
            return None

    def getFwdBlock(self):
        if self.orientation == 0 and self.currentY-1>=0:
            return self.mapMaze[self.currentX][self.currentY-1] #
        elif self.orientation == 1 and self.currentX+1<MAX_X:
            return self.mapMaze[self.currentX+1][self.currentY] #
        elif self.orientation == 2 and self.currentY+1<MAX_Y:
            return self.mapMaze[self.currentX][self.currentY+1] #
        elif self.orientation == 3 and self.currentX-1>=0:
            return self.mapMaze[self.currentX-1][self.currentY] #
        else:
            return None

    def getBkwBlock(self):
        if self.orientation == 0 and self.currentY+1<MAX_Y:
            return self.mapMaze[self.currentX][self.currentY+1] #
        elif self.orientation == 1 and self.currentX-1>=0:
            return self.mapMaze[self.currentX-1][self.currentY] #
        elif self.orientation == 2 and self.currentY-1>=0:
            return self.mapMaze[self.currentX][self.currentY-1] #
        elif self.orientation == 3 and self.currentX+1<MAX_X:
            return self.mapMaze[self.currentX+1][self.currentY] #
        else:
            return None

    def getLowerValue(self):
        print("- cerca valore minore intorno")
        if not self.hasCurrentRightWall() and not self.getRightBlock() is None:
            right_value = self.getRightBlock().getValue()
        else:
            right_value = MAX_VALUE

        if not self.hasCurrentLeftWall() and not self.getLeftBlock() is None:
            left_value = self.getRightBlock().getValue()
        else:
            left_value = MAX_VALUE

        if not self.hasCurrentFrontWall() and not self.getFwdBlock() is None:
            fwd_value = self.getRightBlock().getValue()
        else:
            fwd_value = MAX_VALUE


        if fwd_value <= right_value and fwd_value <= left_value:
            return 1
        elif left_value <= right_value and left_value <= fwd_value:
            return 0
        else:
            return 2


    #--------------------------------------------- SINGLE MOVEMENTS

    def turnRight(self):
        self.orientation += 1
        self.orientation %= 4
        send_serial("d")
        print("- orientation after turning right: " + str(self.orientation))

    def turnLeft(self):
        self.orientation += 3
        self.orientation %= 4
        send_serial("a")
        print("- orientation after turning right: " + str(self.orientation))

    def goFwd(self):
        if self.orientation == 0:
            self.currentY -= 1

        elif self.orientation == 1:
            self.currentX += 1

        elif self.orientation == 2:
            self.currentY += 1

        elif self.orientation == 3:  # right
            self.currentX -= 1

        print("- Going fwd")

        black, stairs = send_serial("w")
        if black: # if found black
            
            print("- black received")

            if self.orientation == 0:
                self.currentY += 1

            elif self.orientation == 1:
                self.currentX -= 1

            elif self.orientation == 2:
                self.currentY -= 1

            elif self.orientation == 3:
                self.currentX += 1

            self.mapMaze[self.currentX][self.currentY].walls[1] = "1"

            # go back a bit

        elif stairs:

            print("- stairs received")
            self.goneFwdStairs()

        time.sleep(1.5)
        #send_serial("r")
        print("- I have gone fwd")

    def goBkw(self):
        if self.orientation == 0:
            self.currentY += 1

        elif self.orientation == 1:
            self.currentX -= 1

        elif self.orientation == 2:
            self.currentY -= 1

        elif self.orientation == 3:  # right
            self.currentX += 1

        print("- going back")
        self.turnRight()
        time.sleep(0.5)
        #send_serial("r")
        self.turnRight()
        time.sleep(0.5)
        self.goFwd()
        time.sleep(0.5)
        #send_serial("r")
        #time.sleep(0.5)
        print("- gone bwd")

    def goLeft(self):
        print("- going left")
        self.turnLeft()
        time.sleep(0.5)
        self.goFwd()
        print("- gone left")

    def goRight(self):
        print("- going right")
        self.turnRight()
        time.sleep(0.5) 
        self.goFwd()
        print("- gone right")

#--------------------------------------------- SPECIAL CASES

    def goneFwdStairs(self):
        if self.orientation == 0:
            self.currentY -= 1

        elif self.orientation == 1:
            self.currentX += 1

        elif self.orientation == 2:
            self.currentY += 1

        elif self.orientation == 3:  # right
            self.currentX -= 1

        self.mapMaze[self.currentX][self.currentY].walls = [1, 0, 1, 0]

        if self.orientation == 0:
            self.currentY -= 1

        elif self.orientation == 1:
            self.currentX += 1

        elif self.orientation == 2:
            self.currentY += 1

        elif self.orientation == 3:  # right
            self.currentX -= 1

    def emptyGoing(self):
        while not self.currentBlock().hasWalls():
            print("- i am going into an empty room")
            self.goFwd()
            self.getValues(False)

        while not self.currentBlock().respectedRR:
            print("- i am coming back from an empty room")
            self.goBkw()

    def isAllVisited(self):
        print("- checking all visited")

        for x in range(MAX_X):
            for y in range(MAX_Y):
                if self.mapMaze[x][y].visited == 2:
                    return False
        return True

    def closedBlock(self):
        print("- i do closed block stuff")

        self.turnLeft()

        take_image_right()
        lettera_right=read_image_letter_right()
        analyse_victim_right(lettera_right)

        self.turnLeft()
        time.sleep(0.5)
        self.goFwd()
        time.sleep(0.5)

        if self.orientation == 0:
            self.currentY += 1

        elif self.orientation == 1:
            self.currentX -= 1

        elif self.orientation == 2:
            self.currentY -= 1

        elif self.orientation == 3:  # right
            self.currentX += 1

    def notBlockedAndNotVisited(self, direction):
        if direction == "r":
            if self.getRightBlock() is None:
                return False
            return not self.hasCurrentRightWall() and not self.getRightBlock().isVisited()
        elif direction == "f":
            if self.getFwdBlock() is None:
                return False
            return not self.hasCurrentFrontWall() and not self.getFwdBlock().isVisited()
        elif direction == "l":
            if self.getLeftBlock() is None:
                return False
            return not self.hasCurrentLeftWall() and not self.getLeftBlock().isVisited()
        else:
            return True

    def blocked(self, direction):
        if direction == "r":
            return self.hasCurrentRightWall()
        elif direction == "f":
            return self.hasCurrentFrontWall()
        elif direction == "l":
            return self.hasCurrentLeftWall()
        else:
            return self.hasCurrentBackWall()


#--------------------------------------------- SET BLOCK DATA

    def getValues(self, first):
        dati_tof = detect_walls()
        dati = dati_tof.split()
        print("- tof ", dati)

        left = int(dati[0])
        front = int(dati[1])
        right = int(dati[3])

        walls = [left, front, right, 0]  # walls = [left, front, right, back]
        if first:
            walls[3] = 0

        self.addBlockData(walls)
        self.assignNumber()

        take_image_right()
        lettera_right=read_image_letter_right()
        analyse_victim_right(lettera_right)
        colore_right=find_square_shapes_right()
        analyse_victim_right(colore_right)

        take_image_left()
        lettera_left=read_image_letter_left()
        analyse_victim_left(lettera_left)
        colore_left=find_square_shapes_left()
        analyse_victim_left(colore_left)


        self.mapMaze[self.currentX][self.currentY].setAsVisited()


        return walls, dati

    def addBlockData(self, walls):
        print("- add data")
        absolute_walls = []

        if self.orientation == 1:
            absolute_walls.append(walls[3])
            absolute_walls.append(walls[0])
            absolute_walls.append(walls[1])
            absolute_walls.append(walls[2])

        elif self.orientation == 2:
            absolute_walls.append(walls[2])
            absolute_walls.append(walls[3])
            absolute_walls.append(walls[0])
            absolute_walls.append(walls[1])

        elif self.orientation == 3:
            absolute_walls.append(walls[1])
            absolute_walls.append(walls[2])
            absolute_walls.append(walls[3])
            absolute_walls.append(walls[0])
        else:
            absolute_walls.append(walls[0])
            absolute_walls.append(walls[1])
            absolute_walls.append(walls[2])
            absolute_walls.append(walls[3])

        self.mapMaze[self.currentX][self.currentY].walls = absolute_walls

        if not self.hasCurrentLeftWall():
            if self.orientation == 0 and self.currentX - 1 >= 0:
                self.mapMaze[self.currentX - 1][self.currentY].visited = 2
            elif self.orientation == 1 and self.currentY - 1 >= 0:
                self.mapMaze[self.currentX][self.currentY - 1].visited = 2
            elif self.orientation == 2 and self.currentX + 1 < MAX_X:
                self.mapMaze[self.currentX + 1][self.currentY].visited = 2
            elif self.orientation == 3 and self.currentY + 1 < MAX_Y:
                self.mapMaze[self.currentX][self.currentY + 1].visited = 2

        if not self.hasCurrentFrontWall():
            if self.orientation == 0 and self.currentY - 1 >= 0:
                self.mapMaze[self.currentX][self.currentY - 1].visited = 2
            elif self.orientation == 1 and self.currentX + 1 < MAX_X:
                self.mapMaze[self.currentX + 1][self.currentY].visited = 2
            elif self.orientation == 2 and self.currentY + 1 < MAX_Y:
                self.mapMaze[self.currentX][self.currentY + 1].visited = 2
            elif self.orientation == 3 and self.currentX - 1 >= 0:
                self.mapMaze[self.currentX - 1][self.currentY].visited = 2

        if not self.hasCurrentRightWall():
            if self.orientation == 0 and self.currentX + 1 < MAX_X:
                self.mapMaze[self.currentX + 1][self.currentY].visited = 2
            elif self.orientation == 1 and self.currentY + 1 > MAX_Y:
                self.mapMaze[self.currentX][self.currentY + 1].visited = 2
            elif self.orientation == 2 and self.currentX - 1 >= 0:
                self.mapMaze[self.currentX - 1][self.currentY].visited = 2
            elif self.orientation == 3 and self.currentY - 1 >= 0:
                self.mapMaze[self.currentX][self.currentY - 1].visited = 2

        if not self.hasCurrentBackWall():
            if self.orientation == 0 and self.currentY + 1 < MAX_Y:
                self.mapMaze[self.currentX][self.currentY + 1].visited = 2
            elif self.orientation == 1 and self.currentX - 1 >= 0:
                self.mapMaze[self.currentX - 1][self.currentY].visited = 2
            elif self.orientation == 2 and self.currentY - 1 >= 0:
                self.mapMaze[self.currentX][self.currentY - 1].visited = 2
            elif self.orientation == 3 and self.currentX + 1 < MAX_X:
                self.mapMaze[self.currentX + 1][self.currentY].visited = 2



        print("- \tabsolute walls: ", self.currentBlock().walls, "\n- \trecorded walls: ", walls)

    def assignNumber(self):

        right = self.getRightBlock()
        if right is None:
            right = MAX_VALUE
        else:
            right = right.getValue()

        left = self.getLeftBlock()
        if left is None:
            left = MAX_VALUE
        else:
            left = left.getValue()

        fwd = self.getFwdBlock()
        if fwd is None:
            fwd = MAX_VALUE
        else:
            fwd = fwd.getValue()

        bkw = self.getBkwBlock()
        if bkw is None:
            bkw = MAX_VALUE
        else:
            bkw = bkw.getValue()


        self.mapMaze[self.currentX][self.currentY].setValue(
            min(right, left, fwd, bkw) + 1
        )

        print("- i am assigning a number ", self.currentBlock().getValue())

#--------------------------------------------- MOVEMENT ALGO
    def emptyRoomsFinding(self, right_distance, left_distance):

        right = self.getRightBlock()
        left = self.getLeftBlock()

        if right_distance == 1 and right is not None and right.isVisited() == 0:
            print("- empty room in the right")
            self.goRight()
            self.emptyGoing()
        elif left_distance == 1 and left is not None and left.isVisited() == 0:
            print("- empty room in the left")
            self.goLeft()
            self.emptyGoing()

    def RR(self):
        if self.notBlockedAndNotVisited("r"):
            print("- right, no wall, not visited")
            self.goRight()
        elif self.notBlockedAndNotVisited("f"):
            print("- fwd, no wall, not visited")
            self.goFwd()
        elif self.notBlockedAndNotVisited("l"):
            print("- left, no wall, not visited")
            self.goLeft()
        elif not self.blocked("r"):
            print("- right, no wall, visited")
            self.goRight()
        elif not self.blocked("f"):
            print("- fwd, no wall, visited")
            self.goFwd()
        elif not self.blocked("l"):
            print("- left, no wall, visited")
            self.goLeft()
        else:
            print("- closed block, walls")
            self.closedBlock()

        self.mapMaze[self.currentX][self.currentY].respectedRR = 1

    def goToStart(self):
        print("- Going to start")

        while self.currentBlock().getValue() > 1:
            print("- current value: ", self.currentBlock().getValue())
            min_value = self.getLowerValue()

            if min_value == 0:
                print("- go left")
                self.goLeft()
            elif min_value == 1:
                print("- go fwd")
                self.goFwd()
            elif min_value == 2:
                print("- go right")
                self.goRight()

#-------------------------------------------------------------------- OTHER FUNCTIONS

def send_medikit_right(): 
    pwm1.ChangeDutyCycle(angle_to_percent(135))
    time.sleep(1)
    pwm1.ChangeDutyCycle(angle_to_percent(180))
    time.sleep(0.5)
    GPIO.output(pwm1_gpio, GPIO.LOW)

def send_medikit_left(): 
    pwm2.ChangeDutyCycle(angle_to_percent(135))
    time.sleep(1)
    pwm2.ChangeDutyCycle(angle_to_percent(180))
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
    elif victim == 'Verde':
        led_5()
    elif victim == 'Giallo':
        led_5()
        send_medikit_right()
    elif victim == 'Rosso':
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
    elif victim == 'Verde':
        led_5()
    elif victim == 'Giallo':
        led_5()
        send_medikit_right()
    elif victim == 'Rosso':
        led_5()
        send_medikit_right()
        send_medikit_right()
