#! python3.11
# coding: utf8

""" calculate spline coordinates """

__author__ = 'Sihir'  # noqa
__copyright__ = "© Sihir 2023-2023 all rights reserved"  # noqa

from sys import exit as _exit

from point import Point
from curve import Curve


def main() -> int:
    pt1 = Point(x_p=0, y_p=0)
    pt2 = Point(x_p=100, y_p=50)

    assert pt1.x == 0
    assert pt1.y == 0
    assert pt2.x == 100
    assert pt2.y == 50

    curve = Curve(array=[pt1, pt2])

    assert curve[0].x == 0
    assert curve[0].y == 0
    assert curve[1].x == 100
    assert curve[1].y == 50

    curve = Curve()
    for i in range(10):
        curve.append(Point(x_p=i, y_p=10 * i))

    for item in curve.pairs:
        print(item)

    return 0


if __name__ == '__main__':
    _exit(main())
