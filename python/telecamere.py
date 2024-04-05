import cv2
import pytesseract
import os
import numpy as np

cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture(2)

img_counter = 0


def find_colored_square(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Definisci i range dei colori che vuoi rilevare (nel formato HSV)
    lower_bound = np.array([0, 50, 50])
    upper_bound = np.array([10, 255, 255])
    
    # Crea una maschera per isolare i colori nell'intervallo specificato
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Trova i contorni nell'immagine mascherata
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Cicla attraverso i contorni e controlla se c'è un quadrato
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        
        # Se l'approssimazione ha 4 lati, potrebbe essere un quadrato
        if len(approx) == 4:
            return True
    
    return False

def take_image_right():
    ret1, frame1 = cam1.read()
    if not ret1:
        print("Failed to grab frame")
        return None
    
    # Processa l'immagine come desiderato
    
    # Controlla se c'è un quadrato colorato
    if find_colored_square(frame1):
        print("Square detected in the right camera image")
    
    # Restituisci il testo rilevato
    return pytesseract.image_to_string(frame1, config='--psm 6')

def take_image_left():
    ret2, frame2 = cam2.read()
    if not ret2:
        print("Failed to grab frame")
        return None
    
    # Processa l'immagine come desiderato
    
    # Controlla se c'è un quadrato colorato
    if find_colored_square(frame2):
        print("Square detected in the left camera image")
    
    # Restituisci il testo rilevato
    return pytesseract.image_to_string(frame2 , config='--psm 6')

def close_camera_right():
	cam1.release()
	cv2.destroyAllWindows()

def close_camera_left():
	cam2.release()
	cv2.destroyAllWindows()
