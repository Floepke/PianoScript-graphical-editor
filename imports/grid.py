#! python3.11
# coding: utf-8

""" grid data proposal """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

# "grid":[
#       {
#         "amount":8,
#         "numerator":5,
#         "denominator":4,
#         "grid":4,
#         "hidden": [2, 4],
#         "visible":true
#        }
#
# result:
#        1 =======    (bar)
#        2 -
#        3 -------
#        4 -
#        5 -------
#        1 =======    (bar)
# ],

from dataclasses import dataclass


@dataclass
class Grid:
    """ measure definition """

    def __init__(self, **kwargs):
        """ initialize the class """

        if 'dct' in kwargs:
            kwargs = kwargs.get('dct', {})

        self.ident: int = int(kwargs.get('ident', -1))
        self.start: int = int(kwargs.get('start', 1))
        self.amount: int = int(kwargs.get('amount', 1))
        self.numerator: int = int(kwargs.get('numerator', 4))
        self.denominator: int = int(kwargs.get('denominator', 4))
        self.hidden: [] = kwargs.get('hidden', [])
        self.visible: bool = bool(kwargs.get('visible', True))

    def __eq__(self, other):
        """ return True when the other has the same ident """

        return self.ident == other.ident

    def to_dict(self) -> dict:
        """ convert back to dictionary """

        return {
            'grid': self.ident,
            'tag': f'grid{self.ident - 1}',
            'start': self.start,
            'amount': self.amount,
            'numerator': self.numerator,
            'denominator': self.denominator,
            'hidden': self.hidden,
            'visible': self.visible
        }

@dataclass
class GridList:
    """ list of measure definition """

    def __init__(self, **kwargs):
        """ initialize the class """
        self.lst = []

        if 'lst' in kwargs:
            # lst is Grid[]
            self.lst = kwargs.get('lst', [])
        elif 'dct' in kwargs:
            # dct is a list of Grid dictionary
            for dct in kwargs.get('dct', []):
                self.lst.append(Grid(dct=dct))

        self.renumber()

    def append(self, index: int = None, grid: Grid = None):
        """ append another grid """

        index = len(self.lst) if index is None else int(index)
        self.lst.insert(index, grid)
        self.renumber()

    def renumber(self):
        """ renumber the grids """

        start = 1
        for number, grid in enumerate(self.lst, 1):
            grid.index = number
            grid.start = start
            start += grid.amount

    def remove(self, number: str):
        """ remove a grid from the list """

        item = next((grd for grd in self.lst if int(grd.index) == int(number)), None)
        if item is not None:
            self.lst.remove(item)
            self.renumber()

    def swap(self, left: int, right: int):
        """ swap two entries """

        self.lst[left], self.lst[right] = self.lst[right], self.lst[left]
        self.renumber()

    def __len__(self):
        """ length of the list """

        if self.lst is None:
            return None

        return len(self.lst)
