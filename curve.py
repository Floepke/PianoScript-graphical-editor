#! python3.11
# coding: utf8

""" calculate spline coordinates """

__author__ = 'Sihir'  # noqa
__copyright__ = "© Sihir 2023-2023 all rights reserved"  # noqa

from point import Point


class Curve:
    """ a point on the canvas """

    def __init__(self, array: list[Point]=None):
        """ initialize the point """

        if array is None:
            self.array = []
        else:
            self.array = array

    def __getitem__(self, index: int):
        """ getter for index """

        return self.array[index]

    def __setitem__(self, index: int, value):
        """ setter for index """

        self.array[index] = value

    def append(self, pnt: Point):
        """ append a point to the array """

        self.array.append(pnt)

    @property
    def pairs(self):
        """ return """

        result = ()
        for pnt in self.array:
            result += (pnt.x, pnt.y)
        return result

    def move(self, **kwargs):
        """ move all points """

        if 'delta' in kwargs:
            delta = kwargs['delta']
        else:
            delta = Point(x_p=kwargs.get('delta_x', 0.0),
                          y_p=kwargs.get('delta_y', 0.0))

        result = []
        for pnt in self.array:
            result.append(pnt.move(delta=delta))
        self.array = result

    def rotate(self, ang: float):
        """ rotate all points """

        result = []
        for pnt in self.array:
            result.append(pnt.rotate(ang=ang))

        self.array = result

    def center(self) -> Point:
        """ where is the center of the curve """

        amount = len(self.array)
        x_p = sum([p.x_p for p in self.array]) / amount
        y_p = sum([p.y_p for p in self.array]) / amount

        return Point(x_p=x_p, y_p=y_p)