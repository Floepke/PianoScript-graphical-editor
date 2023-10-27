#! python3.11
# coding: utf8

""" calculate spline coordinates """

__author__ = 'Sihir'  # noqa
__copyright__ = "© Sihir 2023-2023 all rights reserved"  # noqa


def _sign(value: float) -> int:
    """ return the sign of a value """
    return 1 if value >= 0.0 else -1


def _safe_div(num: float, denom: float) -> float:
    """ safe devision
    :param num: the numerator
    :param denom: the denominator
    :returns: quotient: float>
    """

    if denom == 0.0:
        return 0.0 if num == 0.0 else _sign(num) * 100000.0
    return num / denom


# pylint: disable=too-few-public-methods
class Spline:
    """ Description for Spline.
        This class receives an array of support points
        SetPoints(double [] x, double [] y, double yp1, double ypn)
        The last two parameters set the first derivative at the
        start and the end point
    """

    def __init__(self):
        """ initialize the class """
        self._size: int = 0
        self._spline_x: [float] = []
        self._spline_y: [float] = []
        self._spline_y2: [float] = []

    def set_points(self, x_arr: [float], y_arr: [float],
                   yp1: float = None, ypn: float = None) -> bool:
        """ set_point copies the arrays x and y and stores the
            derivatives at the first and the last point
        :param self: instance
        :param x_arr: array of x
        :param y_arr: array of y
        :param yp1: derivative at the first point
        :param ypn: derivative at the last point
        :returns bool: success
        """
        size = len(x_arr)
        self._size = size
        assert len(y_arr) == size

        self._spline_x = x_arr
        self._spline_y = y_arr
        self._spline_y2 = [0.0] * size
        u_arr = [0.0] * size

        # when yp1 is None take the 'natural' value else copy the derivative
        if yp1 is not None:
            self._spline_y2[0] = -0.5
            u_arr[0] = _safe_div(3.0, x_arr[1] - x_arr[0]) * \
                   (_safe_div(y_arr[1] - y_arr[0], x_arr[1] - x_arr[0]) - yp1)

        for i in range(1, size - 1):
            # This is the decomposition loop of the tridiagonal
            # algorithm. y2 and u are used for temporary storage
            # of the decomposed factors.
            sig = _safe_div(x_arr[i] - x_arr[i - 1], x_arr[i + 1] - x_arr[i - 1])
            par = sig * self._spline_y2[i - 1] + 2.0

            self._spline_y2[i] = _safe_div(sig - 1.0, par)
            u_arr[i] = _safe_div(y_arr[i + 1] - y_arr[i], x_arr[i + 1] - x_arr[i]) - \
                   _safe_div(y_arr[i] - y_arr[i - 1], x_arr[i] - x_arr[i - 1])
            u_arr[i] = _safe_div(6.0 * _safe_div(u_arr[i],
                                             x_arr[i + 1] - x_arr[i - 1]) - sig * u_arr[i - 1], par)

        q_n = 0.0
        u_n = 0.0

        # when ypn is None take the 'natural' value else copy the derivative
        if ypn is not None:  # The upper boundary condition is set
            q_n = 0.5
            u_n = _safe_div(3.0, x_arr[size - 1] - x_arr[size - 2]) * \
                 (ypn - _safe_div(y_arr[size - 1] - y_arr[size - 2],
                                  x_arr[size - 1] - x_arr[size - 2]))

        self._spline_y2[size - 1] = (u_n - q_n * u_arr[size - 2]) / \
                                    (q_n * self._spline_y2[size - 2] + 1.0)

        # This is the back-substitution loop of the tridiagonal algorithm.
        for k in range(size - 2, -1, -1):
            self._spline_y2[k] = self._spline_y2[k] * self._spline_y2[k + 1] + u_arr[k]

        return True

    def interpolate(self, x_i: float) -> float:
        """ Given the arrays xa[1..n] and ya[1..n], which tabulate a function (with
            the xai's in order),and given the array y2a[1 .. n], which is the output
            from spline above, and given a value of x, this routine returns a
            cubic-spline interpolated value y.
        :param x_i:
        :returns: interpolated value
        """
        size = self._size
        klo: int = 0
        khi: int = size - 1
        k_v: int = 0
        h_v: float = 0.0
        b_v: float = 0.0
        a_v: float = 0.0

        # We will find the right place in the table by means of
        # bisection. This is optimal if sequential calls to this
        # routine are at random values of x. If sequential calls
        # are in order, and closely spaced, one would do better
        # to store previous values of klo and khi and test if
        # they remain appropriate on the next call.
        while khi - klo > 1:
            k_v = (khi + klo) >> 1
            if self._spline_x[k_v] > x_i:
                khi = k_v
            else:
                klo = k_v

        # klo and khi now bracket the input value of x
        h_v = self._spline_x[khi] - self._spline_x[klo]

        # The xa's should be distinct.
        a_v = _safe_div(self._spline_x[khi] - x_i, h_v)
        b_v = _safe_div(x_i - self._spline_x[klo], h_v)  # Cubic spline polynomial is now evaluated

        return a_v * self._spline_y[klo] + b_v * self._spline_y[khi] + \
            ((a_v * a_v * a_v - a_v) * self._spline_y2[klo] +
             (b_v * b_v * b_v - b_v) * self._spline_y2[khi]) * (h_v * h_v) / 6.0
