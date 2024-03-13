import tkinter as tk
from tkinter import ttk
import detectionWPID as detection
import cv2
import serial
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Window")

        self.label = ttk.Label(root, text="Main Window Content")
        self.label.pack(padx=20, pady=20)

        self.open_button = ttk.Button(root, text="Open Second Window", command=self.open_second_window)
        self.open_button.pack(pady=10)

        self.port = "/dev/ttyACM1"
        self.baud = 115200
        self.ser = serial.Serial(self.port, self.baud, write_timeout=0)

        #initialize 2 instances of PID class
        self.pid = detection.PIDController(kp=0.05, ki=0.1, kd=0.2)
        self.min_value = 40
        self.base_value = 50
        self.max_value = 60

        #if error is within this pixel count then don't add to steady state
        self.pid_deadZone_min = -20
        self.pid_deadZone_max = 20

        # Open a video capture object (you can replace '0' with the video file name)
        self.cap = cv2.VideoCapture(0)

    def open_second_window(self):
        self.second_window = tk.Toplevel(self.root)
        self.second_window.title("Second Window")

        self.second_label = ttk.Label(self.second_window, text="Second Window Content")
        self.second_label.pack(padx=20, pady=20)

        self.close_button = ttk.Button(self.second_window, text="Close Second Window", command=self.close_second_window)
        self.close_button.pack(pady=10)

    def close_second_window(self):
        self.second_window.destroy()

class ThirdWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("PID GUI")

        # Create sliders
        self.create_sliders()

        # Schedule the loop method to be called after a delay
        self.root.after(10, self.run_loop)

        self.root.after(100, self.update_sliders)
    
    def create_sliders(self):
        # Slider 1
        label1 = ttk.Label(root, text="Slider 1:")
        label1.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.var1 = tk.DoubleVar()
        slider1 = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=200, variable=self.var1, command=lambda x: self.update_textbox_value(slider1, self.var1))
        slider1.grid(row=0, column=1, padx=5, pady=5)
        textbox1 = ttk.Entry(root, textvariable=self.var1, width=10)
        textbox1.grid(row=0, column=2, padx=5, pady=5)
        self.update_textbox_value(slider1, self.var1)

        # Slider 2
        label2 = ttk.Label(root, text="Slider 2:")
        label2.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.var2 = tk.DoubleVar()
        slider2 = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=200, variable=self.var2, command=lambda x: self.update_textbox_value(slider2, self.var2))
        slider2.grid(row=1, column=1, padx=5, pady=5)
        textbox2 = ttk.Entry(root, textvariable=self.var2, width=10)
        textbox2.grid(row=1, column=2, padx=5, pady=5)
        self.update_textbox_value(slider2, self.var2)

        # Slider 3
        label3 = ttk.Label(root, text="Slider 3:")
        label3.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.var3 = tk.DoubleVar()
        slider3 = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=200, variable=self.var3, command=lambda x: self.update_textbox_value(slider3, self.var3))
        slider3.grid(row=2, column=1, padx=5, pady=5)
        textbox3 = ttk.Entry(root, textvariable=self.var3, width=10)
        textbox3.grid(row=2, column=2, padx=5, pady=5)
        self.update_textbox_value(slider3, self.var3)

        # Submit button
        submit_button = ttk.Button(root, text="Submit", command=self.submit_values)
        submit_button.grid(row=3, column=0, columnspan=3, pady=10)

    def update_textbox_value(self, slider, text_var):
        text_var.set(slider.get())

    def submit_values(self):
        value1 = self.var1.get()
        value2 = self.var2.get()
        value3 = self.var3.get()

        # Do something with the values, e.g., print them
        print("Slider 1:", value1)
        print("Slider 2:", value2)
        print("Slider 3:", value3)
    
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
            #print(f" Center Error:", center_error)
            control_output = detection.pid.update(center_error_x, self.pid_deadZone_min, self.pid_deadZone_max)   
            print(f" Control Output:", control_output)
            detection.moveFans(control_output, self.ser)
            print()
        else:
            print(f" Center Error:", None)

        #cv2.imshow('Square and Circle Detection', frame)
        # Convert OpenCV image to Tkinter-compatible format
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)

        # Update the canvas with the new image
        self.canvas.config(width=img.width(), height=img.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.img = img


        self.root.after(10, self.run_loop)


if __name__ == "__main__":
    root = tk.Tk()
    # app1 = MainWindow(root)
    
    # Open the ThirdWindow upon startup
    third_window = tk.Toplevel(root)
    app3 = ThirdWindow(third_window)
    
    root.mainloop()

    app3.cap.release()
    cv2.destroyAllWindows()