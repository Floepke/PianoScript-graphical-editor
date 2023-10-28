#! python3.11
# coding: utf8

""" create a slur from center points """

__author__ = 'Sihir'  # noqa
__copyright__ = "© Sihir 2023-2023 all rights reserved"  # noqa


from point import Point
from curve import Curve
from spline import Spline


# pylint: disable=too-few-public-methods
class Slur:
    """ create a slur """

    def __init__(self,
                 center: [],
                 center_width: float):
        """ create a slur """

        x_arr = [pt.x for pt in center]
        y_arr = [pt.y for pt in center]

        spline1 = Spline()
        spline1.set_points(x_arr=x_arr,
                           y_arr=y_arr)

        curve_points = []

        self._curve = Curve()
        for x_p in range(x_arr[0], x_arr[-1] + 1):
            y_p = spline1.interpolate(x_p)
            curve_points.append(Point(x_p=x_p, y_p=y_p))

        reversed_points = curve_points[::-1]
        offset = []
        amount = (len(curve_points) + 1) // 2
        for idx in range(amount):
            offset.append(Point(x_p=0.0, y_p=center_width * idx / amount))
        offset.extend(offset[::-1])

        for idx, pt in enumerate(curve_points):
            self._curve.append(pnt=pt.move(delta=offset[idx]))

        for idx, pt in enumerate(reversed_points):
            self._curve.append(pnt=pt.move(delta=offset[idx].mirror_y()))

    @property
    def curve(self):
        """ get the curve """

        return self._curve
