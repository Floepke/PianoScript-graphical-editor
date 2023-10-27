#! python3.11
# coding: utf8

""" calculate spline coordinates """

__author__ = 'Sihir'  # noqa
__copyright__ = "© Sihir 2023-2023 all rights reserved"  # noqa

class Point:
    """ a point on the canvas """

    def __init__(self, x_p: float, y_p: float):
        """ initialize the point """

        self.x_p = x_p
        self.y_p = y_p

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
