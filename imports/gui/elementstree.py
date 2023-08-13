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
        self.SortDir = True
        self.ignore_single_click = False
        self.selecteditem = 'note'

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

        # setup the elements_tree:
        self.elements_tree = [
            {
                "text":"Note",
                "id":"folder.note",
                "items":[
                    {
                        "id":"note",
                        "text":"Note",
                        "image":PhotoImage(Image.open(fp="icons/noteinput_R.png").resize((30,30)))
                    },
                    {
                        "id":"accidental",
                        "text":"Accidental",
                        "image":PhotoImage(Image.open(fp="icons/accidental.png").resize((30,30)))
                    },
                    {
                        "id":"beam",
                        "text":"Beam",
                        "image":PhotoImage(Image.open(fp="icons/beam.png").resize((30,30)))
                    }
                ]
            }
        ]

        # placing the elements tree in the treeview:
        for fld in self.elements_tree:
            # create folder
            folder = self.tree.insert(parent='',
                        id=fld['id'],
                        index='end',
                        text=' '+fld['text'],
                        open=True,
                        tag='folder'
                        )
            for it in fld['items']:
                self.tree.insert(parent=folder,
                            id=it['id'],
                            index='end',
                            text=' '+it['text'],
                            image=it['image']
                            )

        self.tree.bind("<ButtonPress-1>", self.on_single_click)
        #self.tree.bind("<Double-1>", self.on_single_click)

        self.tree.selection_set(self.selecteditem)

        # stylize folder looks
        self.tree.tag_configure('folder', background=color_gui_dark, foreground=color_dark, font=('courier', 16, 'bold'))

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
    
    def set(self, element: str):
        self.tree.selection_set(element)