#!python3.11
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

from imports.colors import color_gui_light, color_dark, color_light, color_highlight, color_gui_dark
from tkinter import Frame, Label, Listbox, StringVar, Spinbox

class GridSelector(Frame):
    """docstring for GridSelector"""
    def __init__(self, master):
        self.master = master
        Frame.__init__(self, master)
        
        self.gridselector_frame = self
        self.gridselector_frame.grid_columnconfigure(0,weight=1)
        
        # add gridselector widgets:
        self.noteinput_label = Label(self.gridselector_frame, text='GRID:', bg=color_gui_light, 
            fg=color_gui_dark, anchor='w', font=("courier", 16, 'bold'))
        self.noteinput_label.grid(column=0, row=0, sticky='ew')
        
        # the grid base selector:
        self.list_dur = Listbox(self.gridselector_frame, height=8, bg=color_light, 
            selectbackground=color_highlight,selectforeground=color_dark, 
            fg=color_dark, font=('courier', 16, 'bold'))
        self.list_dur.grid(column=0, row=1, sticky='ew')
        lst_labels = ['1', '2', '4', '8', '16', '32', '64', '128']
        for index, element in enumerate(lst_labels):
            self.list_dur.insert(index,element)
        self.list_dur.select_set(3) # default = 8 (eight note)
        
        # divide selector:
        self.divide_label = Label(self.gridselector_frame, text='÷', font=("courier", 20, "bold"), 
            bg=color_gui_light, fg=color_gui_dark, anchor='c')
        self.divide_label.grid(column=0, row=2, sticky='ew')
        self.divide_variable = StringVar(value=1)
        self.divide_spin = Spinbox(self.gridselector_frame, from_=1, to=99, bg=color_light, 
            fg=color_dark, font=('courier', 16, 'bold'), 
            textvariable=self.divide_variable)
        self.divide_spin.grid(column=0, row=3, sticky='ew')
        
        # times selector:
        self.times_label = Label(self.gridselector_frame, text='×', font=("courier", 20, "bold"), 
            bg=color_gui_light, fg=color_gui_dark, anchor='c')
        self.times_label.grid(column=0, row=4, sticky='ew')
        self.times_variable = StringVar(value=1)
        self.times_spin = Spinbox(self.gridselector_frame, from_=1, to=99, bg=color_light, 
            fg=color_dark, font=('courier', 16, 'bold'), textvariable=self.times_variable)
        self.times_spin.grid(column=0, row=5, sticky='ew')
        
        # seperator:
        self.seperator_1 = Label(self.gridselector_frame, 
            text='------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', 
            bg=color_gui_light, fg='#c8c8c8', anchor='c', font=("courier"))
        self.seperator_1.grid(column=0, row=6, sticky='ew')

        # bind listbox callback
        self.list_dur.bind("<<ListboxSelect>>", self.reset_on_click)

    def reset_on_click(self, event=''):
        
        self.divide_variable.set(1)
        self.times_variable.set(1)

    def get(self):
        '''get the value of the grid in pianoticks'''
        lengthdict = {1: 1024, 2: 512, 4: 256, 8: 128, 16: 64, 32: 32, 64: 16, 128: 8}
        selected_index = self.list_dur.curselection()
        if selected_index:
            selected_length = int(self.list_dur.get(selected_index[0]))
        try: 
            selected_length = lengthdict[selected_length]
        except UnboundLocalError:
            selected_length = 128
            self.list_dur.select_set(3)
        return selected_length / int(self.divide_variable.get()) * int(self.times_variable.get())

    # def set(self, value):
    #     list_dict = {1024:0, 510:1, 256:2, 128:3, 64:4, 32:5, 16:6, 8:7}
    #     self.list_dur.select_set(list_dict[int(value)])
        