#! python3.11
# coding: utf8

""" calculate spline coordinates """

__author__ = 'Sihir'  # noqa
__copyright__ = "© Sihir 2023-2023 all rights reserved"  # noqa

from tkinter import Tk
from tkinter import Canvas

from typing import Optional

from point import Point
from curve import Curve


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

    # solve this by using kwargs:
    # pylint: disable=too-many-arguments
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
