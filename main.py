from MazeClass import *


myMaze = Maze()

    
        



def start(first):
    walls, dati = myMaze.getValues(first)

    right_distance = dati[4]
    left_distance = dati[5] 

  #-------------------------------------------------------------------------------------------------
    print("fn start")
    print("distances[r, l]: ", right_distance, left_distance)
    print("orientation: ", myMaze.orientation)
    myMaze.emptyRoomsFinding(right_distance, left_distance)
    myMaze.RR()