import cv2 as cv
import numpy as np

#0 is laptop cam 
#1 is usb camera
vid = cv.VideoCapture(0)


#HSV
lower = np.array([41, 24, 55])
upper = np.array([165, 92, 129])

def ballFinder(cap):
    ret, frame = cap.read() 
    result = (0,0,0)
    if ret:
        #frame = frame[:, 93:550, :]
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        #mask = cv.inRange(hsv, lower_white, higher_white)
        mask = cv.inRange(hsv, lower, upper)
        mask = cv.blur(mask,(6,6))                        
        mask = cv.erode(mask, None, iterations=2)         
        mask = cv.dilate(mask, None, iterations=2)        
        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > 200:
                (x,y), radius = cv.minEnclosingCircle(cnt)
                x = int(x)
                y = 480 - int(y) #In images, y=0 is on top, not on the bottom 
                radius = int(radius)
                if radius > 20:
                    result = (x,y,radius)
    return(result)

while True:
    ret, frame = vid.read()
    #cv.imshow('frame', frame)
    x,y,radius = ballFinder(vid)
    cv.circle(frame, (x,y), radius, (0,100,100), 3)
    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'): 
        break      
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv.destroyAllWindows()


# while(True):
# # Capture the video frame 
#     # by frame 
#     ret, frame = vid.read() 

#     if not ret:
#         break

#     # Create HSV Image and threshold into a range.
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     mask = cv2.inRange(hsv, lower, upper)
#     output = cv2.bitwise_and(frame, frame, mask= mask)

#     # Display output image
#     cv2.imshow('image',output)

#     if cv2.waitKey(1) & 0xFF == ord('q'): 
#         break  
# # After the loop release the cap object 
# vid.release() 
# # Destroy all the windows 
# cv2.destroyAllWindows()