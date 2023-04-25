import tkinter as tk
import math

class BezierCurveApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cubic Bezier Curve Editor")
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack(expand=True)
        self.control_points = [[100, 100], [150, 200], [250, 200], [300, 100]]
        self.control_points2 = [[100, 100], [150, 210], [250, 210], [300, 100]]
        self.curve_color = "black"
        self.control_point_color = "black"
        self.selected_point_index = None
        self.start_width = 10
        self.deltax = 0
        self.deltay = 0
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
            # if self.selected_point_index in [1,2]:
            #     self.control_points2[self.selected_point_index] = [event.x+self.width, event.y]
            # elif self.selected_point_index == 0:
            #     self.control_points2[self.selected_point_index] = [event.x, event.y]
            #     self.control_points2[self.selected_point_index] = [event.x, event.y]
            # else:
            #     self.control_points2[self.selected_point_index] = [event.x, event.y]
            #     self.control_points2[self.selected_point_index] = [event.x, event.y]

            self.canvas.delete("all")
            self.draw_curve()
            self.draw_control_points()
    
    def draw_curve(self):
        curve_points = []
        steps = 100
        for t in range(steps):
            x, y = self.evaluate_cubic_bezier(t / steps, self.control_points)
            curve_points.append([x, y])

        # experiment
        ctl1 = self.control_points[0]
        ctl2 = self.control_points[1]
        ctl3 = self.control_points[2]
        ctl4 = self.control_points[3]
        ctl2 = self.xy2angle2xy(ctl2[0],ctl2[1],self.xyxy2angle(ctl1[0],ctl1[1],ctl4[0],ctl4[1]),self.width)
        ctl3 = self.xy2angle2xy(ctl3[0],ctl3[1],self.xyxy2angle(ctl1[0],ctl1[1],ctl4[0],ctl4[1]),self.width)
        thickness_x = self.width * math.degrees(math.atan2(abs(ctl1[0]-ctl4[0]), -abs(ctl1[1]-ctl4[1])))/200
        thickness_y = self.width * math.degrees(math.atan2(abs(ctl1[1]-ctl4[1]), -abs(ctl1[0]-ctl4[0])))/200
        for t in reversed(range(steps)):

            self.control_points2 = [[ctl1[0],ctl1[1]],
            [ctl2[0]+thickness_x,ctl2[1]+thickness_y],
            [ctl3[0]+thickness_x,ctl3[1]+thickness_y],
            [ctl4[0],ctl4[1]]
            ]

            x, y = self.evaluate_cubic_bezier(t / steps, self.control_points2)
            curve_points.append([x, y])
        self.canvas.create_polygon(curve_points, fill=self.curve_color, width=4)
        self.canvas.create_line(self.control_points, dash=(6,6), width=1)
    
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

    def xyxy2angle(self,x1,y1,x2,y2):
        return math.degrees(math.atan2(y2 - y1, x2 - x1))

    def xy2angle2xy(self,x1,y1,angledegrees,width):
        # Convert degrees to radians
        angle = math.radians(angledegrees)
        # Calculate the endpoint of the line using trigonometry
        x_end = x1 + width * math.cos(angle)
        y_end = y1 - width * math.sin(angle)
        return x_end,y_end

root = tk.Tk()
app = BezierCurveApp(root)
app = BezierCurveApp(root)
root.mainloop()
