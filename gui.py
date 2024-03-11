import tkinter as tk
from tkinter import ttk

def update_slider_value(slider, text_var):
    try:
        value = float(text_var.get())
        slider.set(value)
    except ValueError:
        pass

def update_textbox_value(slider, text_var):
    text_var.set(slider.get())

def submit_values():
    value1 = slider1.get()
    value2 = slider2.get()
    value3 = slider3.get()

    # Do something with the values, e.g., print them
    print("Slider 1:", value1)
    print("Slider 2:", value2)
    print("Slider 3:", value3)

# Create the main window
root = tk.Tk()
root.title("Slider GUI")

# Slider 1
label1 = ttk.Label(root, text="Proportional:")
label1.grid(row=0, column=0, padx=5, pady=5, sticky="w")
var1 = tk.DoubleVar()
slider1 = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=200, variable=var1, command=lambda x: update_textbox_value(slider1, var1))
slider1.grid(row=0, column=1, padx=5, pady=5)
textbox1 = ttk.Entry(root, textvariable=var1, width=10)
textbox1.grid(row=0, column=2, padx=5, pady=5)
update_textbox_value(slider1, var1)

# Slider 2
label2 = ttk.Label(root, text="Integral:")
label2.grid(row=1, column=0, padx=5, pady=5, sticky="w")
var2 = tk.DoubleVar()
slider2 = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=200, variable=var2, command=lambda x: update_textbox_value(slider2, var2))
slider2.grid(row=1, column=1, padx=5, pady=5)
textbox2 = ttk.Entry(root, textvariable=var2, width=10)
textbox2.grid(row=1, column=2, padx=5, pady=5)
update_textbox_value(slider2, var2)

# Slider 3
label3 = ttk.Label(root, text="Derivative:")
label3.grid(row=2, column=0, padx=5, pady=5, sticky="w")
var3 = tk.DoubleVar()
slider3 = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=200, variable=var3, command=lambda x: update_textbox_value(slider3, var3))
slider3.grid(row=2, column=1, padx=5, pady=5)
textbox3 = ttk.Entry(root, textvariable=var3, width=10)
textbox3.grid(row=2, column=2, padx=5, pady=5)
update_textbox_value(slider3, var3)

# Submit button
submit_button = ttk.Button(root, text="Submit", command=submit_values)
submit_button.grid(row=3, column=0, columnspan=3, pady=10)

# Start the Tkinter event loop
root.mainloop()
