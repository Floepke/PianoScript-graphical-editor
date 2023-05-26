import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor

def opposite_color(hex_color):
    # Remove the "#" from the hexadecimal color code
    hex_color = hex_color.lstrip("#")

    # Convert the hex color to RGB values
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # Calculate the opposite RGB values
    r_opposite = 255 - r
    g_opposite = 255 - g
    b_opposite = 255 - b

    # Convert the opposite RGB values to hex color code
    opposite_hex_color = f"#{r_opposite:02x}{g_opposite:02x}{b_opposite:02x}"

    return opposite_hex_color


def in_between_color(color1, color2):
    # Remove the "#" from the hexadecimal color codes
    color1 = color1.lstrip("#")
    color2 = color2.lstrip("#")

    # Convert the hex colors to RGB values
    r1, g1, b1 = tuple(int(color1[i:i+2], 16) for i in (0, 2, 4))
    r2, g2, b2 = tuple(int(color2[i:i+2], 16) for i in (0, 2, 4))

    # Calculate the average RGB values
    r_avg = (r1 + r2) // 2
    g_avg = (g1 + g2) // 2
    b_avg = (b1 + b2) // 2

    # Convert the average RGB values to hex color code
    in_between_hex_color = f"#{r_avg:02x}{g_avg:02x}{b_avg:02x}"

    return in_between_hex_color


import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser


class ColorPicker(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Color Picker")
        self.geometry("250x200")

        # Initialize RGB values
        self.r_value = tk.IntVar()
        self.g_value = tk.IntVar()
        self.b_value = tk.IntVar()

        # Create RGB sliders
        self.r_slider = ttk.Scale(self, from_=0, to=255, variable=self.r_value,
                                  orient=tk.HORIZONTAL, length=200,
                                  command=self.update_color)
        self.r_slider.set(0)
        self.r_slider.pack(pady=10)

        self.g_slider = ttk.Scale(self, from_=0, to=255, variable=self.g_value,
                                  orient=tk.HORIZONTAL, length=200,
                                  command=self.update_color)
        self.g_slider.set(0)
        self.g_slider.pack(pady=10)

        self.b_slider = ttk.Scale(self, from_=0, to=255, variable=self.b_value,
                                  orient=tk.HORIZONTAL, length=200,
                                  command=self.update_color)
        self.b_slider.set(0)
        self.b_slider.pack(pady=10)

        # Create color preview label
        self.color_preview = tk.Label(self, width=15, height=5, bg="black")
        self.color_preview.pack(pady=10)

        # Create OK button
        self.ok_button = ttk.Button(self, text="OK", command=self.get_color)
        self.ok_button.pack(pady=10)

    def update_color(self, *args):
        # Get current RGB values
        r = self.r_value.get()
        g = self.g_value.get()
        b = self.b_value.get()

        # Convert RGB to hexadecimal
        color_hex = f"#{r:02x}{g:02x}{b:02x}"

        # Update color preview
        self.color_preview.configure(bg=color_hex)

    def get_color(self):
        # Get current RGB values
        r = self.r_value.get()
        g = self.g_value.get()
        b = self.b_value.get()

        # Convert RGB to hexadecimal
        color_hex = f"#{r:02x}{g:02x}{b:02x}"

        # Return hexadecimal color code
        self.parent.clipboard_clear()
        self.parent.clipboard_append(color_hex)
        self.destroy()
        

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = ColorPicker(root)
    app.mainloop()