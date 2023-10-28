#! python3.11
# coding: utf8

""" calculate spline coordinates """

__author__ = 'Sihir'  # noqa
__copyright__ = "© Sihir 2023-2023 all rights reserved"  # noqa

from sys import exit as _exit

from tkinter import Tk

from point import Point
from slur import Slur
from board import Board


class DrawSlur:
    """ draw a polygon """

    def __init__(self):
        """ initialize the class """

        self.root = Tk()
        self.board = Board(root=self.root)
        self.selected = None
        self.points = []
        self.points.append(Point(x_p=50, y_p=50))
        self.points.append(Point(x_p=100, y_p=70))
        self.points.append(Point(x_p=150, y_p=40))
        self.points.append(Point(x_p=200, y_p=50))
        self.points.append(Point(x_p=250, y_p=20))

        width_end = 10
        width_center = 10
        self.delta = [width_end, width_center, width_center, width_center, width_end]

        self.draw()
        self.root.mainloop()

    def draw(self):
        """ draw the slur """

        slur = Slur(center=self.points, center_width=4.0)

        self.board = Board(root=self.root)
        self.board.draw_polygon(slur.curve, bg='blue', ol='blue')

        # slur.curve.move(delta_x=0.0, delta_y=-20.0)
        # self.board.draw_polygon(slur.curve, bg='blue', ol='blue')

        center = slur.curve.center()

        # move around isocenter
        slur.curve.move(delta=center.enlarge(factor=-1))
        slur.curve.rotate(ang=90.0)
        # move back
        slur.curve.move(delta=center)
        # and draw again
        self.board.draw_polygon(slur.curve, bg='red', ol='red')

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


def main() -> int:
    """ main function """

    _ = DrawSlur()

    return 0


if __name__ == '__main__':
    _exit(main())
