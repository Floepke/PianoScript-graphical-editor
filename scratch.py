import tkinter as tk

def on_key_press(event):
    if event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
        label.config(text="Shift key pressed")

def on_key_release(event):
    if event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
        label.config(text="Press the Shift key")

root = tk.Tk()
root.title("Shift Key Binding Example")

label = tk.Label(root, text="Press the Shift key")
label.pack(pady=20)

root.bind('<KeyPress>', on_key_press)
root.bind('<KeyRelease>', on_key_release)

root.mainloop()
