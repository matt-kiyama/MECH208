import cv2
import numpy as np
import time
import serial

prevCircle = None
prevSquare = None
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2

square_center_x = None
square_center_y = None
circle_center_x = None
circle_center_y = None
w = None

port = "/dev/ttyACM1"
baud = 115200
ser = serial.Serial(port, baud, write_timeout=0)
update_rate = 2 #in ms

prev_time = time.time()

def moving_average(data, window_size):
    """
    Calculate the moving average of a given data set and return a single value.

    Parameters:
        data (array-like): The input data.
        window_size (int): The size of the moving window.

    Returns:
        float: The average of the moving averages.
    """
    # Convert data to numpy array
    data = np.array(data)
    
    # Pad the data to handle edges
    padded_data = np.pad(data, (window_size-1, 0), mode='constant', constant_values=np.nan)
    
    # Calculate the moving averages
    moving_averages = np.convolve(padded_data, np.ones(window_size)/window_size, mode='valid')
    
    # Calculate the average of the moving averages
    average_of_moving_averages = np.mean(moving_averages)
    
    return average_of_moving_averages

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
    return prevSquare

def getErrors(xy_1, xy_2):
    x1, y1 = xy_1
    x2, y2 = xy_2
    error = dist(x1, y1, x2, y2)
    return error

def getErrorInX(x1,  x2):
    return x2 - x1

def moveFans(control_value, serial, stop):
    global base_value
    global min_value
    global max_value
    global prev_time
    global update_rate
    global bias_coef

    pwm_l = base_value - control_value
    pwm_r = base_value + control_value

    #bias compensation
    pwm_r = pwm_r * bias_coef
    pwm_l = pwm_l * 0.836
    #pwm_l = pwm_l * bias_coef

    #limit check
    if(pwm_l < min_value):
        pwm_l = min_value
    if(pwm_l > max_value):
        pwm_l = max_value    
    
    if(pwm_r < min_value):
        pwm_r = min_value
    if(pwm_r > max_value):
        pwm_r = max_value

    #control_string = str(pwm_l) + " " + str(pwm_r) + "\n"
    control_string = str(pwm_r) + " " + str(pwm_l) + "\n"
    
    print(control_string)
    milliseconds_elapsed = (time.time() - prev_time) * 1000
    print("millis " + str(milliseconds_elapsed)+ "\n")
    if(milliseconds_elapsed > update_rate):
        print(str(update_rate) + " elapsed\n")
        serial.write(control_string.encode('utf-8'))
        #ser.write(control_string.encode('utf-8'))
        prev_time = time.time()
    
    if(stop):
        control_string = str(0) + " " + str(0) + "\n"
        serial.write(control_string.encode('utf-8'))


class PIDController:
    def __init__(self, kp, ki, kd, update_rate):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.update_rate = update_rate

        self.prev_error = 0  # Previous error for derivative term
        self.integral = 0  # Accumulated error for integral term

    def update(self, error, deadZoneMin, deadZoneMax):
        # Proportional term
        p_term = self.kp * error

        # Integral term
        if(deadZoneMin < error < deadZoneMax ):
            self.integral = self.integral + (error * 10)
        #self.integral += error*self.update_rate    
        i_term = self.ki * self.integral

        # Derivative term
        derivative = (error - self.prev_error) / 20
        #derivative = (error - self.prev_error) / self.update_rate
        d_term = self.kd * derivative
        self.prev_error = error

        # PID control output
        print("P Term: " + str(p_term) + "\n")
        print("I Term: " + str(i_term) + "\n")
        print("D Term: " + str(d_term) + "\n")
        #pid_output = p_term + d_term
        pid_output = p_term + i_term + d_term

        return pid_output

# #initialize instance of PID class
# pid = PIDController(kp=0.033, ki=0.00001, kd=3.235, update_rate=update_rate) 
# #pid = PIDController(kp=0.028, ki=0.00001, kd=3.25, update_rate=update_rate) 
# min_value = 50
# base_value = 65
# max_value = 75
# bias_coef = 1
    
#initialize instance of PID class
pid = PIDController(kp=0.045, ki=0.000013, kd=3.219, update_rate=update_rate) 
#pid = PIDController(kp=0.028, ki=0.00001, kd=3.25, update_rate=update_rate) 
min_value = 55
base_value = 65
max_value = 75
bias_coef = 0.835

#if error is within this pixel count then don't add to steady state
pid_deadZone_min = -55
pid_deadZone_max = 55

# Open a video capture object (you can replace '0' with the video file name)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video feed
    ret, frame = cap.read()

    # Break the loop if no frame is captured
    if not ret:
        break

    # Detect squares in the current frame
    square_result = detect_square(frame, min_area=550, max_area=2500)

    # Detect circle in the current frame
    circle_result = detect_ball(frame)

    # Display the result
    if square_result is not None:
        square_center = square_result
        square_center_x, square_center_y = square_center
        #print(f"Set point coordinates: ({square_center_x}, {square_center_y})", end="")
    else:
        pass
        #print(f"Set point coordinates: ({None}, {None})", end="")

    if circle_result is not None: 
        circle_center, circle_radius = circle_result
        circle_center_x, circle_center_y = circle_center
        #print(f" Ball coordinates: ({circle_center_x}, {circle_center_y}, {circle_radius})", end="")
    else:
        pass
        #print(f" Ball coordinates: ({None}, {None}, {None})", end="")

    if square_result is not None and circle_result is not None:
        center_error = getErrors(square_center, circle_center)
        center_error_x = getErrorInX(square_center_x, circle_center_x)
        #center_error_x_avg = moving_average(center_error_x, 5)
        print(f" Center Error X:", center_error_x)
        #print(f" Center Error:", center_error)
        control_output = pid.update(center_error_x, pid_deadZone_min, pid_deadZone_max)   
        #print(f"Control Output:", control_output)
        #print()
        moveFans(control_output, ser, stop=False)
        #moveFans(0, ser, stop=False)
        #print()
    else:
        pass
        #print(f" Center Error:", None)

    cv2.imshow('Square and Circle Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        moveFans(0, ser, stop=True)
        break

# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()

