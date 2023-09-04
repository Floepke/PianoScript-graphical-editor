#! python3.11
# coding: utf8

""" Checkbutton container """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from typing import cast
from typing import Callable
from typing import Optional
from typing import Literal
from typing import LiteralString

from tkinter import Tk
from tkinter import Toplevel
from tkinter import Frame
from tkinter import Checkbutton
from tkinter import BooleanVar


class CheckBoxContainer:
    """ container for a Checkbutton """

    def __init__(self,
                 master: (Tk | Toplevel | Frame),
                 **kwargs):

        """ initialize the ChkContainer """
        self.frame = Frame(master)
        self.callback: Optional[Callable] = None
        checked: bool = kwargs.get('checked', False)
        text = kwargs.get('text', '')
        tag = kwargs.get('tag', None)
        state = kwargs.get('state', 'normal')

        self.chk_var = BooleanVar(
            master=self.frame,
            name=tag,
            value=checked)

        self.chk_var.trace('w', self.invoke_callback)

        self.check = Checkbutton(
            master=self.frame,
            text=text,
            state=state,
            variable=self.chk_var)

        self.check.grid(row=0, column=0)

        self.callback: Callable = kwargs.get('callback', None)

    def invoke_callback(self, name: str, _: str, mode: str):
        """ when specified, to the callback """

        if self.callback:
            value = self.chk_var.get()
            self.callback(name, value, mode)

    @property
    def checked(self) -> bool:
        """ whether the checkbox is checked or not """

        return self.chk_var.get()

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
