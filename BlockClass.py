class Block:
    # walls = [left, front, right, back]
    # data = random stuff u need to save
    def __init__(self):
        self.walls = [0, 0, 0, 0]
        self.data = ""
        self.rightDistance = 0
        self.leftDistance = 0
        self.visited = 0
        self.respectedRR = False
        self.value = 0


    def isVisited(self):
        return self.visited == 1
    def setAsVisited(self):
        self.visited = 1
    def getData(self):
        return self.data
    def setData(self, data):
        self.data = data

# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------walls
    def hasWalls(self):
        return self.hasLeftWall() or self.hasRightWall() or self.hasFrontWall()

    # ------------------------------------------------left wall
    def hasLeftWall(self):
        return self.walls[0] == "1"  or self.walls[0] == 1
    def getLeftWall(self):
        return self.walls[0]== "1"
    def setLeftWall(self, wall):
        self.walls[0] = wall


    # ------------------------------------------------front wall
    def hasFrontWall(self):
        return self.walls[1] == "1" or self.walls[1] == 1
    def getFrontWall(self):
        return self.walls[1] == "1"
    def setFrontWall(self, wall):
        self.walls[1] = wall

    # ------------------------------------------------right wall
    def hasRightWall(self):
        return self.walls[2] == "1" or self.walls[2] == 1
    def getRightWall(self):
        return self.walls[2] == "1"
    def setRightWall(self, wall):
        self.walls[2] = wall

    # ------------------------------------------------back wall
    def hasBackWall(self):
        return self.walls[3] == "1" or self.walls[3] == 1
    def getBackWall(self):
        return self.walls[3]
    def setBackWall(self, wall):
        self.walls[3] = wall

# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------distance
    def getRightDistance(self):
        return self.rightDistance
    def setRightDistance(self, distance):
        self.rightDistance = distance

    def getLeftDistance(self):
        return self.leftDistance
    def setLeftDistance(self, distance):
        self.leftDistance = distance
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------value
    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value
