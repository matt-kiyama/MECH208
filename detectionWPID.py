import cv2
import numpy as np
import time

prevCircle = None
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2

square_center_x = None
square_center_y = None
circle_center_x = None
circle_center_y = None
w = None

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
        #print(circles)
        chosen = None
        for i in circles[0, :]:
            if chosen is None: chosen = i
            if prevCircle is not None:
                if dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) <= dist(i[0], i[1], prevCircle[0], prevCircle[1]):
                    chosen = i
        cv2.circle(frame, (chosen[0], chosen[1]), 1, (0,100,100), 3)
        cv2.circle(frame, (chosen[0], chosen[1]), chosen[2], (255,0,255), 3)

        center = (chosen[0], chosen[1])
        radius = chosen[2]

        prevCircle = chosen

        return center, radius
    else:
        return None


def detect_square(frame, min_area, max_area):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help with contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Canny edge detector to find edges in the image
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through the contours
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # If the polygon has 4 vertices, it is a rectangle
        if len(approx) == 4:
            # Calculate the aspect ratio of the rectangle
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h

            # Define a threshold for aspect ratio to consider it a square
            aspect_ratio_threshold = 0.9  # Adjust as needed

            if 1 - aspect_ratio_threshold < aspect_ratio < 1 + aspect_ratio_threshold:
                # Calculate the area of the rectangle
                area = cv2.contourArea(approx)

                # Check if the area is within the specified range
                if min_area < area < max_area:
                    # Draw the rectangle on the original frame
                    cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)

                    # Calculate the center of the square
                    center_x = x + w // 2
                    center_y = y + h // 2
                    center = [center_x, center_y]

                    return center

    # Return None if no square is detected
    return None

def getErrors(xy_1, xy_2):
    x1, y1 = xy_1
    x2, y2 = xy_2
    error = dist(x1, y1, x2, y2)
    return error

class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain

        self.prev_error = 0  # Previous error for derivative term
        self.integral = 0  # Accumulated error for integral term

    def update(self, error):
        # Proportional term
        p_term = self.kp * error

        # Integral term
        self.integral += error
        i_term = self.ki * self.integral

        # Derivative term
        d_term = self.kd * (error - self.prev_error)
        self.prev_error = error

        # PID control output
        pid_output = p_term + i_term + d_term

        return pid_output

#initialize instance of PID class
pid = PIDController(kp=0.5, ki=0.1, kd=0.2)

# Open a video capture object (you can replace '0' with the video file name)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video feed
    ret, frame = cap.read()

    # Break the loop if no frame is captured
    if not ret:
        break

    # Detect squares in the current frame
    square_result = detect_square(frame, min_area=200, max_area=15000)

    # Detect circle in the current frame
    circle_result = detect_ball(frame)

    # Display the result
    if square_result is not None:
        square_center = square_result
        square_center_x, square_center_y = square_center
        print(f"Set point coordinates: ({square_center_x}, {square_center_y})", end="")
    else:
        print(f"Set point coordinates: ({None}, {None})", end="")

    if circle_result is not None: 
        circle_center, circle_radius = circle_result
        circle_center_x, circle_center_y = circle_center
        print(f" Ball coordinates: ({circle_center_x}, {circle_center_y}, {circle_radius})", end="")
    else:
        print(f" Ball coordinates: ({None}, {None}, {None})", end="")

    if square_result is not None and circle_result is not None:
        center_error = getErrors(square_center, circle_center)
        print(f" Center Error:", center_error)
        control_output = pid.update(center_error)   
        print(f" Control Output:", control_output)
        print()
    else:
        print(f" Center Error:", None)

    cv2.imshow('Square and Circle Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()

