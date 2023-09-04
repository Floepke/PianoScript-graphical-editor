#! python3.11
# coding: utf-8

from __future__ import annotations

""" Prompt: a simple message box """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from typing import Optional

from tkinter import Tk
from tkinter import Toplevel
from tkinter import Label
from tkinter import Button
from tkinter import Frame

from enum import Enum


class PromptEnum(Enum):
    NONE = 0
    OK = 1
    CANCEL = -1


# pylint: disable=too-few-public-methods
class Prompt:
    """ show a simple prompt to the user """

    def __init__(self, **kwargs):
        """ initialize the class and create a simple dialog """

        self.callback = kwargs.get('callback', None)
        self.closing = kwargs.get('closing', None)

        title = kwargs.get('title', 'Message')
        message = kwargs.get('message', 'no message provided')
        timeout = kwargs.get('timeout_s', 0) * 1000  # ms
        foreground = kwargs.get('foreground', 'black')
        background = kwargs.get('background', 'white')
        font: Optional[tuple] = kwargs.get('font', ('Comic Sans MS', 12, 'normal'))

        size: str = kwargs.get('size', '')
        root: [Tk, Toplevel] = kwargs.get('root', None)

        self.root = Tk() if root is None else Toplevel(master=root)
        self.root.protocol("WM_DELETE_WINDOW", self._done)
        self.root.title(title)
        self.root.attributes('-toolwindow', True)
        self.root.attributes('-topmost', True)
        self.after = None

        self.label = Label(master=self.root,
                           text=message,
                           justify='left',
                           font=font,
                           foreground=foreground,
                           background=background)

        self.label.grid(row=0,
                        column=0,
                        ipadx=10,
                        ipady=10,
                        padx=10,
                        pady=10,
                        sticky='news')

        button_frame = Frame(self.root)
        self.button = Button(master=button_frame,
                             text='OK',
                             width=7,
                             foreground=foreground,
                             background=background,
                             command=self._done_ok)

        self.button.grid(row=0,
                         column=0,
                         padx=2,
                         pady=8,
                         sticky='w')

        self.button = Button(master=button_frame,
                             text='Cancel',
                             width=7,
                             foreground=foreground,
                             background=background,
                             command=self._done_cancel)

        self.button.grid(row=0,
                         column=1,
                         padx=2,
                         pady=8,
                         sticky='e')

        button_frame.grid(row=1,
                          column=0,
                          padx=0,
                          pady=0,
                          sticky='ns')

        if timeout > 0:
            self.after = self.root.after(ms=timeout,
                                         func=self._done)

        # is this a stand-alone window?
        if root is None:
            self.root.mainloop()
        else:
            parent_left= root.winfo_x()
            parent_top = root.winfo_y()
            parent_width = root.winfo_width()
            parent_height = root.winfo_height()
            my_width = self.root.winfo_width()
            my_height = self.root.winfo_height()
            my_left = parent_left + int((parent_width - my_width) / 2)
            my_top = parent_top + int((parent_height - my_height) / 2)

            self.root.geometry(f'{size}+{my_left}+{my_top}')

    def update(self, **kwargs):
        """ prompt has not closed yet """

        if self.after is not None:
            self.root.after_cancel(self.after)

        timeout = kwargs.get('timeout_s', 0) * 1000  # ms
        message = kwargs.get('message', 'no message provided')
        self.label.config(text=message)

        if timeout > 0:
            self.after = self.root.after(ms=timeout,
                                         func=self._done)

    def _done_ok(self):
        """ OK clicked """

        if self.callback:
            self.callback(PromptEnum.OK)

        self._done()

    def _done_cancel(self):
        """ Cancel clicked """

        if self.callback:
            self.callback(PromptEnum.CANCEL)

        self._done()

    def _done(self):
        """ close the window """

        if self.closing:
            self.closing()

        self.root.destroy()
