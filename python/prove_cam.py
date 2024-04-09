import cv2
import numpy as np

def empty(img):
    pass

video = cv2.VideoCapture(2)

cv2.namedWindow("TrackBar")
cv2.resizeWindow("TrackBar", 600, 300)
cv2.createTrackbar("hue_min", "TrackBar",0,179,empty)
cv2.createTrackbar("hue_max", "TrackBar",179,179,empty)
cv2.createTrackbar("sat_min", "TrackBar",0,255,empty)
cv2.createTrackbar("sat_max", "TrackBar",255,255,empty)
cv2.createTrackbar("val_min", "TrackBar",0,255,empty)
cv2.createTrackbar("val_max", "TrackBar",255,255,empty)

while True:
    ret,img = video.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue_min = cv2.getTrackbarPos("hue_min", "TrackBar")
    hue_max = cv2.getTrackbarPos("hue_max", "TrackBar")
    sat_min = cv2.getTrackbarPos("sat_min", "TrackBar")
    sat_max = cv2.getTrackbarPos("sat_max", "TrackBar")
    val_min = cv2.getTrackbarPos("val_min", "TrackBar")
    val_max = cv2.getTrackbarPos("val_max", "TrackBar")
    lower = np.array([hue_min, sat_min, val_min])
    upper = np.array([hue_max, sat_max, val_max])
    mask = cv2.inRange(hsv, lower, upper)
    cnts, hei = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 300:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Estrarre la regione di interesse
            roi = hsv[y:y+h, x:x+w]
            # Calcolare la media dei valori di colore nella regione di interesse
            avg_hue = np.mean(roi[:,:,0])
            avg_sat = np.mean(roi[:,:,1])
            avg_val = np.mean(roi[:,:,2])
            print("Average Hue:", avg_hue)
            print("Average Saturation:", avg_sat)
            print("Average Value:", avg_val)
    cv2.imshow("Frame", img)
    cv2.imshow("hsv",hsv)
    cv2.imshow("mask",mask)
    k=cv2.waitKey(1)
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()