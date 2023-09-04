#! python3.11
# coding: utf-8

""" grid editor proposal """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from tkinter import Frame
from tkinter import Toplevel
from tkinter import Label

from typing import Callable
from typing import cast

from PIL import ImageTk
from PIL import Image

from imports.grid import Grid
from imports.grid import GridList
from imports.grid_helper import GridHelper

from imports.treeview_container import Treeview_Container
from imports.prompt import Prompt

from imports.edit_measure import EditMeasure
from imports.show_measure import ShowMeasure


# py-lint: disable=too-many-instance-attributes
class Gredit:
    """ the grid editor class """

    def __init__(self,
                 master: Toplevel,
                 grids: dict,
                 on_save: Callable):
        """ initialize the class """

        self.master = master
        self.master.title('Grid editor')
        self.set_window_icon()

        self.initialized = False
        self._on_save = on_save

        self._context = [
            ('move up', self._move_up),
            ('move down', self._move_down)
        ]

        self.grid_list = None

        self.tree = None
        self.create_treeview(master=self.master,
                             row=0,
                             column=0,
                             padx=2,
                             pady=2,
                             sticky='news')

        self._create_label_result(master=self.master,
                                  row=1,
                                  column=0,
                                  columnspan=2,
                                  padx=2,
                                  pady=2,
                                  sticky='news')

        self._create_settings_frame(master=self.master,
                                    row=0,
                                    column=1,
                                    padx=0,
                                    pady=0,
                                    sticky='news')

        grid_list = GridList()
        for item in grids:
            grid_list.append(index=item['grid'], grid=Grid(dct=item))

        self.edit_measure.update_settings= self._update_settings
        self.edit_measure.save_file = self._save_file
        self.edit_measure.change_callback = self._value_changed
        self.show_measure.on_result = self._on_result
        self.edit_measure.initialized = True

        self.display_grids(grid_list)

    def _create_label_result(self, master, **kwargs):
        """ the result label """

        self._label_result = Label(master=master,
                                   text='range',
                                   anchor='w',
                                   justify='left',
                                   height=1,
                                   background='white')

        self._label_result.grid(row=kwargs.get('row', 1),
                                column=kwargs.get('column', 0),
                                columnspan=kwargs.get('columnspan', 2),  # noqa
                                padx=kwargs.get('padx', 2),  # noqa
                                pady=kwargs.get('pady', 2),  # noqa
                                sticky=kwargs.get('sticky', 'news'))

    def _create_settings_frame(self, master, **kwargs):
        """ two sub-frames: edit and display"""

        settings_frame = Frame(master)
        self.edit_measure = EditMeasure(master=settings_frame,
                                        row=0,
                                        column=0)

        self.show_measure = ShowMeasure(master=settings_frame,
                                        start=1,
                                        finish=2,
                                        row=5,
                                        column=0,
                                        on_result=self._on_result)

        settings_frame.grid(row=kwargs.get('row', 0),
                            column=kwargs.get('column', 1),
                            padx=kwargs.get('padx', 0),  # noqa
                            pady=kwargs.get('pady', 0),  # noqa
                            sticky=kwargs.get('sticky', 'news'))

    def set_window_icon(self):
        """ the image in the title bar """

        png = Image.open('./icons/GridEditor.png')
        photo = ImageTk.PhotoImage(png)
        self.master.iconphoto(False, cast(Image, photo))

    def _on_result(self, grid: Grid):
        """ show the pianoticks """

        value = GridHelper.to_pianoticks(grid)

        self._label_result.config(text=value)
        self.edit_measure.set_hidden(grid.hidden)

    def _value_changed(self, *args):
        """ some value changed """

        assert len(args) == 2  # these are provided by tkinter

        if not self.initialized:
            return

        values = self.edit_measure.get_values()
        if values is None:
            return

        self.show_measure.update(dct=values)

    def _update_settings(self, **kwargs):
        """ store back the settings """

        mode = kwargs.get('mode', 'update')

        dct = kwargs.get('dct', {})

        # remove hidden lines that are out of bounds
        numerator = dct.get('numerator', 0)
        dct['hidden'] = [line for line in dct['hidden'] if line <= numerator]

        grid = Grid(dct=dct)

        match mode:

            case 'update':
                self.tree.populate_row(grid=grid)
                grids = self.get_grids()
                grids.renumber()
                self.display_grids(grid_list=grids)
                self.show_measure.update(dct=dct)

            case 'append':
                grids = self.get_grids()
                number = dct.get('ident', -1)
                grids.append(index=number, grid=grid)
                self.display_grids(grid_list=grids)

            case 'delete':
                number = dct.get('ident', -1)
                grids = self.get_grids()
                grids.remove(number=number)
                self.display_grids(grid_list=grids)

            case _:
                self.prompt(message=f'unknown mode {mode}')

    def prompt(self, message: str = 'Nothing to report'):
        """ create a simple prompt window """

        _ = Prompt(root=self.master,
                   title='Notification',
                   message=message,
                   timeout_s=10)

    def _save_file(self):
        """ save results to file """

        if self._on_save is not None:
            # save information back

            result = []
            for item in self.get_grids().lst:
                result.append(item.to_dict())

            self._on_save(result)

    def get_grids(self) -> GridList:
        """ return the grids """

        result = GridList()
        tree = self.tree.tree

        ident = 1
        for child in tree.get_children():
            values = tree.item(child).get('values', [])
            grid = GridHelper.from_row(ident=str(ident), values=values)
            result.append(index=None, grid=grid)
            ident += 1

        return result

    def _on_main_close(self):
        """ window is closed """

        # on_exit = self._setup.get('on_exit', None)
        # if on_exit:
            # on_exit()

        self.master.destroy()

    def create_treeview(self,
                        master: Toplevel,
                        **kwargs):
        """ a treeview for the results """

        width = 120
        self.master = Frame(master)

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

        self.tree = Treeview_Container(master=self.master,
                                       double_click=self.on_double_click,
                                       single_click=self.on_single_click,
                                       context=self._context,
                                       height=height,
                                       width=width,
                                       dct=dct)

        self.tree.grid(row=0, column=0, sticky='news')
        self.tree.grid_columnconfigure(index=0, weight=1)

        self.master.grid(
            row = kwargs.get('row', 0),
            column = kwargs.get('column', 0),
            padx = kwargs.get('padx', 2),
            pady = kwargs.get('pady', 2),
            sticky = kwargs.get('sticky', 'news'))

        return self.master

    def on_double_click(self,
                        ident: str,
                        region: str,
                        column: str,
                        values: []):
        """ item was double clicked """

        print(f'double click {ident} region {region}')
        if region == 'cell':
            print(f'value [{column}] = {values[column]}')

    def on_single_click(self,
                        ident: str,
                        region: str,
                        column: int,
                        values: []):
        """ item was single clicked """

        assert column
        if region == 'cell':
            if not self.edit_measure.ready():
                return

            grid = GridHelper.from_row(ident=ident, values=values)
            self.edit_measure.selected(grid=grid)
            self.show_measure.selected(grid=grid)

    def display_grids(self, grid_list: GridList):
        """ save and display the grid list """

        self.grid_list = grid_list
        items = []
        lines = 1
        start = 1

        for item in grid_list.lst:
            start += item.amount

            ident = str(lines)
            dct = {'ident': ident,
                   'img_name': 'GridEditor',
                   'text': f'grid {lines}',
                   'parent': '',
                   'values': GridHelper.to_row(item),
                   }
            items.append(dct)
            lines += 1

        self.tree.populate(items=items)

    def _move_up(self, ident: str):
        """ move a row up """

        index = int(ident) - 1
        if index < 1:
            return

        if not self.edit_measure.ready():
            return

        lst = self.grid_list
        lst.swap(index - 1, index)

        self.display_grids(lst)

    def _move_down(self, ident: str):
        """ move a row down """

        lst = self.grid_list

        # the indices start from 1
        index = int(ident) - 1

        # out of range?
        if index >= len(lst) - 1:
            return

        if not self.edit_measure.ready():
            return

        lst.swap(index, index + 1)

        self.display_grids(lst)
