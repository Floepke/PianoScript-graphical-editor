import tkinter as tk

app = tk.Tk()
app.title("Maximized Window Example")

# Maximize the window
app.attributes("-zoomed", 1)

app.mainloop()