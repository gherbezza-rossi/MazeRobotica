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
        print("orientation after turning right: " + str(self.orientation))

    def turnLeft(self):
        self.orientation += 3
        self.orientation %= 4
        print("orientation after turning right: " + str(self.orientation))

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
        time.sleep(3)
        send_serial("r")
        time.sleep(3)
        print("I have gone fwd")

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
        time.sleep(3)
        send_serial("r")
        time.sleep(3)
        print("gone bwd")

    def goLeft(self):
        print("going left")
        self.turnLeft()
        send_serial("a")
        time.sleep(3)   
        self.goFwd()
        print("gone left")

    def goRight(self):
        print("going right")
        self.turnRight()
        send_serial("d")
        time.sleep(3) 
        self.goFwd()
        print("gone right")

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

        print("all visited: ", (right and left and fwd))

        return right and left and fwd

    def addBlockData(self, walls):
        print("add data")
        absolute_walls = walls

        if self.orientation == 1:
            absolute_walls[1] = walls[0]
            absolute_walls[2] = walls[1]
            absolute_walls[3] = walls[2]
            absolute_walls[0] = walls[3]

        elif self.orientation == 2:
            absolute_walls[0] = walls[2]
            absolute_walls[1] = walls[3]
            absolute_walls[2] = walls[0]
            absolute_walls[3] = walls[1]

        elif self.orientation == 3:
            absolute_walls[0] = walls[1]
            absolute_walls[1] = walls[2]
            absolute_walls[2] = walls[3]
            absolute_walls[3] = walls[0]


        self.mapMaze[self.currentX][self.currentY].walls = absolute_walls
        self.mapMaze[self.currentX][self.currentY].setAsVisited()
        print("absolute walls: ", self.mapMaze[self.currentX][self.currentY].walls, "\trecorded walls: ", walls)

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

        print("i am assigning a number ", self.mapMaze[self.currentX][self.currentY].getValue())
    
    def emptyRoomsFinding(self, right_distance, left_distance):

        print("looking for empty rooms")

        right = self.getRightBlock()
        left = self.getLeftBlock()

        if right_distance == 1 and right is not None and right.isVisited() == 0:
            print("empty room in the right")
            self.goRight()
            self.emptyGoing()
        elif left_distance == 1 and left is not None and left.isVisited() == 0:
            print("empty room in the left")
            self.goLeft()
            self.emptyGoing()

    def emptyGoing(self):
        while not self.mapMaze[self.currentX][self.currentY].hasWalls():
            print("i am going into an empty room")
            self.goFwd()
            getValues(False)
            # TODO: read block data

        while not self.mapMaze[self.currentX][self.currentY].respectedRR:
            print("i am coming back from an empty room")
            self.goBkw()


    def notBlockedAndNotVisited(self, direction):
        if direction == "r":
            if self.getRightBlock() is None:
                return False
            return not self.mapMaze[self.currentX][self.currentY].hasRightWall() and not self.getRightBlock().isVisited()
        elif direction == "f":
            if self.getFwdBlock() is None:
                return False
            return not self.mapMaze[self.currentX][self.currentY].hasFrontWall() and not self.getFwdBlock().isVisited()
        elif direction == "l":
            if self.getLeftBlock() is None:
                return False
            return not self.mapMaze[self.currentX][self.currentY].hasLeftWall() and not self.getLeftBlock().isVisited()
        else:
            return True
    
    def blocked(self, direction):
        if direction == "r":
            return self.mapMaze[self.currentX][self.currentY].hasRightWall()
        elif direction == "f":
            return self.mapMaze[self.currentX][self.currentY].hasFrontWall()
        elif direction == "l":
            return self.mapMaze[self.currentX][self.currentY].hasLeftWall()
        else:
            return False

    def vicoloCieco(self):
            # TODO: turn and search for victims
        print ("i do vicolo cieco stuff")

    def RR(self):
        print("fn RR")
        if self.notBlockedAndNotVisited("r"):
            print("right, no wall, not visited")
            self.mapMaze[self.currentX][self.currentY].respectedRR = 1
            self.goRight()
        elif self.notBlockedAndNotVisited("f"):
            print("fwd, no wall, not visited")
            self.mapMaze[self.currentX][self.currentY].respectedRR = 1
            self.goFwd()
        elif self.notBlockedAndNotVisited("l"):
            print("left, no wall, not visited")
            self.mapMaze[self.currentX][self.currentY].respectedRR = 1
            self.goLeft()
        elif not self.blocked("r"):
            print("right, no wall, visited")
            self.mapMaze[self.currentX][self.currentY].respectedRR = 1
            self.goRight()
        elif not self.blocked("f"):
            print("fwd, no wall, visited")
            self.mapMaze[self.currentX][self.currentY].respectedRR = 1
            self.goFwd()
        elif not self.blocked("l"):
            print("left, no wall, visited")
            self.mapMaze[self.currentX][self.currentY].respectedRR = 1
            self.goLeft()
        else:
            print("vicolo cieco, walls")
            self.vicoloCieco()
            self.mapMaze[self.currentX][self.currentY].respectedRR = 1
            self.goBkw()
