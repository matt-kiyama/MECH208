import tkinter as tk
from tkinter import ttk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Window")

        self.label = ttk.Label(root, text="Main Window Content")
        self.label.pack(padx=20, pady=20)

        self.open_button = ttk.Button(root, text="Open Second Window", command=self.open_second_window)
        self.open_button.pack(pady=10)

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
