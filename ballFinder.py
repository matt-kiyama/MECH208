import cv2
import numpy as np

#0 is laptop cam 
#1 is usb camera
vid = cv2.VideoCapture(0)
prevCircle = None
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2

def detect_ball(frame):
    global prevCircle, dist

    #gray and blur normal color video frame
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(grayFrame, (13,13), 0)  #larger odd intergers = more blur
  

    # Display the resulting frame 
    #cv2.imshow('frame', frame) 
    #cv2.imshow('blurframe', blurFrame) 

    #returns a list of circles
    circles = cv2.HoughCircles(blurFrame, cv2.HOUGH_GRADIENT, 1, 100, param1 = 100, param2 = 30, minRadius = 0, maxRadius = 100)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        print(circles)
        chosen = None
        for i in circles[0, :]:
            if chosen is None: chosen = i
            if prevCircle is not None:
                if dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) <= dist(i[0], i[1], prevCircle[0], prevCircle[1]):
                    chosen = i
        center, radius = get_circle_info(chosen)
        cv2.circle(frame, (chosen[0], chosen[1]), 1, (0,100,100), 3)
        cv2.circle(frame, (chosen[0], chosen[1]), chosen[2], (255,0,255), 3)
        prevCircle = chosen
        return chosen

def get_circle_info(circle):
    center = (circle[0], circle[1])
    radius = circle[2]
    return center, radius

while(True):
# Capture the video frame 
    # by frame 
    ret, frame = vid.read() 

    if not ret:
        break


    center, radius = detect_ball(frame)
    print(f"Circle Info: ({center}, {radius})")
    
    cv2.imshow("circles", frame)
      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 