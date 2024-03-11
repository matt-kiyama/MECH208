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
        self.root.title("Third Window")

        self.label = ttk.Label(root, text="Third Window Content")
        self.label.pack(padx=20, pady=20)

        self.close_button = ttk.Button(root, text="Close Third Window", command=self.close_third_window)
        self.close_button.pack(pady=10)

    def close_third_window(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app1 = MainWindow(root)
    
    # Open the ThirdWindow upon startup
    third_window = tk.Toplevel(root)
    app3 = ThirdWindow(third_window)
    
    root.mainloop()
