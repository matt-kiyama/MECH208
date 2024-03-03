import cv2
import numpy as np

#0 is laptop cam 
#1 is usb camera
vid = cv2.VideoCapture(0)


#HSV
lower = np.array([110, 40, 170])
upper = np.array([165, 110, 255])

while(True):
# Capture the video frame 
    # by frame 
    ret, frame = vid.read() 

    if not ret:
        break

    # Create HSV Image and threshold into a range.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(frame, frame, mask= mask)

    # Display output image
    cv2.imshow('image',output)

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break  
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows()