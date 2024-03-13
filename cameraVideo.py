import cv2
import numpy as np

#0 is laptop cam 
#1 is usb camera
vid = cv2.VideoCapture(4)

#in BGR
upper_orange = (100, 250, 252)
lower_orange = (3, 219, 252)

red_lower = [17, 15, 100]
red_upper = [50, 56, 200]

white_upper = [255, 255, 255]
white_lower = [150, 150, 150]

while(True):
# Capture the video frame 
    # by frame 
    ret, frame = vid.read() 
  
    lower = np.array(white_lower, dtype = "uint8")
    upper = np.array(white_upper, dtype = "uint8")

    mask = cv2.inRange(frame, lower, upper)
    output = cv2.bitwise_and(frame, frame, mask = mask)

    cv2.imshow("images", np.hstack([frame, output]))

    # Display the resulting frame 
    #cv2.imshow('frame', frame) 
      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 