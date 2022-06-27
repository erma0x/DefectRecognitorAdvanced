from importlib.resources import path
import sys
import cv2
import numpy as np

def empty(value):
    new_image = img.copy()
    new_image[:,:,2] = value
    cv2.imshow('img', new_image)


path_immagine = '\\data\\img\\examples\\logo2.png'

path_finale = sys.path[0].replace("\\tests\\trackbar","") + path_immagine

print("il path della tua immagine è : ",path_finale)

nome_trackbar = 'trackbar'
minimo_parametro = 0
massimo_parametro = 255

cv2.namedWindow(nome_trackbar)
#cv2.resizeWindow(nome_trackbar,640,240)

cv2.createTrackbar('h_min',nome_trackbar, 0, 255, empty)
cv2.createTrackbar('h_max',nome_trackbar, 255, 255, empty)
cv2.createTrackbar('s_min',nome_trackbar, 0, 255, empty)
cv2.createTrackbar('s_max',nome_trackbar, 255, 255, empty)
cv2.createTrackbar('v_min',nome_trackbar, 0, 255, empty)
cv2.createTrackbar('v_max',nome_trackbar, 255, 255, empty)


while True:
    img = cv2.imread(path_finale)
    
    h_min = cv2.getTrackbarPos('h_min',nome_trackbar)
    h_max = cv2.getTrackbarPos('h_max',nome_trackbar)
    s_min = cv2.getTrackbarPos('s_min',nome_trackbar)
    s_max = cv2.getTrackbarPos('s_max',nome_trackbar)
    v_min = cv2.getTrackbarPos('v_min',nome_trackbar)
    v_max = cv2.getTrackbarPos('v_max',nome_trackbar)

    lower_bands = np.array([h_min,s_min,v_min]) 
    upper_bands = np.array([h_max,s_max,v_max]) 

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV, lower_bands, upper_bands)

    img_final = cv2.bitwise_and(imgHSV,imgHSV,mask)

    cv2.imshow('original',img)
    cv2.imshow('img',img_final)

    cv2.waitKey(1)
