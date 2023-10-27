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
