from PIL import ImageGrab
import numpy as np
import cv2 as cv
import pyautogui #used to get coordinates of screengrab for now

#util function to silence trackbar updates
def nothing(x):
    return


#create trackbar window
alpha=900
beta=1200
alpha_slider_max = 2000
cv.namedWindow('WarpAdjust')
cv.createTrackbar('UpperLimit', 'WarpAdjust' , 0, alpha_slider_max, nothing)
cv.createTrackbar('LowerLimit', 'WarpAdjust' , 0, alpha_slider_max, nothing)
cv.createTrackbar('UpperWidth', 'WarpAdjust' , 0, alpha_slider_max, nothing)
cv.createTrackbar('LowerWidth', 'WarpAdjust' , 0, alpha_slider_max, nothing)

while True:
    #grab image
    grab = ImageGrab.grab(bbox=(35,272,1825,1300)) #bbox=(x,y,width,height) from top-left
    orig_img= np.array(grab) 

    #warp into a more favorible perspective
    alpha=cv.getTrackbarPos('UpperLimit','WarpAdjust')
    beta=cv.getTrackbarPos('LowerLimit','WarpAdjust')
    gamma=cv.getTrackbarPos('UpperWidth','WarpAdjust')
    theta=cv.getTrackbarPos('LowerWidth','WarpAdjust')
    pts1 = np.float32([[(1825/2)-(gamma/2),alpha],[(1825/2)+(gamma/2),alpha],[(1825/2)-(theta/2),beta],[(1825/2)+(theta/2),beta]])
    pts2 = np.float32([[0,0],[912,0],[0,650],[912,650]])
    M = cv.getPerspectiveTransform(pts1,pts2)#creates Transf. matrix
    warp_img = cv.warpPerspective(orig_img,M,(912,650))

    # Convert the img to grayscale 
    gray = cv.cvtColor(warp_img,cv.COLOR_BGR2GRAY) 
    
    # Apply edge detection method on the image 
    edges = cv.Canny(gray,50,150,apertureSize = 3) 
    
    # This returns an array of r and theta values 
    lines = cv.HoughLines(edges,1,np.pi/180, 200) 
    
    if lines is not None:
        # The below for loop runs till r and theta values  
        # are in the range of the 2d array 
        for r,theta in lines[0]: 
            
            # Stores the value of cos(theta) in a 
            a = np.cos(theta) 
        
            # Stores the value of sin(theta) in b 
            b = np.sin(theta) 
            
            # x0 stores the value rcos(theta) 
            x0 = a*r 
            
            # y0 stores the value rsin(theta) 
            y0 = b*r 
            
            # x1 stores the rounded off value of (rcos(theta)-1000sin(theta)) 
            x1 = int(x0 + 1000*(-b)) 
            
            # y1 stores the rounded off value of (rsin(theta)+1000cos(theta)) 
            y1 = int(y0 + 1000*(a)) 
        
            # x2 stores the rounded off value of (rcos(theta)+1000sin(theta)) 
            x2 = int(x0 - 1000*(-b)) 
            
            # y2 stores the rounded off value of (rsin(theta)-1000cos(theta)) 
            y2 = int(y0 - 1000*(a)) 
            
            # cv2.line draws a line in img from the point(x1,y1) to (x2,y2). 
            # (0,0,255) denotes the colour of the line to be  
            #drawn. In this case, it is red.  
            cv.line(warp_img,(x1,y1), (x2,y2), (0,0,255),2) 

    cv.imshow("Output", warp_img)
    #pyautogui.displayMousePosition()
    if cv.waitKey(1) & 0xFF == ord('q'):#use q key to quit, update frame
        cv.destroyWindow("Output")
        break

