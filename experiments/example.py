import tkinter as tk
import math

class BezierCurveApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cubic Bezier Curve Editor")
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()
        self.control_points = [(100, 100), (150, 200), (250, 200), (300, 100)]
        self.curve_color = "black"
        self.control_point_color = "blue"
        self.selected_point_index = None
        self.start_width = 2
        self.middle_width = 100
        self.draw_curve(self.start_width,self.middle_width)
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
            self.control_points[self.selected_point_index] = (event.x, event.y)
            self.canvas.delete("all")
            self.draw_curve(self.start_width,self.middle_width)
            self.draw_control_points()
    
    def draw_curve(self, start_width, middle_width):
        curve_points = []
        steps = 100
        for t in range(0, steps):
            x, y = self.evaluate_cubic_bezier(t / 100, self.control_points)
            curve_points.append([x, y])
        setting = 10

        # better solution for drawing the slur:
        def linear_interpolation(x,y,z):
            return (z - x) / (y - x)
        points = []
        for idx,c in enumerate(curve_points):
            if idx > 50: idx = 100 - idx
            add = -linear_interpolation(start_width, middle_width, idx)*10
            points.append((c[0], c[1]+add))
        for idx,c in enumerate(reversed(curve_points)):
            if idx > 50: idx = 100 - idx
            add = linear_interpolation(start_width, middle_width, idx)*10
            points.append((c[0], c[1]+add))
        self.canvas.create_polygon(points, fill=self.curve_color)

        # solution for drawing the slur:
        # for c in range(len(curve_points)):
        #     if c < 49: width = middle_width * (c / 100)
        #     else: width = middle_width * ((100 - c) / 100)
        #     if c == len(curve_points)-1: break
        #     self.canvas.create_line(curve_points[c], curve_points[c+1], fill=self.curve_color, width=width, capstyle='round')
    
    def draw_control_points(self):
        for i, (x, y) in enumerate(self.control_points):
            fill_color = self.control_point_color
            if self.selected_point_index == i:
                fill_color = "green"
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=fill_color)
    
    def evaluate_cubic_bezier(self, t, control_points):
        p0, p1, p2, p3 = control_points
        x = (1 - t) ** 3 * p0[0] + 3 * t * (1 - t) ** 2 * p1[0] + 3 * t ** 2 * (1 - t) * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * t * (1 - t) ** 2 * p1[1] + 3 * t ** 2 * (1 - t) * p2[1] + t ** 3 * p3[1]
        return x, y

root = tk.Tk()
app = BezierCurveApp(root)
root.mainloop()
