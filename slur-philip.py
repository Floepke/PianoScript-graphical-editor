import tkinter as tk
import math

class BezierCurveApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cubic Bezier Curve Editor")
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack(expand=True, fill='both')
        self.control_points = [[200, 100], [250, 200], [350, 200], [400, 100]]
        self.control_points2 = [[0, 100], [50, 210], [150, 210], [200, 100]]
        self.control_point_color = "black"
        self.selected_point_index = None
        self.width = 10
        self.draw_curve()
        self.draw_control_points()
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
    
    def on_mouse_click(self, event):
        x, y = event.x, event.y
        for i, (px, py) in enumerate(self.control_points):
            if abs(x - px) < 10 and abs(y - py) < 10:
                self.selected_point_index = i
                break
    
    def on_mouse_drag(self, event):
        if self.selected_point_index is not None:
            self.control_points[self.selected_point_index] = [event.x, event.y]
            self.canvas.delete("all")
            self.draw_curve()
            self.draw_control_points()
    
    def draw_curve(self):
        # here is my question: I try to create a music slur using polygon from tkinter.
        # my approach is to draw two cubic bezier curves with slightly different middle control points.
        # how to draw the outline of a music slur?????
        curve_points = []
        ctl1 = self.control_points[0]
        ctl2 = self.control_points[1]
        ctl3 = self.control_points[2]
        ctl4 = self.control_points[3]

        # creating the basic curve
        for t in range(100):
            x, y = self.evaluate_cubic_bezier(t / 100, [ctl1,ctl2,ctl3,ctl4])
            curve_points.append([x, y])

        # doing the same curve in reverse with slightly changed ctl2 and ctl3 points. How to calculate the right xy offsets for ctl2 and 3?????
        for t in reversed(range(100)):
            x, y = self.evaluate_cubic_bezier(t / 100, [ctl1,[ctl2[0]+15,ctl2[1]+10],[ctl3[0],ctl3[1]+10],ctl4])
            curve_points.append([x, y])
        
        # draw slur
        self.canvas.create_polygon(curve_points, fill='black', tag='slur')
        self.canvas.create_line(self.control_points, dash=(6,6), width=1, fill='red')
    
    def draw_control_points(self):
        for i, (x, y) in enumerate(self.control_points):
            fill_color = self.control_point_color
            if self.selected_point_index == i:
                fill_color = "green"
            r = 5
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill_color)
    
    def evaluate_cubic_bezier(self, t, control_points):
        p0, p1, p2, p3 = control_points
        x = (1 - t) ** 3 * p0[0] + 3 * t * (1 - t) ** 2 * p1[0] + 3 * t ** 2 * (1 - t) * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * t * (1 - t) ** 2 * p1[1] + 3 * t ** 2 * (1 - t) * p2[1] + t ** 3 * p3[1]
        return x, y

root = tk.Tk()
app = BezierCurveApp(root)
root.mainloop()