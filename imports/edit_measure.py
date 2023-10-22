#! python3.11
# coding: utf-8

""" grid editor proposal """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from tkinter import Frame
from tkinter import Label
from tkinter import Button
from tkinter import Canvas
from tkinter.font import Font

from typing import Any
from typing import Callable

from imports.spin_box_container import SpinboxContainer
from imports.checkbox_container import CheckBoxContainer
from imports.combobox_container import ComboBoxContainer

from imports.grid import Grid


# pylint: disable=too-many-instance-attributes
class EditMeasure:
    """ edit the values of a range of measures """

    def __init__(self, master: Frame, **kwargs):
        """ initialize the class """

        self._master = master
        self.start = None
        self._ident = None
        self.hidden = []
        self.save_file = None
        self._initialized = False
        self.update_settings: Callable = kwargs.get('update_settings', None)
        self.top = 1
        self.finish = 2
        self.step = 1

        # --- amount
        select_frame = Frame(master)

        state = 'disabled'

        self.select_label = Label(master=select_frame,
                                  text='Selected:',
                                  anchor='w',
                                  width=12)

        self.select_label.grid(row=0,
                               column=0,
                               padx=2,
                               pady=2,
                               sticky='news')

        self.select_value = Label(master=select_frame,
                                  text='None',
                                  anchor='w',
                                  width=8)

        self.select_value.grid(row=0,
                               column=1,
                               padx=2,
                               pady=2,
                               sticky='news')

        select_frame.grid(row=0,
                          column=0,
                          padx=0,
                          pady=0,
                          sticky='wns')

        start_frame = Frame(master)
        self.spin_start = SpinboxContainer(master=start_frame,
                                           label='Start',
                                           label_width=12,
                                           width=3,
                                           min_value=1,
                                           max_value=999,
                                           value=0,
                                           changed=self._value_changed,
                                           state='disabled')
        self.spin_start.frame.grid(row=0,
                                   column=0,
                                   padx=2,
                                   pady=2,
                                   sticky='news')

        self.visible = CheckBoxContainer(master=start_frame,
                                         text='Visible',
                                         callback=self._value_changed,
                                         state=state,
                                         tag='visible')
        _, check_frame = self.visible.this

        check_frame.grid(row=0,
                         column=2,
                         padx=(10, 2),
                         pady=2,
                         sticky='news')

        start_frame.grid(row=1,
                         column=0,
                         padx=0,
                         pady=0,
                         sticky='wns')

        self.spin_amount = SpinboxContainer(master=master,
                                            label='Amount',
                                            label_width=12,
                                            min_value=1,
                                            max_value=999,
                                            width=3,
                                            value=0,
                                            changed=self._value_changed,
                                            state=state)
        self.spin_amount.frame.grid(row=2,
                                    column=0,
                                    padx=2,
                                    pady=2,
                                    sticky='news')

        signature_frame = Frame(master)

        # ---- numerator
        self.spin_numer = SpinboxContainer(master=signature_frame,
                                           label='Signature',
                                           label_width=12,
                                           min_value=1,
                                           max_value=100,
                                           value=0,
                                           width=3,
                                           changed=self._value_changed,
                                           state=state)

        self.spin_numer.frame.grid(row=0,
                                   column=0,
                                   padx=(2, 0),
                                   pady=0,
                                   sticky='news')

        # ---- denominator

        values = [1, 2, 4, 8, 16, 32, 64, 128]
        self.combobox = ComboBoxContainer(master=signature_frame,
                                          prefix=None,
                                          prefix_width=10,
                                          value=1,
                                          width=4,
                                          values=values,
                                          state=state,
                                          callback=self._value_changed)

        self.combobox.frame.grid(row=0,
                                 column=1,
                                 padx=(0, 2),
                                 pady=0,
                                 sticky='news')

        signature_frame.grid(row=3,
                             column=0,
                             padx=0,
                             pady=0,
                             sticky='news')

        self.button_frame = Frame(master)

        self.add_button = Button(master=self.button_frame,
                                 text='Add',
                                 width=6,
                                 command=self._add)

        self.add_button.grid(row=0,
                             column=0,
                             padx=0,
                             pady=2,
                             sticky='news')

        self.del_button = Button(master=self.button_frame,
                                 text='Delete',
                                 width=6,
                                 command=self._del)

        self.del_button.grid(row=0,
                             column=1,
                             padx=0,
                             pady=2,
                             sticky='news')

        self.button_frame.grid(row=4,
                               column=0,
                               padx=4,
                               pady=0,
                               sticky='nsw')

        self._canvas_frame = Frame(master)
        self._canvas = Canvas(master=self._canvas_frame,
                              background='black',
                              width=200,
                              height=270)

        self._canvas.configure(bg='white')
        self._canvas.bind('<Button-1>', self.left_click)

        self._canvas.grid(row=5,
                          rowspan=1,
                          column=0,
                          padx=(4, 4),
                          pady=2,
                          sticky='ns')

        self._canvas_frame.grid(row=5,
                                column=0,
                                padx=0,
                                pady=0,
                                sticky='news')

    def left_click(self, event):
        """ left click on canvas """

        if not self._initialized:
            return

        self.top = 3
        bottom = self._canvas.winfo_height()
        self.step = bottom / self.spin_numer.value

        pos = 1 + int(round((event.y - self.top) / self.step))

        if pos in self.hidden:
            self.hidden.remove(pos)
        else:
            self.hidden.append(pos)
            self.hidden.sort()

        self.update()

    def _value_changed(self, name: str, value: Any, mode: str):
        """ the value has changed, callback when initialized """

        assert name  # parameter is not used
        assert value is not None  # parameter is not used
        assert mode is not None  # parameter is not used

        if not self._initialized or self._ident is None:
            return

        self.update()

    def _insert(self):
        """ insert """

        self.update(mode='insert')

    def _add(self):
        """ add a set """

        self.update(mode='append')

    def _del(self):
        """ delete current set """

        self.update(mode='delete')

    def get_values(self) -> dict:
        """ return the current values as dictionary  """

        grid = self._ident
        num = int(self.spin_numer.value)
        den = int(self.combobox.value)

        return {
            'grid': str(grid),
            'start': int(self.spin_start.value),
            'amount': int(self.spin_amount.value),
            'numerator': num,
            'denominator': den,
            'signature': f'{num}/{den}',
            'visible': self.visible.checked,
            'hidden': self.hidden
        }

    def update(self, mode: str = 'update'):
        """ save the settings back """

        if self._ident is None or not self._initialized:
            return

        if self.update_settings is not None:
            # print('call update_settings')
            self.update_settings(mode=mode,
                                 dct=self.get_values())

        self.draw_measure()

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

    # pylint: disable=too-many-locals
    def draw_measure(self):
        """ draw the measure counting lines """
        self._canvas.delete('all')

        numerator = self.spin_numer.value
        right = self._canvas.winfo_width()
        bottom = self._canvas.winfo_height()

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

            self._canvas.create_line(x_pos + 10, 0, x_pos + 10, bottom,
                                     width=width,
                                     dash=dash,
                                     fill='black')

        self.top = 3
        lines = [(self.top, 2, right), (bottom - 3, 2, right)]
        hidden = self.hidden
        self.step = bottom / numerator

        pos = self.step
        for meas_line in range(1, numerator):
            size = 30 if meas_line + 1 in hidden else right
            lines.append((pos, 1, size))
            pos += self.step

        for y_pos, width, size in lines:
            self._canvas.create_line(20, y_pos, size, y_pos,
                                     width=width,
                                     fill='black')

        txt_font = self.get_font(self._canvas, available=self.step - 6)

        for idx in range(0, numerator):
            y_pos = 8 + idx * self.step
            x_pos = 10
            self._canvas.create_text(x_pos, y_pos, text=str(idx + 1), font=txt_font)

    def selected(self, grid: Grid):
        """ a row in the table is selected """

        # no callback while setting the values
        self._initialized = False

        self._ident = grid.grid
        txt = '' if self._ident is None else str(self._ident)
        self.select_value.config(text=f'grid {txt}')

        combo_state = 'readonly'
        new_state = 'normal'
        if self._ident is None:
            combo_state = 'disabled'
            new_state = 'disabled'

        self.spin_start.state = 'disabled'  # never 'normal'
        self.spin_amount.state = new_state
        self.spin_numer.state = new_state
        self.combobox.state = combo_state
        self.visible.state = new_state

        if self._ident is None:
            return

        self.spin_start.value = grid.start
        self.spin_amount.value = grid.amount
        self.spin_numer.value = grid.numerator
        self.combobox.value = grid.denominator  # noqa
        self.visible.checked = grid.visible
        self.hidden = grid.hidden

        self.draw_measure()

        # ready for changes
        self._initialized = True

    def set_hidden(self, hidden: []):
        """ set the hidden result from show_measure"""

        self.hidden = hidden
