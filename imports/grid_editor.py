#! python3.11
# coding: utf-8

""" grid editor proposal """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from tkinter import Frame
from tkinter import Toplevel
from tkinter import Label

from typing import cast
from typing import Callable

from PIL import ImageTk
from PIL import Image

from imports.grid import Grid
from imports.grid import GridList
from imports.grid_helper import GridHelper

from imports.treeviewcontainer import TreeviewContainer

from imports.edit_measure import EditMeasure


# pylint: disable=too-many-instance-attributes
class Gredit:
    """ the grid editor class """

    def __init__(self,
                 master: Toplevel,
                 list_grids: [dict],
                 on_close: Callable):
        """ initialize the class """

        # print(f'Gr_edit           {id(self)}')

        self.master = master
        self.master.title('Grid editor')
        self.master.protocol("WM_DELETE_WINDOW", self._close)
        self.on_close = on_close

        self.set_window_icon()
        self.edit_measure = None
        self.treeview_master = None
        self.grid_list = None

        self._context = [
            ('move up', self._move_up),
            ('move down', self._move_down)
        ]

        self.tree_container = self.create_treeview(master=self.master)
        self.tree = self.tree_container.control

        self.tree.grid_columnconfigure(
            index=0,
            weight=1)

        self.tree.grid(
            row=0,
            column=0,
            padx=2,
            pady=2,
            sticky='news')

        self._create_label_result(
            master=self.master,
            row=1,
            column=0,
            columnspan=2,
            padx=2,
            pady=2,
            sticky='news')

        self.settings_frame = Frame(master)
        self.edit_measure = EditMeasure(
            master=self.settings_frame,
            update_settings=self._update_settings)

        self.settings_frame.grid(
            row=0,
            column=1,
            padx=0,
            pady=0,
            sticky='news')

        glist = GridList()
        for index, item in enumerate(list_grids, 1):
            glist.append(index=index, grid=Grid(dct=item))

        self.display_grids(glist)
        pass

    def _close(self):
        """ close the editor window """

        if self.on_close is not None:
            self.on_close()

        self.master.destroy()

    @property
    def result(self) -> list:
        """ return the resulting grid list """

        grids = self.get_grids()
        lst = [grid.to_dict() for grid in grids.lst]
        return lst

    def _create_label_result(self, master, **kwargs):
        """ the result label """

        label_result = Label(master=master,
                             text='range',
                             anchor='w',
                             justify='left',
                             height=1,
                             background='white')

        label_result.grid(row=kwargs.get('row', 1),
                          column=kwargs.get('column', 0),
                          columnspan=kwargs.get('columnspan', 2),  # noqa
                          padx=kwargs.get('padx', 2),  # noqa
                          pady=kwargs.get('pady', 2),  # noqa
                          sticky=kwargs.get('sticky', 'news'))

        self._label_result = label_result

    def set_window_icon(self):
        """ the image in the title bar """

        png = Image.open('./icons/GridEditor.png')
        photo = ImageTk.PhotoImage(png)
        self.master.iconphoto(False, cast(Image, photo))

    def _on_result(self, grid: Grid):
        """ show the pianoticks """

        value = GridHelper.to_pianoticks(grid)

        self._label_result.config(text=value)

    def _update_settings(self, **kwargs):
        """ store back the settings """

        mode = kwargs.get('mode', 'update')

        dct = kwargs.get('dct', {})

        # remove hidden lines that are out of bounds
        numerator = dct.get('numerator', 0)
        dct['hidden'] = [line for line in dct['hidden'] if line <= numerator]

        grid = Grid(dct=dct)
        self._on_result(grid=grid)

        match mode:

            case 'update':
                self.tree_container.populate_row(grid=grid)
                grids = self.get_grids()
                grids.renumber()
                self.display_grids(grid_list=grids)

            case 'append':
                grids = self.get_grids()
                number = dct.get('grid', -1)
                grids.append(index=number, grid=grid)
                self.display_grids(grid_list=grids)

            case 'delete':
                number = int(dct.get('grid', -1))
                grids = self.get_grids()
                grids.remove(number=number)
                self.display_grids(grid_list=grids)

    def get_grids(self) -> GridList:
        """ return the grids """

        result = GridList()

        ident = 1
        for child in self.tree.get_children():
            values = self.tree.item(child).get('values', [])
            grid = GridHelper.from_row(grid=str(ident), values=values)
            result.append(index=None, grid=grid)
            ident += 1

        return result

    def create_treeview(self,
                        master: Toplevel):
        """ a treeview for the results """

        width = 120
        self.treeview_master = master  # Frame(master)

        dct = {'row_height': 24,
               'headings': ('headings', 'tree'),
               'columns': [('number', 'grid', 80),  # index in the tree
                           ('start', 'start', 30),
                           ('amount', 'amount', 50),
                           ('signature', 'signature', 60),
                           ('visible', 'visible', 40),
                           ('hidden', 'hidden', 120),
                           ]
               }

        height = 200

        container = TreeviewContainer(
            master=self.treeview_master,
            single_click=self.on_single_click,
            context=self._context,
            height=height,
            width=width,
            dct=dct)

        return container

    def on_single_click(self,
                        ident: str,
                        region: str,
                        column: int,
                        values: []):
        """ item was single clicked """

        assert column is not None
        if region == 'cell':

            grid = GridHelper.from_row(grid=ident, values=values)
            self.edit_measure.selected(grid=grid)
            self._on_result(grid=grid)

            # re-activate the row
            self.tree.selection_set(grid.grid)

    def display_grids(self, grid_list: GridList):
        """ save and display the grid list """

        self.grid_list = grid_list
        items = []
        lines = 1
        start = 1

        for item in grid_list.lst:
            start += item.amount

            dct = {'grid': item.grid,
                   'img_name': 'GridEditor',
                   'text': f'grid {lines}',
                   'parent': '',
                   'values': GridHelper.to_row(item),
                   }
            items.append(dct)
            lines += 1

        self.tree_container.populate(items=items)

    def _move_up(self, ident: str):
        """ move a row up """

        index = int(ident) - 1
        if index < 1:
            return

        self._complete_move(index, index - 1)

    def _move_down(self, ident: str):
        """ move a row down """

        lst = self.grid_list

        # the indices start from 1
        index = int(ident) - 1

        # out of range?
        if index >= len(lst) - 1:
            return

        self._complete_move(index, index + 1)

    def _complete_move(self, source, target):
        """ do the move """

        # rows start at 0
        grids = self.grid_list
        grids.swap(source, target)

        self.display_grids(grids)
        self.edit_measure.selected(grid=grids.lst[target])
