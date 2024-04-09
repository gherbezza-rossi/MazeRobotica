import cv2
import pytesseract
import os
from PIL import Image
import numpy as np

cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(2)

img_counter = 0









def take_image_right():
	ret1, frame1 = cam1.read()
	if not ret1:
		print("failed to grab frame")
	else:
		img_name1 = "/home/sirio/Desktop/opencv_frame_right.png"
		cv2.imwrite(img_name1, frame1)
		print("written!")
          
def read_image_letter_right():
    bgr_img1 = cv2.imread("../opencv_frame_right.png")  # Load the image
    img_rotate = cv2.rotate(bgr_img1, cv2.ROTATE_180)
    img_name1 = "/home/sirio/Desktop/opencv_frame_right.png"
    cv2.imwrite(img_name1, img_rotate)
    gry_img1 = cv2.cvtColor(img_rotate, cv2.COLOR_BGR2GRAY)
    gry_img1 = cv2.bilateralFilter(gry_img1, 11, 17, 17)
    thresh1 = cv2.adaptiveThreshold(gry_img1, 255,
    cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10)
    border_img1 = cv2.copyMakeBorder(thresh1, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=255)
    cv2.imwrite("/home/sirio/Desktop/thresh_image_right.png", border_img1)
    txt1 = pytesseract.image_to_string(border_img1, config='--psm 6')
    print(txt1)

def find_square_shapes_right():
    img=cv2.imread("/home/sirio/Desktop/opencv_frame_right")
    hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower=np.array([0, 133, 98]) #0,133,98
    upper=np.array([179, 255, 255]) #179,255,255
    mask=cv2.inRange(hsv, lower, upper)
    cnts,hei=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cnts:
        area=cv2.contourArea(c)
        if area>2400:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            # Estrarre la regione di interesse
            roi = hsv[y:y+h, x:x+w]
            # Calcolare la media dei valori di colore nella regione di interesse
            avg_hue = np.mean(roi[:,:,0])
            if avg_hue >= 20 and avg_hue <= 40: # Giallo
                color = "Giallo"
            elif avg_hue >= 40 and avg_hue <= 80: # Verde
                color = "Verde"
            elif avg_hue >= 160 and avg_hue <= 180: # Rosso
                color = "Rosso"
            else:
                color = "Altro"
            return color

def close_camera_right():
	cam1.release()
	cv2.destroyAllWindows()
  

def take_image_left():
	ret2, frame2 = cam2.read()
	if not ret2:
		print("failed to grab frame")
	else:
		img_name2 = "/home/sirio/Desktop/opencv_frame_left.png"
		cv2.imwrite(img_name2, frame2)
		print("written!")
          
def read_image_letter_left():
    bgr_img2 = cv2.imread("/home/sirio/Desktop/opencv_frame_left.png")  # Load the image
    gry_img2 = cv2.cvtColor(bgr_img2, cv2.COLOR_BGR2GRAY)
    gry_img2 = cv2.bilateralFilter(gry_img2, 11, 17, 17)
    thresh2 = cv2.adaptiveThreshold(gry_img2, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    #border_img2 = cv2.copyMakeBorder(thresh2, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=255)
    cv2.imwrite("/home/sirio/Desktop/thresh_image_left.png", thresh2)
    txt2 = pytesseract.image_to_string(thresh2, config='--psm 6')
    print(txt2) 


def find_square_shapes_left():
    img=cv2.imread("/home/sirio/Desktop/opencv_frame_left.png")
    hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower=np.array([0, 133, 98]) #0,133,98
    upper=np.array([179, 255, 255]) #179,255,255
    mask=cv2.inRange(hsv, lower, upper)
    cnts,hei=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cnts:
        area=cv2.contourArea(c)
        if area>2400:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            # Estrarre la regione di interesse
            roi = hsv[y:y+h, x:x+w]
            # Calcolare la media dei valori di colore nella regione di interesse
            avg_hue = np.mean(roi[:,:,0])
            if avg_hue >= 20 and avg_hue <= 40: # Giallo
                color = "Giallo"
            elif avg_hue >= 40 and avg_hue <= 80: # Verde
                color = "Verde"
            elif avg_hue >= 160 and avg_hue <= 180: # Rosso
                color = "Rosso"
            else:
                color = "Altro"
            print("Colore:", color)


def close_camera_right():
	cam2.release()
	cv2.destroyAllWindows()

take_image_left()
read_image_letter_left()