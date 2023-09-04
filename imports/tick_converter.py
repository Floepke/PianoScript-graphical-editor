#! python3.11
# coding: utf-8

""" convert tick to tuple """

__author__ = 'Philip Bergwerf'  # noqa
__copyright__ = '© Philip Bergwerf 2023-2023 all rights reserved'  # noqa

# from math import gcd as _gcd


def gcd(val1: int, val2: int) -> int:
    """ calculate the greatest common divisor """

    # Reduce the fraction to its simplest form
    # by dividing both numerator and denominator
    # by their greatest common divisor (GCD)

    while val2 != 0:
        val1, val2 = val2, val1 % val2

    return val1


def piano_ticks_to_time_signature(piano_ticks: int) -> tuple:
    """ convert piano tick to a fraction """

    # 8192 piano ticks represent a full note (1/1)
    # 2048 piano ticks represent a quarter note (1/4)
    # 8 piano ticks represent a quarter note (1/128)
    den = 8192

    # Calculate the numerator of the time signature fraction
    num = piano_ticks # // note_piano_ticks

    # Calculate the denominator of the time signature fraction
    # den = 4  # Since it's a quarter note by default

    # our GCD
    gcd_value = gcd(num, den)
    num //= gcd_value
    den //= gcd_value

    # Return the time signature fraction as a tuple (numerator, denominator)
    return num, den