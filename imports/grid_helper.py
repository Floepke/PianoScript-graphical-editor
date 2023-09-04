#! python3.11
# coding: utf-8

""" grid data proposal """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from imports.grid import Grid
from imports.grid import GridList

from imports.string_builder import StringBuilder


class GridHelper:
    """ measure definition """

    @staticmethod
    def to_row(grid) -> list:
        """ representation in the table """

        hidden = ','.join([str(hide) for hide in grid.hidden])
        return [str(grid.start),
                str(grid.amount),
                f'{grid.numerator}/{grid.denominator}',
                'Yes' if grid.visible else 'No',
                f'[{hidden}]'
               ]

    @staticmethod
    def from_row(ident: str, values: []) -> Grid:
        """ get the grid from a row in the table ="""

        start = int(values[0])
        amount = int(values[1])

        num, den = values[2].split('/')
        visible = values[3] == 'Yes'
        value = values[4][1:-1]

        hidden = []
        if len(value) > 0:
            for hide in value.split(','):
                hidden.append(int(hide))

        grid = Grid(start=start,
                    ident=ident,
                    amount=amount,
                    numerator=int(num),
                    denominator=int(den),
                    hidden=hidden,
                    visible=visible)
        return grid

    @staticmethod
    def to_pianoticks(grid):  # noqa
        """ output:
            start,
            amount,
            [ tick position, ... ],
            [ hidden position, ...],
            Visible|Invisible,
            signature
        """

        builder = StringBuilder()
        builder.append(f'{grid.start},')
        builder.append(f'{grid.amount},[')

        ticks: [str] = []
        for tick in range(1, grid.numerator):
            pos = int(round(8192 * tick / grid.denominator))
            ticks.append(str(pos))
        builder.append(','.join(ticks))

        builder.append(f'],"{grid.numerator}/{grid.denominator}",')
        if len(grid.hidden) == 0:
            hidden = ''
        else:
            hidden = ','.join([str(hide) for hide in grid.hidden])
        builder.append(f'[{hidden}],')
        builder.append(f'{"Visible" if grid.visible else "Invisible"}')

        result = builder.to_string()
        return result

    @staticmethod
    def to_pianotick_list(grids: GridList):  # noqa
        """ convert to piano-ticks """

        result = []
        for grid in grids.lst:
            ticks = GridHelper.to_pianoticks(grid)
            result.append(ticks)

        return result
