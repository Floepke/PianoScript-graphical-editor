#! python3.11
# coding: utf-8

""" display the help file of the player """

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


class Tree(Frame):

    def __init__(self, master, **kwargs):
        """ initialize the frame """

        # self.single_click: Callable = kwargs.get('single_click')
        # self.double_click: Callable = kwargs.get('double_click')
        self.SortDir = True
        self.ignore_single_click = False
        self.itemselected = 'right'

        Frame.__init__(self, master, width=100)

        self.dataCols = kwargs.get('columns',())
        show = ['headings' if kwargs.get('headings', False) else 'tree']
        self.tree = Treeview(self,
                             columns=self.dataCols,
                             show=show,
                             selectmode='browse',
                             height=32)

        self.tree.pack(fill='both')

        # for col in kwargs.get
        self.tree.column("#0", minwidth=90, width=90, stretch=True)
        self.tree.heading('#0', text='objects', anchor='w')

        style = ttk.Style(master)
        style.configure('Treeview', rowheight=32)

        # Node note:
        self.node_note = self.tree.insert(parent='',
                                id='folder.note',
                                index='end',
                                text=' Note',
                                open=True
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

        # Node layout:
        self.node_layout = self.tree.insert(parent='',
                                id='folder.layout',
                                index='end',
                                text=' Layout',
                                open=True
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

        img = Image.open(fp="icons/beam.png")
        img.resize((24,24))
        self.img_beam = PhotoImage(img)
        self.tree.insert(parent=self.node_layout,
                         id='beamtool',
                         index='end',
                         text=' Beam',
                         image=self.img_beam
                         )

        # Node lines
        self.node_lines = self.tree.insert(parent='',
                                id='folder.lines',
                                index='end',
                                text=' Lines',
                                open=True
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
                                text=' Text',
                                open=True
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
                                text=' Bar',
                                open=True
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

        self.tree.bind("<ButtonRelease-1>", self.on_single_click)

        self.tree.selection_set(self.itemselected)

    def on_single_click(self, event):
        """ single click on tree """

        if self.ignore_single_click:
            # print('ignore single click')
            self.ignore_single_click = False
            return

        item = self.tree.selection()
        # print(item)
        # if item[0].startswith('folder'):
        #     self.tree.selection_set(self.itemselected)
        #     return

        if item:
            who = self.tree.identify("item", event.x, event.y)
            if who == '':
                return

            message = f'left click {who}'
            id = item[0]
            who = self.tree.item(id)

            if id.startswith('folder'):
                # print(f'event.x is {event.x}')
                if event.x > 12:
                    open = not bool(who['open'])
                    self.tree.item(item[0], open=open)
                    #self.single_click('')
            else:
                self.itemselected = who

    @property
    def get(self):
        return self.tree.selection()[0]