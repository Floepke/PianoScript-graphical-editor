#! python3.11
# coding: utf8

from __future__ import annotations

""" calculate spline coordinates """

__author__ = 'Sihir'  # noqa
__copyright__ = "© Sihir 2023-2023 all rights reserved"  # noqa

from math import radians
from math import degrees
from math import sin
from math import cos
from math import sqrt
from math import atan2


class Point:
    """ a point on the canvas """

    def __init__(self, **kwargs):
        """ initialize the point """

        if 'pt' in kwargs:
            pt = kwargs.get('pt', None)
            self.x_p = pt.x_p
            self.y_p = pt.x_p
        else:
            self.x_p = kwargs.get('x_p', 0.0)
            self.y_p = kwargs.get('y_p', 0.0)

    @property
    def x(self):
        """ get the x coordinate """

        return self.x_p

    @x.setter
    def x(self, value: float):
        """ get the x coordinate """

        self.x_p = value

    @property
    def y(self):
        """ get the y coordinate """

        return self.y_p

    @y.setter
    def y(self, value: float):
        """ get the x coordinate """

        self.y_p = value

    def move(self, **kwargs) -> Point:
        """ move a point over delta x and y """

        if 'delta' in kwargs:
            delta = kwargs.get('delta', Point(x_p=0.0, y_p=0.0))
        else:
            delta = Point(x_p=kwargs.get('delta_x', 0.0), y_p=kwargs.get('delta_y', 0.0))

        return Point(x_p=self.x_p + delta.x, y_p=self.y_p + delta.y)

    def rotate(self, ang: float, unit_rad: bool = False) -> Point:
        """ rotate a point """

        # note: the rotation is done in the opposite fashion
        # from for a right-handed coordinate system due to
        # the left-handedness of computer coordinates
        ang_rad = ang if unit_rad else radians(ang)
        x_rot = self.x_p * cos(ang_rad) + self.y_p * sin(ang_rad)
        y_rot = -self.x_p * sin(ang_rad) + self.y_p * cos(ang_rad)
        return Point(x_p=x_rot, y_p=y_rot)

    def enlarge(self, factor: float) -> Point:
        """ multiply the coordinates with a factor """

        return Point(x_p=self.x_p * factor, y_p=self.y_p * factor)

    def distance(self, other: Point) -> float:
        """ distance between two points """

        value_x = other.x_p - self.x_p
        value_y = other.y_p - self.y_p
        return sqrt(value_x * value_x + value_y * value_y)

    def angle(self, other: Point, unit_rad: bool = False) -> float:
        """ the direction in radians of a line """

        rad = atan2(other.x_p - self.x_p, other.y_p - self.y_p)
        return rad if unit_rad else 180 - degrees(rad)

    @property
    def int_tuple(self) -> ():
        """ return as tuple of int """
        return int(round(self.x_p)), int(round(self.y_p))

    def mirror_x(self) -> Point:
        """ mirror x in the y axis """
        return Point(x_p=-self.x_p, y_p=self.y_p)

    def mirror_y(self) -> Point:
        """ mirror y in the x axis """
        return Point(x_p=self.x_p, y_p=-self.y_p)

    def __str__(self) -> str:
        """ convert to string """
        return f'({self.x_p:.3f},{self.y_p:.3f})'

    @classmethod
    def event(cls, event):
        """ convert event position to Point """
        return Point(x_p=event.x, y_p=event.y)
