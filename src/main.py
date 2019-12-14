import cv2
import numpy as np
import matplotlib as plt
from PIL import ImageGrab

def detect_bounds():
    grab = ImageGrab.grab()#bbox=(35,272,1825,1300)) #bbox=(x,y,width,height) from top-left
    window_grab=np.array(grab) #whole screen
    
    
    
    
    #cv2.imshow('result', window_grab)
    #cv2.waitKey(0)
    return

def make_coordinates(image, line_parameters):#converts from slope+intercept to x,y
    slope,intercept=line_parameters
    y1 = image.shape[0]#this gets the height parameter of the image
    y2 = int(y1*(3/5))#draw it to like 3/5ths of the screen 
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return np.array([x1,y1,x2,y2])

def average_slope_intercept(image,lines):
    left_fit=[]#cordinages of avg line on the left
    right_fit=[]#cordinates of avg line on the right
    left_line=np.array([0,0,0,0])
    right_line=np.array([0,0,0,0])

    if lines is not None:
        for line in lines:
            x1,y1,x2,y2=line.reshape(4)
            parameters = np.polyfit((x1,x2),(y1,y2),1) #fit a first degree polynomial mx+b to the lines given by coords
            slope=parameters[0]#slope is inverted as pixels are counted from left top corner
            intercept=parameters[1]
            if slope < 0:
                left_fit.append((slope,intercept))
            else:
                right_fit.append((slope,intercept))

    if left_fit:        
        left_fit_average=np.average(left_fit,axis=0)#axis specifies direction of averaging, down a row
        left_line=make_coordinates(image,left_fit_average)
    if right_fit:
        right_fit_average=np.average(right_fit,axis=0)
        right_line=make_coordinates(image,right_fit_average)
    return np.array([left_line,right_line])

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)#optional since canny does it inside, filtering out noise via weighted averaging pixels in locality 5x5 kernel 
    canny=cv2.Canny(blur,50,150)#works by detecting intensity changes (2D gradient/derivative), if a gradient is higher then high thresh than its edge, 
    #if lower than low thresh its not, and if in between its only edge if conncetd to strong edge, recomended 1 to 3 ratio
    return canny

def display_lines(image, lines):
    line_image=np.zeros_like(image) #same dimensions as image
    if lines is not None:
        for x1,y1,x2,y2 in lines:
            try:
                cv2.line(line_image, (x1,y1),(x2,y2),(255,0,0,),10)#draw lines for each set of cordinates in blue color 10p wide
            except:
                print(x1,y1,x2,y2)
    return line_image #just lines nothing else (zeros)

def region_of_interest(image):
    height = image.shape[0]
    width = image.shape[1]
    polygons = np.array([
        [(int(width/4),height),(int(3*width/4),height),(width/2,250)]#[(200,height),(1100,height),(550,250)]
        ], dtype=np.int64)
    mask = np.zeros_like(image)#array of zeros with the same dimensions as image (zero intensity/black)
    cv2.fillPoly(mask,polygons, 255)#create triangle of white 255 intensity 
    mask_image=cv2.bitwise_and(image, mask)
    return mask_image

# image = cv2.imread('img/test_image.jpg')
# lane_image = np.copy(image)
# cv.namedWindow('WarpAdjust')
# cv.createTrackbar('CannyLo', 'WarpAdjust' , 0, 500, pass)
# cv.createTrackbar('CannyHi', 'WarpAdjust' , 0, 500, pass)

detect_bounds()

# while True:
#     #grab image
#     grab = ImageGrab.grab(bbox=(35,272,1825,1300)) #bbox=(x,y,width,height) from top-left
#     lane_image= np.array(grab) 

#     canny_image = canny(lane_image)
#     cropped_image = region_of_interest(canny_image)
#     lines = cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)#first param is input, second and third params are resoultions of distance in pixels and angles in radians, 
#     #the larger res the more precision but slow. Current is 2 pixels and 1 degree for angles, fourth param is threshold for bin matches (min number of matches),fifth is placeholder array, 
#     #sixth is min lenght to be considered a line, seventh is max gap between segments to be unified into a line
#     averaged_lines=average_slope_intercept(lane_image,lines)
#     line_image=display_lines(lane_image,averaged_lines)
#     blended_image=cv2.addWeighted(lane_image,0.8,line_image,1,1) #weighted averge between images with respcetive proportions 20% more weight 
    
#     #output
#     resized_image=cv2.resize(cropped_image,(640,480))
#     cv2.imshow('result', resized_image)

#     if cv2.waitKey(1) & 0xFF == ord('q'):#use q key to quit, update frame
#         cv2.destroyWindow("Output")
#         break