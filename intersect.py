#! python3.11
# coding: utf8

""" calculate spline coordinates """

__author__ = 'Sihir'  # noqa
__copyright__ = "© Sihir 2023-2023 all rights reserved"  # noqa

from sys import exit as _exit

from tkinter import Tk
from tkinter import Canvas

from typing import Optional

from point import Point
from curve import Curve
from spline import Spline


class Board:
    """drawing board """

    def __init__(self, root: Tk):
        """ initialize the class """

        self.canvas = Canvas(master=root,
                             width=400,
                             height=200,
                             background='white')

        self.canvas.grid(row=0,
                         column=0,
                         padx=2,
                         pady=2,
                         sticky='news')

    def draw_curve(self, curve: Curve, bg: str = 'black', width=1):
        """draw a curve"""

        last_x, last_y = curve[0].x, curve[0].y

        if len(curve.array) == 1:
            self.canvas.create_line(curve[0].x,
                                    curve[0].y,
                                    curve[0].x,
                                    curve[0].y,
                                    fill=bg,
                                    width=width)
        else:
            for cur_p in curve.array:
                self.canvas.create_line(last_x,
                                        last_y,
                                        cur_p.x,
                                        cur_p.y,
                                        fill=bg,
                                        width=width)

                last_x, last_y = cur_p.x, cur_p.y

    def draw_circle(self,
                    x_c: float,
                    y_c: float,
                    r_c: float = 10.0,
                    bg: Optional[str] = None,
                    ol: Optional[str] = 'black',
                    w_c: int = 1):
        """ draw a circle """

        self.canvas.create_oval(int(x_c - r_c),
                                int(y_c - r_c),
                                int(x_c + r_c),
                                int(y_c + r_c),
                                fill=bg,
                                outline=ol,
                                width=w_c)

    def draw_polygon(self,
                     curve: Curve,
                     bg: Optional[str] = 'black',
                     ol: Optional[str] = 'black'):
        """ draw a polygon from the outer edge of the curve """

        self.canvas.create_polygon(curve.pairs,
                                   fill=bg,
                                   outline=ol)

    def draw_plus(self,
                  pt: Point,
                  size: int,
                  width: int,
                  bg: Optional[str] = 'black'):
        """ draw a + on the """

        self.canvas.create_line(pt.x - size,
                                pt.y,
                                pt.x + size,
                                pt.y,
                                fill=bg,
                                width=width)

        self.canvas.create_line(pt.x,
                                pt.y - size,
                                pt.x,
                                pt.y + size,
                                fill=bg,
                                width=width)
class DrawLine:
    """ draw line class """

    def __init__(self):
        """ initialize the class"""

        self.root = Tk()

        board = Board(root=self.root)

        pt1 = Point(x_p=100, y_p=0)
        pt2 = Point(x_p=200, y_p=50)
        curve = Curve(array=[pt1, pt2])
        board.draw_curve(curve=curve, bg='blue', width=3)

        self.root.mainloop()

class Slur:
    """ create a slur """

    def __init__(self,
                 center: [],
                 width_end: int,
                 width_center: int):
        """ create a slur """

        delta = [width_end, width_center, width_center, width_end]
        index = 0
        edge1 = []

        for pt in center:
            edge1.append(Point(x_p=pt.x, y_p=pt.y + delta[index]))
            index += 1

        spline1 = Spline()
        spline1.set_points(x_arr=[pt.x for pt in edge1],
                           y_arr=[pt.y for pt in edge1])

        index = 0
        edge2 = []
        for pt in center:
            edge2.append(Point(x_p=pt.x, y_p=int(pt.y - delta[index])))
            index += 1

        edge2.append(edge1[0])
        spline2 = Spline()
        spline2.set_points(x_arr=[pt.x for pt in edge2],
                           y_arr=[pt.y for pt in edge2])

        start_x = int(center[0].x)
        finish_x = int(center[-1].x)

        self._curve = Curve()
        for x_p in range(start_x, finish_x + 1):
            y_p = spline1.interpolate(x_p)
            self._curve.append(Point(x_p=x_p, y_p=y_p))

        for x_p in range(finish_x, start_x - 1, -1):
            y_p = spline2.interpolate(x_p)
            self._curve.append(Point(x_p=x_p, y_p=y_p))

    @property
    def curve(self):
        """ get the curve """

        return self._curve


class DrawSlur:
    """ draw a polygon """

    def __init__(self):
        """ initialize the class """

        self.selected = None
        self.points = []
        self.points.append(Point(x_p=50, y_p=50))
        self.points.append(Point(x_p=100, y_p=70))
        self.points.append(Point(x_p=150, y_p=40))
        self.points.append(Point(x_p=200, y_p=50))

        self.root = Tk()
        self.draw()
        self.root.mainloop()

    def draw(self):
        slur = Slur(center=self.points, width_end=1, width_center=4)

        self.board = Board(root=self.root)
        self.board.draw_polygon(slur.curve, bg='blue', ol='blue')

        for pt in self.points:
            self.board.draw_plus(pt=pt,
                                 size=4,
                                 width=2,
                                 bg='red')

        self.board.canvas.bind("<Button-1>", self.on_mouse_click)
        self.board.canvas.bind("<B1-Motion>", self.on_mouse_drag)

    def on_mouse_click(self, event):
        """ canvas was clicked """

        self.selected = None
        x, y = event.x, event.y
        for i, pnt in enumerate(self.points):
            if abs(x - pnt.x) < 10 and abs(y - pnt.y) < 10:
                self.selected = i
                break

    def on_mouse_drag(self, event):
        """ mouse was dragged """

        if self.selected is not None:
            self.points[self.selected] = Point(x_p=event.x, y_p=event.y)
            self.board.canvas.delete('all')
            self.draw()

class DrawCurve:
    """ draw a spline """

    def __init__(self):
        """ initialize the class"""

        self.root = Tk()
        board = Board(root=self.root)

        x_arr = [100.0, 120.0, 140.0, 160.0]
        y_arr1 = [50.0, 75.0, 60.0, 80.0]

        pts = []
        for idx in range(len(x_arr)):
            pts.append(Point(x_p=x_arr[idx], y_p=y_arr1[idx]))

        spline1 = Spline()
        spline1.set_points(x_arr=x_arr,
                           y_arr=y_arr1)

        y_arr2 = [50.0, 85.0, 70.0, 80.0]
        spline2 = Spline()
        spline2.set_points(x_arr=x_arr,
                           y_arr=y_arr2)

        curve = Curve()
        for x_p in range(100, 161):
            y_p = spline1.interpolate(x_p)
            curve.append(Point(x_p=x_p, y_p=y_p))

        for x_p in range(160, 99, -1):
            y_p = spline2.interpolate(x_p)
            curve.append(Point(x_p=x_p, y_p=y_p))

        # board.draw_curve(curve=curve, bg='blue', width=3)
        board.draw_polygon(curve, bg='blue', ol='blue')

        pt1 = Point(x_p=130, y_p=20)
        pt2 = Point(x_p=130, y_p=90)
        curve = Curve(array=[pt1, pt2])
        board.draw_curve(curve=curve, bg='black', width=1)

        cur_y = spline2.interpolate(pt1.x)

        board.draw_circle(x_c=pt1.x, y_c=cur_y, r_c=4, bg=None, ol='red', w_c=1)

        for pt in pts:
            board.draw_plus(pt=pt,
                            size=4,
                            width=2,
                            bg='red')

        self.root.mainloop()


def main() -> int:
    """ main function """

    _ = DrawSlur()

    return 0


if __name__ == '__main__':
    _exit(main())
