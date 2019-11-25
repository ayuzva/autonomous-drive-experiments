from PIL import ImageGrab
import numpy as np
import cv2 as cv
import pyautogui #used to get coordinates of screengrab, more elegant solution in future
def nothing(x):
    return()
alpha=900
beta=1200

alpha_slider_max = 2000
title_window = 'WarpTesting'
cv.namedWindow(title_window)
cv.createTrackbar('UpperLimit', title_window , 0, alpha_slider_max, nothing)
cv.createTrackbar('LowerLimit', title_window , 0, alpha_slider_max, nothing)
cv.createTrackbar('UpperWidth', title_window , 0, alpha_slider_max, nothing)
cv.createTrackbar('LowerWidth', title_window , 0, alpha_slider_max, nothing)

#(bbox= x,y,width,height *starts top-left)

while True:
    alpha=cv.getTrackbarPos('UpperLimit','WarpTesting')
    beta=cv.getTrackbarPos('LowerLimit','WarpTesting')
    gamma=cv.getTrackbarPos('UpperWidth','WarpTesting')
    theta=cv.getTrackbarPos('LowerWidth','WarpTesting')
    #frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    img = ImageGrab.grab(bbox=(35,272,1825,1300)) #bbox specifies specific region (bbox= x,y,width,height *starts top-left)
    frame = np.array(img) #this is the array obtained from conversion
    pts1 = np.float32([[(1825/2)-(gamma/2),alpha],[(1825/2)+(gamma/2),alpha],[(1825/2)-(theta/2),beta],[(1825/2)+(theta/2),beta]])
    pts2 = np.float32([[0,0],[1000,0],[0,1000],[1000,1000]])
    M = cv.getPerspectiveTransform(pts1,pts2)
    dst = cv.warpPerspective(frame,M,(1000,1000))
    cv.imshow("ScreenGrab", dst)
    #pyautogui.displayMousePosition()
    if cv.waitKey(1) & 0xFF == ord('q'):#use q key to quit
        cv.destroyWindow("ScreenGrab")
        break

