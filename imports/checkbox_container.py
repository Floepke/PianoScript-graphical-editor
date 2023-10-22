#! python3.11
# coding: utf8

""" Checkbutton container """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from typing import cast
from typing import Callable
from typing import Literal
from typing import LiteralString

from tkinter import Tk
from tkinter import Toplevel
from tkinter import Frame
from tkinter import Checkbutton
from tkinter import IntVar


class CheckBoxContainer:
    """ container for a Checkbutton """

    def __init__(self,
                 master: (Tk | Toplevel | Frame),
                 **kwargs):

        """ initialize the ChkContainer """
        self.frame = Frame(master)
        self.frame.grid(
            row=0,
            column=0,
            padx=1,
            pady=1,
            sticky='news')

        checked = int(kwargs.get('checked', 0))
        text = kwargs.get('text', '')

        state = kwargs.get('state', 'normal')

        self.chk_var = IntVar(
            master=self.frame,
            value=checked)

        self.check = Checkbutton(
            master=self.frame,
            text=text,
            state=state,
            onvalue=True,
            offvalue=False,
            variable=self.chk_var)

        self.check.grid(
            row=0,
            column=0,
            padx=0,
            pady=0,
            sticky='news')

        # do this now to prevent an early callback
        callback: Callable = kwargs.get('callback', None)
        self.chk_var.trace('w', callback)

    @property
    def checked(self) -> bool:
        """ whether the checkbox is checked or not """

        return bool(self.chk_var.get())

    @checked.setter
    def checked(self, value: bool):
        """ whether the checkbox is checked or not """

        self.chk_var.set(value=value)

    @property
    def this(self):
        """ return the checkbutton and the container """
        return self.check, self.frame

    @property
    def state(self):
        """ get the state """
        result = self.check.config()
        return result['state']

    @state.setter
    def state(self, value: LiteralString):
        """ set the state """

        # the alternative way, see also combobox_container.py
        self.check.config(state=cast(Literal, value))
