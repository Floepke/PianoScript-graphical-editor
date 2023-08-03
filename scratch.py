import tkinter as tk
from tkinter import font

window = tk.Tk()
for i in list(font.families()):
    
    if 'Edwin' in i:
        print(i)
        tk.Label(window, text=i, font=(i, 16, 'bold')).pack()
window.mainloop()