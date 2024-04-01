from MazeClass import Maze
user_input = input("hai rimosso il cavo del sensore colori? (yes/no): ")
if user_input.lower() in ["yes", "no"]:
    print("settaggio tof")
    from python.tof import *
    user_input = input("hai ricollegato il sensore? (yes/no): ")
    if user_input.lower() in ["yes", "no"]:
        print("settaggio sensore colori")
       # from python.color_sensor import *
        print("settaggio telecamere")
        from python.telecamere import *
        from python.led_control import *




else:
    print("Exiting...")

def start():  
  myMaze = Maze()

  first = True
        
  while True:
      dati_tof=detect_walls()
      print(dati_tof)
      dati = dati_tof.split()
      left=dati[0]
      front=dati[1]
      right=dati[3]

      walls = [left, front, right, 0]        # walls = [left, front, right, back]
      if first:
          walls[3] = 1
          first = False
      print("muri")
      print(walls)
      right_distance = dati[4]
      left_distance = dati[5]
      
      # ----------------------------  altre cose che deve fare robot ---------------------------------
      
      dati_camera1 = take_image1()
      close_camera1()
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
      dati_camera2 = take_image2()
      close_camera2()
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
      
      
      myMaze.addBlockData(walls)
      myMaze.assignNumber()

      print("this is the general function that represents the algorithm that makes the robot move")

      print("as first it checks if there is any empty \"rooms\" in the right or left of the robot")
      print(right_distance, left_distance)
      print(myMaze.orientation)
      myMaze.theFirstFunctionDISTANCE(right_distance, left_distance)
      print(myMaze.orientation)

      print("it follows the right rule")
      myMaze.RR()

start()
