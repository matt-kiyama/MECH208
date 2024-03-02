import numpy as np 
import cv2 as cv
import time

#Initialize the capture 
cap = cv.VideoCapture(1)

def ballFinder(cap):
    ret, frame = cap.read() 
    result = (0,0,0)
    if ret:
        #frame = frame[:, 93:550, :]
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        lower_value = np.array([00,80,100])
        higher_value = np.array([50,255,255])
        mask = cv.inRange(hsv, lower_value, higher_value)
        mask = cv.blur(mask,(6,6))                        
        mask = cv.erode(mask, None, iterations=2)         
        mask = cv.dilate(mask, None, iterations=2)        
        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > 1500:
                (x,y), radius = cv.minEnclosingCircle(cnt)
                x = int(x)
                y = 480 - int(y) #In images, y=0 is on top, not on the bottom 
                radius = int(radius)
                if radius > 20:
                    result = (x,y,radius)
    return(result)

while True:
    ret, frame = cap.read()
    #cv.imshow('frame', frame)
    x,y,radius = ballFinder(cap)
    cv.circle(frame, (x,y), radius, (0,100,100), 3)
    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'): 
        break      
# After the loop release the cap object 
cap.release() 
# Destroy all the windows 
cv.destroyAllWindows()


# while True:
#     ret, frame = cap.read() 
#     cv.imshow('frame', frame)
#     result = (0,0)
#     if ret:
#         frame = frame[:, 93:550, :]
#         hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
#         lower_value = np.array([00,80,100])
#         higher_value = np.array([50,255,255])
#         mask = cv.inRange(hsv, lower_value, higher_value)
#         mask = cv.blur(mask,(6,6))                        
#         mask = cv.erode(mask, None, iterations=2)         
#         mask = cv.dilate(mask, None, iterations=2)        
#         contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
#         for cnt in contours:
#             area = cv.contourArea(cnt)
#             if area > 1500:
#                 (x,y), radius = cv.minEnclosingCircle(cnt)
#                 x = int(x)
#                 y = 480 - int(y) #In images, y=0 is on top, not on the bottom 
#                 radius = int(radius)
#                 if radius > 20:
#                     result = (x,y)
#     cv.circle(frame, (x,y), radius, (0,100,100), 3)
#     cv.imshow('frame', frame)   

#     if cv.waitKey(1) & 0xFF == ord('q'): 
#         break      

# # After the loop release the cap object 
# cap.release() 
# # Destroy all the windows 
# cv.destroyAllWindows()