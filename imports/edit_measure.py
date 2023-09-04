#! python3.11
# coding: utf-8

""" grid editor proposal """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2023 all rights reserved'  # noqa

from tkinter import Frame
from tkinter import Label
from tkinter import Button

from typing import Optional
from typing import Any

from imports.spin_box_container import SpinboxContainer
from imports.checkbox_container import CheckBoxContainer
from imports.combobox_container import ComboBoxContainer

from imports.prompt import PromptEnum
from imports.prompt import Prompt

from imports.grid import Grid


# pylint: disable=too-many-instance-attributes
class EditMeasure:
    """ edit the values of a range of measures """

    def __init__(self, master: Frame,
                 **kwargs):
        """ initialize the class """

        self._master = master
        self._dirty = False
        self.update_settings = None
        self.change_callback = None
        self.save_file = None
        self.start = None
        self._ident = None
        self.prm = None
        self.hidden = []

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
                                           # leading_zero=True,
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

        self.spin_update = Button(master=self.button_frame,
                                  text='Update',
                                  width=6,
                                  command=self.measure_update)

        self.spin_update.grid(row=0,
                              column=0,
                              padx=0,
                              pady=2,
                              sticky='news')

        self.add_button = Button(master=self.button_frame,
                                 text='Add',
                                 width=6,
                                 command=self._add)

        self.add_button.grid(row=0,
                             column=1,
                             padx=0,
                             pady=2,
                             sticky='news')

        self.del_button = Button(master=self.button_frame,
                                 text='Delete',
                                 width=6,
                                 command=self._del)

        self.del_button.grid(row=0,
                             column=2,
                             padx=0,
                             pady=2,
                             sticky='news')

        self._save_file = Button(master=self.button_frame,
                                 text='Save',
                                 width=6,
                                 command=self._save)

        self._save_file.grid(row=0,
                             column=3,
                             padx=0,
                             pady=2,
                             sticky='news')

        self.button_frame.grid(row=4,
                               column=0,
                               padx=4,
                               pady=0,
                               sticky='nsw')


    def ready(self):
        """ ready to accept data """

        if self._dirty:
            self.prompt('Settings were not saved')

        return not self._dirty

    def prompt(self, message: str = 'Nothing to report'):
        """ create a simple prompt window """

        if self.prm is None:
            self.prm = Prompt(root=self._master,
                              title='Notification',
                              message=message,
                              timeout_s=5,
                              callback=self._callback,
                              closing=self._prompt_closing)
        else:
            self.prm.update(message=message,
                            timeout_s=5)

    def _prompt_closing(self):
        """ prompt is closing """

        self.prm = None

    def _callback(self, response: PromptEnum):
        """ clicked 'OK' or 'Cancel' """

        if response == PromptEnum.OK:
            self._dirty = False

    def _value_changed(self, name: str, value: Any, mode: str):
        """ the value has changed """

        assert mode  # parameter is not used
        if self.change_callback:
            self.change_callback(name, value)
            self._dirty = True

    def _insert(self):
        """ insert """

        self.measure_update(mode='insert')

    def _add(self):
        """ add a set """

        self.measure_update(mode='append')

    def _del(self):
        """ delete current set """

        self.measure_update(mode='delete')

    def _save(self):
        """ save the result to file """

        if self.save_file:
            self.save_file()

    def get_values(self) -> Optional[dict]:
        """ return the current values as dictionary  """

        ident = self._ident

        if ident is None:
            return None

        num = int(self.spin_numer.value)
        den = int(self.combobox.value)

        # print(f'edit_measure.get_values, hidden = {self.hidden}')

        return {
            'ident': str(ident),
            'start': int(self.spin_start.value),
            'amount': int(self.spin_amount.value),
            'numerator': num,
            'denominator': den,
            'signature': f'{num}/{den}',
            'visible': self.visible.checked,
            'hidden': self.hidden
        }

    def measure_update(self, mode: str = 'update'):
        """ save the settings back """

        # print(f'edit_measure._update, ident {self._ident} hidden {self.hidden}')
        if self._ident is None:
            return

        if self.update_settings is not None:
            self.update_settings(mode=mode,
                                 dct=self.get_values())
            self._dirty = False

    def selected(self, grid: Grid):
        """ a row in the table is selected """

        self._ident = grid.ident

        # print(f'selected: ident {self._ident} hidden: {self.hidden}')

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

        numer = grid.numerator
        denom = grid.denominator  # noqa

        # no callback while setting the values
        self.initialized = False

        self.spin_start.value = grid.start
        self.spin_amount.value = grid.amount
        self.spin_numer.value = numer
        self.combobox.value = denom
        self.visible.checked = grid.visible
        self.hidden = grid.hidden

        # ready for changes
        self.initialized = True

    def set_hidden(self, hidden: []):
        """ set the hidden result from show_measure"""

        self.hidden = hidden
