import tkinter as tk

def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_scrollbar_move(*args):
    canvas.yview(*args)
    
root = tk.Tk()
root.title("Scrollbar Example")

canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(canvas, command=on_scrollbar_move)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Attach the on_canvas_configure function to the canvas configuration event
canvas.bind("<Configure>", on_canvas_configure)

for i in range(50):
    tk.Label(frame, text=f"Label {i}").pack()

root.mainloop()
