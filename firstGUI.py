import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import detectionWPID as detection

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenCV GUI")

        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        # Open a video capture object (you can replace '0' with the video file name)
        self.cap = cv2.VideoCapture(0)

        self.update()

    def update(self):
        # Read a frame from the video feed
        ret, frame = self.cap.read()

        # Break the loop if no frame is captured
        if not ret:
            return

        # Detect squares in the current frame
        square_result = detection.detect_square(frame, min_area=200, max_area=15000)
        # square_result = self.detect_square(frame, min_area=200, max_area=15000)

        # Detect circle in the current frame
        circle_result = detection.detect_ball(frame)
        # circle_result = self.detect_ball(frame)

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
            center_error = self.get_errors(square_center, circle_center)
            print(f" Center Error:", center_error)
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

        # Schedule the update method to be called after a delay
        self.root.after(1, self.update)


class ThirdWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("PID GUI")

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

if __name__ == "__main__":
    root = tk.Tk()
    app1 = MainWindow(root)
    
    # Open the ThirdWindow upon startup
    third_window = tk.Toplevel(root)
    app3 = ThirdWindow(third_window)
    
    root.mainloop()
