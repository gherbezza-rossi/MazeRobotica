from BlockClass import Block
from python.lettura_encoder import *

MAX_Y = 500
MAX_X = 500
MAX_VALUE = 1000000
class Maze(object):
    mapMaze = [[Block() for _ in range(MAX_X)] for _ in range(MAX_Y)]
    currentX = 250
    currentY = 499
    orientation = 0
        # 0 => lC=lA, fC=fA, rC=rA, bC=bA
        # 1 (90 to the right) => lA=bC, fA= lC, rA=fC, bA=rC
        # 2 (180) => lA=rC, fA=bC, rA=lC, bA=fC
        # 3 (270 to the right) => lA=fC, fA=rC, rA=bC, bA=lC



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

    def isRightFree(self):
        if self.orientation == 0:
            return not self.mapMaze[self.currentX][self.currentY].walls[2]

        elif self.orientation == 1:
            return not self.mapMaze[self.currentX][self.currentY].walls[3]

        elif self.orientation == 2:
            return not self.mapMaze[self.currentX][self.currentY].walls[0]

        elif self.orientation == 3:
            return not self.mapMaze[self.currentX][self.currentY].walls[1]

    def turnRight(self):
        self.orientation += 1
        self.orientation %= 4
        print("orientation: " + str(self.orientation))

    def turnLeft(self):
        self.orientation += 3
        self.orientation %= 4
        print("orientation: " + str(self.orientation))

    def goFwd(self):
        self.mapMaze[self.currentX][self.currentY].visited = 1

        if self.orientation == 0:
            self.currentY -= 1

        elif self.orientation == 1:
            self.currentX += 1

        elif self.orientation == 2:
            self.currentY += 1

        elif self.orientation == 3:  # right
            self.currentX -= 1

        print("Going fwd")
        send_serial("w")
        send_serial("r")

    def goBkw(self):
        if self.orientation == 0:
            self.currentY += 1

        elif self.orientation == 1:
            self.currentX -= 1

        elif self.orientation == 2:
            self.currentY -= 1

        elif self.orientation == 3:  # right
            self.currentX += 1

        print("going back")
        send_serial("s")
        send_serial("r")

    def goLeft(self):
        self.turnRight()
        send_serial("a")
        time.sleep(3)   
        self.goFwd()     

    def goRight(self):
        self.turnLeft()
        send_serial("d")
        time.sleep(3) 
        self.goFwd()      

    def isVisitedAllAround(self): #
        right = self.getRightBlock()
        if right is None:
            right = True
        else:
            right = right.isVisited()

        left = self.getLeftBlock()
        if left is None:
            left = True
        else:
            left = left.isVisited()

        fwd = self.getFwdBlock()
        if fwd is None:
            fwd = True
        else:
            fwd = fwd.isVisited()

        return right and left and fwd

    def addBlockData(self, walls):

        absolute_walls = walls

        if self.orientation == 1:
            absolute_walls[0] = walls[1]
            absolute_walls[1] = walls[2]
            absolute_walls[2] = walls[3]
            absolute_walls[3] = walls[0]

        elif self.orientation == 2:
            absolute_walls[0] = walls[2]
            absolute_walls[1] = walls[3]
            absolute_walls[2] = walls[0]
            absolute_walls[3] = walls[1]

        elif self.orientation == 3:
            absolute_walls[0] = walls[3]
            absolute_walls[1] = walls[0]
            absolute_walls[2] = walls[1]
            absolute_walls[3] = walls[2]


        self.mapMaze[self.currentX][self.currentY].walls = absolute_walls
        self.mapMaze[self.currentX][self.currentY].data = ""
        self.mapMaze[self.currentX][self.currentY].setAsVisited()
        print(self.mapMaze[self.currentX][self.currentY].walls)

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
    
    def theFirstFunctionDISTANCE(self, right_distance, left_distance):
        right = self.getRightBlock()
        left = self.getLeftBlock()

        if right_distance == 1 and right is not None and right.isVisited() == 0:
            print(right_distance == 1)
            print(right is not None)
            print(right.isVisited() == 0)
            self.goRight()
            self.emptyGoing()
        elif left_distance == 1 and left is not None and left.isVisited() == 0:
            print("werbvrvwe")
            self.goLeft()
            self.emptyGoing()

    def emptyGoing(self):
        while self.mapMaze[self.currentX][self.currentY].hasWalls() == 0:
            self.goFwd()

        while self.mapMaze[self.currentX][self.currentY].respectedRR == 0:
            self.goBkw()


    def notBlockedOrVisited(self, direction):
        if direction == "r":
            print(self.mapMaze[self.currentX][self.currentY].hasRightWall() and self.getRightBlock() is not None)
            return self.mapMaze[self.currentX][self.currentY].hasRightWall() and self.getRightBlock() is not None
        elif direction == "f":
            return self.mapMaze[self.currentX][self.currentY].hasFrontWall() and self.getFwdBlock() is not None
        elif direction == "l":
            return self.mapMaze[self.currentX][self.currentY].hasLeftWall() and self.getLeftBlock() is not None
        else:
            return True
    
    def notBlocked(self, direction):
        print("blocked")
        if direction == "r":
            print(self.mapMaze[self.currentX][self.currentY].hasRightWall())
            return self.mapMaze[self.currentX][self.currentY].hasRightWall()
        elif direction == "f":
            return self.mapMaze[self.currentX][self.currentY].hasFrontWall()
        elif direction == "l":
            return self.mapMaze[self.currentX][self.currentY].hasLeftWall()
        else:
            return True

    def RR(self):
        print("right rule")
        if not self.notBlockedOrVisited("r"):
            print("oviubriu")
            self.mapMaze[self.currentX][self.currentY].respectedRR = 1
            self.goRight()
        elif not self.notBlockedOrVisited("f"):

            self.mapMaze[self.currentX][self.currentY].respectedRR = 1
            self.goFwd()
        elif not self.notBlockedOrVisited("l"):
            self.mapMaze[self.currentX][self.currentY].respectedRR = 1
            self.goLeft()
        elif not self.notBlocked("r"):
            print("iewbu")
            self.mapMaze[self.currentX][self.currentY].respectedRR = 1
            self.goRight()
        elif not self.notBlocked("f"):
            self.mapMaze[self.currentX][self.currentY].respectedRR = 1
            self.goFwd()
        elif not self.notBlocked("l"):
            self.mapMaze[self.currentX][self.currentY].respectedRR = 1
            self.goLeft()
        else:
            self.mapMaze[self.currentX][self.currentY].respectedRR = 1
            self.goBkw()
