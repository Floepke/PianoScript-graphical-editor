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


class DrawSpline:
    """ draw a spline """

    def __init__(self):
        """ initialize the class"""

        self.root = Tk()
        board = Board(root=self.root)

        x_arr = [100.0, 120.0, 140.0, 160.0]
        y_arr = [50.0, 75.0, 60.0, 80.0]
        spline = Spline()
        spline.set_points(x_arr=x_arr,
                          y_arr=y_arr)

        curve = Curve()
        for x_p in range(100, 161):
            y_p = spline.interpolate(x_p)
            curve.append(Point(x_p=x_p, y_p=y_p))

        board.draw_curve(curve=curve, bg='blue', width=3)

        pt1 = Point(x_p=130, y_p=20)
        pt2 = Point(x_p=130, y_p=90)
        curve = Curve(array=[pt1, pt2])
        board.draw_curve(curve=curve, bg='black', width=1)

        cur_y = spline.interpolate(pt1.x)

        board.draw_circle(x_c=pt1.x, y_c=cur_y, r_c=4, bg=None, ol='red', w_c=1)
        self.root.mainloop()


def main() -> int:
    """ main function """

    _ = DrawSpline()

    return 0


if __name__ == '__main__':
    _exit(main())
