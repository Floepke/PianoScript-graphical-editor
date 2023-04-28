from tkinter import *

class BezierCurveApp:
    def __init__(self, master):
        self.master = master
        self.canvas_width = 400
        self.canvas_height = 400
        self.curve_color = "blue"
        self.curve_width = 2
        self.p1 = (100, 100)
        self.p2 = (200, 300)
        self.p3 = (300, 100)
        self.selected_point = None
        
        self.canvas = Canvas(self.master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        self.draw_curve()
        
    def on_mouse_down(self, event):
        if self.distance(event.x, event.y, self.p1[0], self.p1[1]) <= 10:
            self.selected_point = self.p1
        elif self.distance(event.x, event.y, self.p2[0], self.p2[1]) <= 10:
            self.selected_point = self.p2
        elif self.distance(event.x, event.y, self.p3[0], self.p3[1]) <= 10:
            self.selected_point = self.p3
    
    def on_mouse_move(self, event):
        if self.selected_point:
            self.selected_point = (event.x, event.y)
            self.draw_curve()
    
    def on_mouse_up(self, event):
        self.selected_point = None
        
    def draw_curve(self):
        self.canvas.delete("all")
        self.canvas.create_oval(self.p1[0]-5, self.p1[1]-5, self.p1[0]+5, self.p1[1]+5, fill="red")
        self.canvas.create_oval(self.p2[0]-5, self.p2[1]-5, self.p2[0]+5, self.p2[1]+5, fill="green")
        self.canvas.create_oval(self.p3[0]-5, self.p3[1]-5, self.p3[0]+5, self.p3[1]+5, fill="blue")
        
        curve_points = []
        for t in range(0, 101, 1):
            t = t / 100
            x = (1-t)**2 * self.p1[0] + 2*t*(1-t) * self.p2[0] + t**2 * self.p3[0]
            y = (1-t)**2 * self.p1[1] + 2*t*(1-t) * self.p2[1] + t**2 * self.p3[1]
            curve_points.append(x)
            curve_points.append(y)
            
        self.canvas.create_line(curve_points, fill=self.curve_color, width=self.curve_width)
    
    def distance(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

from tkinter import Tk

root = Tk()
app = BezierCurveApp(root)
root.mainloop()