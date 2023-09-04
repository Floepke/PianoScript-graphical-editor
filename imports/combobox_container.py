#! python3.11
# coding: utf8

""" Checkbutton container """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from typing import Callable
from typing import LiteralString

from tkinter import Tk
from tkinter import Toplevel
from tkinter import Frame
from tkinter import Label
from tkinter import StringVar
from tkinter.ttk import Combobox


class ComboBoxContainer:
    """ container for a Checkbutton """

    def __init__(self,
                 master: (Tk | Toplevel | Frame),
                 **kwargs):

        """ initialize the ChkContainer """
        self._frame = Frame(master)

        prefix = kwargs.get('prefix', None)

        value = kwargs.get('value', '')
        values: [str] = kwargs.get('values', False)

        width = kwargs.get('width', 4)
        tag = kwargs.get('tag', None)
        state = kwargs.get('state', 'normal')
        self.callback: Callable = kwargs.get('callback', None)

        col = 0
        if prefix is not None:
            prefix_width = kwargs.get('prefix_width', 4)

            self.label = Label(master=self._frame,
                               text=prefix,
                               width=prefix_width,
                               justify = 'left',
                               anchor = 'w')

            self.label.grid(row=0,
                            column=col,
                            padx=2,
                            pady=2,
                            sticky='w')
            col += 1

        self.cmb_var = StringVar(
            master=self._frame,
            name=tag,
            value=value)

        self.cmb_var.trace('w', self.invoke_callback)

        self.combo = Combobox(
            master=self._frame,
            width=width,
            state=state,
            textvariable=self.cmb_var,
            values=values)

        self.combo.grid(row=0,
                        column=col,
                        padx=2,
                        pady=2,
                        sticky='w')

    @property
    def value(self) -> str:
        """ get the value """

        return self.cmb_var.get()

    @value.setter
    def value(self, value):
        """ set the value """

        self.cmb_var.set(value)

    def invoke_callback(self, name: str, _: str, mode: str):
        """ when specified, do the callback """

        if self.callback:
            value = self.cmb_var.get()
            self.callback(name, value, mode)

    @property
    def frame(self):
        """ return the checkbutton and the container """
        return self._frame

    @property
    def state(self):
        """ get the state """

        return self.combo.config()['state']

    @state.setter
    def state(self, value: LiteralString):
        """ set the state
            the state is supposed to be a Literal,
            like this: Literal['normal']
        """

        # print(value)
        self.combo.config(state=value)
