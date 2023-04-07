import tkinter as tk
import random


root = tk.Tk()
canvas = tk.Canvas(root, width=550, height=500, borderwidth=0)
canvas.pack(expand=True, fill="both")

coord_list=[]

for i in range(random.randint(1,4)):
    xos=[150,200,250,300,350,400,450,500]
    yos=[150,200,250,300,350,400,450]
    xos_=random.choice(xos)
    yos_=random.choice(yos)

    coord = (xos_,yos_,xos_+50,yos_+50)
    coord_list.append(coord)
    objectt=canvas.create_rectangle(coord, fill="blue")
    canvas.create_rectangle(25, 15, 50, 40, fill="red")

# Delete red rectangle
def delete1(event):
    item = canvas.find_overlapping(25, 15, 50, 40)
    canvas.delete(item)

# Delete blue rectangles
def delete2(event):
    for coord in coord_list:
        item = canvas.find_overlapping(*coord)
        canvas.delete(item)

#Click on the canvas to delete objects at the coordinates
canvas.bind("<Button-1>", delete2) # change function to delete blue rectangles
root.mainloop()