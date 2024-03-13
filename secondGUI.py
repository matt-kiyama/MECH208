import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import detectionWPID as detection
import serial

class ThirdWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("PID Control and Video Feed")

        # Initialize PID controller and other parameters
        self.pid = detection.PIDController(kp=0.05, ki=0.1, kd=0.2)
        self.min_value = 40
        self.base_value = 50
        self.max_value = 60
        self.pid_deadZone_min = -20
        self.pid_deadZone_max = 20

        # Open a video capture object (you can replace '0' with the video file name)
        self.cap = cv2.VideoCapture(0)

        self.port = "/dev/ttyACM1"
        self.baud = 115200
        self.serial = serial.Serial(self.port, self.baud, write_timeout=0)

        # Create sliders
        self.create_sliders()

        # Create canvas for video feed
        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        # Schedule the loop method and slider update method to be called after a delay
        self.root.after(10, self.run_loop)
        self.root.after(100, self.update_sliders)

    def create_sliders(self):
        # Create and configure sliders
        self.slider_var1 = tk.DoubleVar(value=self.base_value)
        slider1 = ttk.Scale(self.root, from_=self.min_value, to=self.max_value, orient="horizontal", length=200, variable=self.slider_var1, command=self.update_slider)
        slider1.pack(pady=10)

        self.slider_var2 = tk.DoubleVar(value=self.base_value)
        slider2 = ttk.Scale(self.root, from_=self.min_value, to=self.max_value, orient="horizontal", length=200, variable=self.slider_var2, command=self.update_slider)
        slider2.pack(pady=10)

        self.slider_var3 = tk.DoubleVar(value=self.base_value)
        slider3 = ttk.Scale(self.root, from_=self.min_value, to=self.max_value, orient="horizontal", length=200, variable=self.slider_var3, command=self.update_slider)
        slider3.pack(pady=10)

    def update_slider(self, *args):
        # You can add custom logic here if needed
        pass

    def update_sliders(self):
        # Update sliders
        self.slider_var1.set(self.base_value)  # Update with actual values if needed
        self.slider_var2.set(self.base_value)
        self.slider_var3.set(self.base_value)

        # Schedule the update_sliders method to be called after a delay
        self.root.after(100, self.update_sliders)

    def run_loop(self):
        # Read a frame from the video feed
        ret, frame = self.cap.read()

        # Break the loop if no frame is captured
        if not ret:
            return

        # Detect squares in the current frame
        square_result = detection.detect_square(frame, min_area=800, max_area=2500)

        # Detect circle in the current frame
        circle_result = detection.detect_ball(frame)

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
            center_error = detection.getErrors(square_center, circle_center)
            center_error_x = detection.getErrorInX(square_center_x, circle_center_x)
            print(f" Center Error X:", center_error_x)
            control_output = self.pid.update(center_error_x, self.pid_deadZone_min, self.pid_deadZone_max)
            print(f" Control Output:", control_output)
            detection.moveFans(control_output, self.serial)
            print()
        else:
            print(f" Center Error:", None)

        # Convert OpenCV image to Tkinter-compatible format
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)

        # Update the canvas with the new image
        self.canvas.config(width=img.width(), height=img.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.img = img

        # Schedule the run_loop method to be called after a delay
        self.root.after(10, self.run_loop)

# Include the necessary detect_square, detect_ball, getErrors, getErrorInX, and moveFans functions here

# Create an instance of the ThirdWindow class
if __name__ == "__main__":
    root = tk.Tk()
    app = ThirdWindow(root)
    root.mainloop()

# Release the video capture object when the application is closed
app.cap.release()
cv2.destroyAllWindows()
