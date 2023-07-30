#! python3.9.2
# coding: utf-8

'''
This file is part of the pianoscript project: http://www.pianoscript.org/

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files 
(the “Software”), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish, 
distribute, sublicense, and/or sell copies of the Software, and to permit 
persons to whom the Software is furnished to do so, subject to the 
following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR 
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
OTHER DEALINGS IN THE SOFTWARE.
'''

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from sys import exit as _exit

from typing import Callable

from PIL import Image
from tkinter import Tk

import tkinter.ttk as ttk
from tkinter.ttk import Frame
from tkinter.ttk import Treeview
from tkinter.ttk import Label

from PIL.ImageTk import PhotoImage

from imports.colors import *


class Tree(Frame):

    def __init__(self, master, **kwargs):
        """ initialize the frame """

        # self.single_click: Callable = kwargs.get('single_click')
        # self.double_click: Callable = kwargs.get('double_click')
        self.SortDir = True
        self.ignore_single_click = False
        self.selecteditem = 'right'

        Frame.__init__(self, master, width=100, relief='flat')

        self.dataCols = kwargs.get('columns',())
        show = ['headings' if kwargs.get('headings', False) else 'tree']
        self.tree = Treeview(self,
                             columns=self.dataCols,
                             show=show,
                             selectmode='none',
                             height=32,
                             padding=[-25,0,0,0])

        self.tree.pack(fill='both')

        # for col in kwargs.get
        self.tree.column("#0", minwidth=90, width=90, stretch=True)
        self.tree.heading('#0', text='objects', anchor='w')

        style = ttk.Style(master)
        style.configure('Treeview', rowheight=40)

        # Node note:
        self.node_note = self.tree.insert(parent='',
                                id='folder.note',
                                index='end',
                                text=' Note:',
                                open=True,
                                tag='folder'
                                )

        img = Image.open(fp="icons/noteinput_R.png")
        img.resize((24,24))
        self.img_noteinput_l = PhotoImage(img)
        self.tree.insert(parent=self.node_note,
                         id='right',
                         index='end',
                         text=' Right',
                         image=self.img_noteinput_l
                         )

        img = Image.open(fp="icons/noteinput_L.png")
        img.resize((24,24))
        self.img_noteinput_r = PhotoImage(img)
        self.tree.insert(parent=self.node_note,
                         id='left',
                         index='end',
                         text=' Left',
                         image=self.img_noteinput_r
                         )

        img = Image.open(fp="icons/accidental.png")
        img.resize((24,24))
        self.img_accidental = PhotoImage(img)
        self.tree.insert(parent=self.node_note,
                         id='accidental',
                         index='end',
                         text=' Accidental',
                         image=self.img_accidental
                         )

        img = Image.open(fp="icons/beam.png")
        img.resize((24,24))
        self.img_beam = PhotoImage(img)
        self.tree.insert(parent=self.node_note,
                         id='beamtool',
                         index='end',
                         text=' Beam',
                         image=self.img_beam
                         )

        # Node layout:
        self.node_layout = self.tree.insert(parent='',
                                id='folder.layout',
                                index='end',
                                text=' Layout:',
                                open=True,
                                tag='folder'
                                )

        img = Image.open(fp="icons/linebreak.png")
        img.resize((24,24))
        self.img_linebreak = PhotoImage(img)
        self.tree.insert(parent=self.node_layout,
                         id='linebreak',
                         index='end',
                         text=' Linebreak',
                         image=self.img_linebreak
                         )

        img = Image.open(fp="icons/staffspacer.png")
        img.resize((24,24))
        self.img_staffsizer = PhotoImage(img)
        self.tree.insert(parent=self.node_layout,
                         id='staffsizer',
                         index='end',
                         text=' Staffsizer',
                         image=self.img_staffsizer
                         )

        # Node lines
        self.node_lines = self.tree.insert(parent='',
                                id='folder.lines',
                                index='end',
                                text=' Lines:',
                                open=True,
                                tag='folder'
                                )

        img = Image.open(fp="icons/countline.png")
        img.resize((24,24))
        self.img_countline = PhotoImage(img)
        self.tree.insert(parent=self.node_lines,
                         id='countline',
                         index='end',
                         text=' Countline',
                         image=self.img_countline
                         )

        img = Image.open(fp="icons/slur.png")
        img.resize((24,24))
        self.img_slur = PhotoImage(img)
        self.tree.insert(parent=self.node_lines,
                         id='slur',
                         index='end',
                         text=' Slur',
                         image=self.img_slur
                         )

        # Node text
        self.node_text = self.tree.insert(parent='',
                                id='folder.text',
                                index='end',
                                text=' Text:',
                                open=True,
                                tag='folder'
                                )

        img = Image.open(fp="icons/text.png")
        img.resize((24,24))
        self.img_text = PhotoImage(img)
        self.tree.insert(parent=self.node_text,
                         id='text',
                         index='end',
                         text=' Text',
                         image=self.img_text
                         )

        # Node bar
        self.node_bar = self.tree.insert(parent='',
                                id='folder.bar',
                                index='end',
                                text=' Bar:',
                                open=True,
                                tag='folder'
                                )

        img = Image.open(fp="icons/repeats.png")
        img.resize((24,24))
        self.img_repeats = PhotoImage(img)
        self.tree.insert(parent=self.node_bar,
                         id='repeats',
                         index='end',
                         text=' Repeats',
                         image=self.img_repeats
                         )

        self.tree.bind("<ButtonPress-1>", self.on_single_click)
        self.tree.bind("<Double-1>", self.on_single_click)

        self.tree.selection_set(self.selecteditem)

        # stylize folder looks
        self.tree.tag_configure('folder', background=color_gui_contrast, foreground=color_dark, font=('courier', 16, 'bold'))

    def on_single_click(self, event):
        """ single click on tree """
        item = self.tree.selection()
        if item:
            iid = self.tree.identify("item", event.x, event.y)
            element = self.tree.item(iid)
            if not iid.startswith('folder'):
                self.selecteditem = iid
                self.tree.selection_set(iid)
            elif iid.startswith('folder'):
                open = not bool(element['open'])
                self.tree.item(iid, open=open)

    #TODO: Scroll fix

    @property
    def get(self):
        return self.selecteditem