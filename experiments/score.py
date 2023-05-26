import tkinter as tk

from math import atan2, pi
from tkinter import Tk, Canvas

def draw_slur(canvas, x0, y0, x1, y1, x2, y2, x3, y3):
    #x0, y0, x1, y1, x2, y2, x3, y3 = [x0, y0, x1, y1, x2, y2, x3, y3]
    
    cx1, cy1 = (x0 + x1) / 2, (y0 + y1) / 2
    cx2, cy2 = (x1 + x2) / 2, (y1 + y2) / 2
    cx3, cy3 = (x2 + x3) / 2, (y2 + y3) / 2
    
    ax, ay = cx1 + (x1 - cx1) / 3, cy1 + (y1 - cy1) / 3
    bx, by = cx2 + (x1 - cx2) / 3, cy2 + (y1 - cy2) / 3
    cx, cy = cx2 + (x2 - cx2) / 3, cy2 + (y2 - cy2) / 3
    dx, dy = cx3 + (x2 - cx3) / 3, cy3 + (y2 - cy3) / 3
    
    angle1 = atan2(y1 - y0, x1 - x0)
    angle2 = atan2(y2 - y1, x2 - x1)
    
    if angle2 < angle1:
        angle2 += 2 * pi
    
    r1 = (x1 - x0) ** 2 + (y1 - y0) ** 2
    r2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
    r3 = (x3 - x2) ** 2 + (y3 - y2) ** 2
    
    width1 = 8 * (1 - r1 / (r1 + r2))
    width2 = 8 * (1 - r3 / (r2 + r3))
    
    coords = [
        ax + (bx - ax) * t + (cx - 2 * bx + ax) * t ** 2 + (dx - 3 * cx + 3 * bx - ax) * t ** 3
        for t in [i / 20 for i in range(21)]
    ]
    
    coords += [
        ay + (by - ay) * t + (cy - 2 * by + ay) * t ** 2 + (dy - 3 * cy + 3 * by - ay) * t ** 3
        for t in [i / 20 for i in range(21)]
    ][1:]
    
    coords += [
        x3 + (x2 - x3) * t + (cx3 - 2 * x2 + x3) * t ** 2 + (cx2 - 2 * cx3 + x2) * t ** 3
        for t in [i / 20 for i in range(21)]
    ][1:]
    
    coords += [
        y3 + (y2 - y3) * t + (cy3 - 2 * y2 + y3) * t ** 2 + (cy2 - 2 * cy3 + y2) * t ** 3
        for t in [i / 20 for i in range(21)]
    ][1:]
    
    return canvas.create_polygon(coords[:80], fill='black')


root = tk.Tk()
canvas = tk.Canvas(root)
canvas.pack()
draw_slur(canvas, 100, 100, 150, 200, 250, 200, 300, 100)
root.mainloop()

