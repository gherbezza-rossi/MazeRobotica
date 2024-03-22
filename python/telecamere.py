import cv2
import pytesseract
import os

cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(2)

img_counter = 0

def take_image1():
	ret1, frame1 = cam1.read()
	if not ret1:
		print("failed to grab frame")
	else:
		img_name1 = "/home/sirio/Desktop/opencv_frame1.png"
		cv2.imwrite(img_name1, frame1)
		print("written!")
		bgr_img1 = cv2.imread("/home/sirio/Desktop/opencv_frame1.png")  # Load the image
		img_rotate = cv2.rotate(bgr_img1, cv2.ROTATE_180)
		img_name1 = "/home/sirio/Desktop/opencv_frame1.png"
		cv2.imwrite(img_name1, img_rotate)
		gry_img1 = cv2.cvtColor(img_rotate, cv2.COLOR_BGR2GRAY)
		gry_img1 = cv2.bilateralFilter(gry_img1, 11, 17, 17)
		thresh1 = cv2.adaptiveThreshold(gry_img1, 255,
		cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)
		border_img1 = cv2.copyMakeBorder(thresh1, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=255)
		cv2.imwrite("/home/sirio/Desktop/thresh_image1.png", border_img1)
		txt1 = pytesseract.image_to_string(border_img1, config='--psm 6')
		return(txt1)
  
  
def take_image2():
	ret2, frame2 = cam2.read()
	if not ret2:
		print("failed to grab frame")
	else:
		img_name2 = "/home/sirio/Desktop/opencv_frame2.png"
		cv2.imwrite(img_name2, frame2)
		print("written!")
		bgr_img2 = cv2.imread("/home/sirio/Desktop/opencv_frame2.png")  # Load the image
		gry_img2 = cv2.cvtColor(bgr_img2, cv2.COLOR_BGR2GRAY)
		gry_img2 = cv2.bilateralFilter(gry_img2, 11, 17, 17)
		thresh2 = cv2.adaptiveThreshold(gry_img2, 255,
		cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)
		border_img2 = cv2.copyMakeBorder(thresh2, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=255)
		cv2.imwrite("/home/sirio/Desktop/thresh_image2.png", border_img2)
		txt2 = pytesseract.image_to_string(border_img2, config='--psm 6')
		return(txt2) 

def close_camera1():
	cam1.release()
	cv2.destroyAllWindows()

def close_camera2():
	cam2.release()
	cv2.destroyAllWindows()