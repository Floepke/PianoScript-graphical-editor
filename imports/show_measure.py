#! python3.11
# coding: utf-8

""" grid editor proposal """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from tkinter import Frame
from tkinter.font import Font
from tkinter import Canvas

from imports.grid import Grid
from imports.grid_helper import GridHelper


class ShowMeasure:
    """ show the configuration of the measure"""

    def __init__(self, master: Frame, **kwargs):
        """ initialize the view """

        row = kwargs.get('row', 0)
        self.ident = None
        self.start = kwargs.get('start', 1)
        self.finish = kwargs.get('finish', 1)
        self.top = None
        self.bottom = None
        self.step = None
        self.numerator = None
        self.grid = None
        self.on_result = None

        row = 5
        canvas = Canvas(master=master,
                        background='black',
                        width=200,
                        height=270)

        canvas.configure(bg='white')
        canvas.bind('<Button-1>', self.left_click)

        canvas.grid(row=row,
                    rowspan=1,
                    column=0,
                    padx=(4, 4),
                    pady=2,
                    sticky='ns')

        self._canvas = canvas

    def left_click(self, event):
        """ left click on canvas """

        pos = 1 + int(round((event.y - self.top) / self.step))
        how = 'ignored' if pos >= self.numerator + 1 else ''
        # print(f'click on x: {event.x} y: {event.y} line {pos} {how}')

        if pos in self.grid.hidden:
            self.grid.hidden.remove(pos)
        else:
            self.grid.hidden.append(pos)
            self.grid.hidden.sort()

        # print(self.grid.hidden)

        self.selected(self.grid)

    def get_font(self, can: Canvas, available: float) -> tuple:
        """ get the font size for the available height """

        id_txt = can.create_text(0, 0, text='M')
        bounds = can.bbox(id_txt)   # returns a tuple like (x1, y1, x2, y2)
        height = bounds[3] - bounds[1]
        def_font = can.itemcget(id_txt, 'font')
        info = Font(family=def_font).actual()
        size = min(info['size'], 10)

        if size > available:
            size = int(size * available / height)

        can.delete(id_txt)

        return def_font, str(size), 'normal'

    def selected(self, grid: Grid):
        """ selected settings """

        self.ident = grid.ident
        self.grid = grid
        self.numerator = grid.numerator

        # print(f'show_measure.on_result, grid.hidden {grid.hidden}')
        if self.on_result is not None:
            self.on_result(grid)

        canvas = self._canvas
        canvas.delete('all')

        right = canvas.winfo_width()
        bottom = canvas.winfo_height()

        # draw the lines for the bar
        for x_pos, mode in [
            (25, 1), (35, 1),
            (55, 2), (65, 2), (75, 2),
            (95, 3), (105, 3),
            (125, 2), (135, 2), (145, 2),
            (165, 1), (175, 1)
        ]:
            width = 1
            dash = None
            match mode:
                case 2:
                    width = 2
                case 3:
                    dash = (3, 3)

            canvas.create_line(x_pos + 10, 0, x_pos + 10, bottom,
                               width=width,
                               dash=dash,
                               fill='black')

        self.top = 3
        lines = [(self.top, 2, right), (bottom - 3, 2, right)]
        hidden = grid.hidden
        self.step = bottom / grid.numerator

        pos = self.step
        for meas_line in range(1, grid.numerator):
            size = 30 if meas_line + 1 in hidden else right
            lines.append((pos, 1, size))
            pos += self.step

        for y_pos, width, size in lines:
            canvas.create_line(20, y_pos, size, y_pos,
                               width=width,
                               fill='black')

        txt_font = self.get_font(canvas, available=self.step - 6)

        for idx in range(0, grid.numerator):
            y_pos = 8 + idx * self.step
            x_pos = 10
            canvas.create_text(x_pos, y_pos, text=str(idx + 1), font=txt_font)

    def update(self, **kwargs):
        """ update the settings """

        if 'dct' in kwargs:
            kwargs = kwargs.get('dct', {})

        grid = Grid(dct=kwargs)
        self.selected(grid=grid)
