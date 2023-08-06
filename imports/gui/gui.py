#!python3.9.2
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

from tkinter import Tk, Canvas, Menu, Scrollbar, messagebox, PanedWindow, PhotoImage
from tkinter import filedialog, Label, Spinbox, StringVar, Listbox, ttk, Frame
import platform, ctypes

from imports.style import STYLE
from imports.colors import color_light, color_dark, color_gui_light, color_gui_dark, color_highlight
from imports.gui.grid_selector import GridSelector
from imports.gui.elementstree import Tree


class Gui:

	def __init__(self, master):
		
		### GUI ###
		# root
		self.root = master
		self.root.title('PianoScript')
		if platform.system() == 'Windows': self.root.state('zoomed')
		self.scrwidth = self.root.winfo_screenwidth()
		self.scrheight = self.root.winfo_screenheight()
		self.root.geometry("%sx%s+0+0" % (int(self.scrwidth), int(self.scrheight)))

		# style
		self.ttkstyle = ttk.Style()
		self.ttkstyle.theme_create('pianoscript', settings=STYLE)
		ttk.Style(self.root).theme_use("pianoscript")

		# set dpi for windows:
		if platform.system() == 'Windows':
		    try: # >= win 8.1
		        ctypes.windll.shcore.SetProcessDpiAwareness(2)
		    except: # win 8.0 or less
		        ctypes.windll.user32.SetProcessDPIAware()

		# main_frame
		self.main_frame = Frame(self.root)
		self.main_frame.pack(fill='both',expand=True)
		
		# main_paned
		self.main_paned = PanedWindow(self.main_frame, orient='h', sashwidth=7.5, 
			relief='flat', bg=color_gui_light)
		self.main_paned.pack(expand=True,fill='both')
		# add gridpanel
		self.gridpanel = Frame(self.main_paned, bg=color_gui_light)
		self.gridpanel.grid_columnconfigure(0,weight=1)
		self.main_paned.add(self.gridpanel, width=100)
		# grid selector
		self.grid_selector = GridSelector(self.gridpanel)
		self.grid_selector.grid(column=0,row=0)
		# staff selector
		self.staffselect_label = Label(self.gridpanel, text='STAFF:', bg=color_gui_light, fg=color_gui_light, font=("courier", 16, 'bold'), anchor='w')
		self.staffselect_label.grid(column=0, row=7, sticky='ew')
		self.staff_selector = StringVar(value=1)
		self.staffselect_spin = Spinbox(self.gridpanel, from_=1, to=4, bg=color_light, fg=color_dark, font=('courier', 16, 'normal'), textvariable=self.staff_selector)
		self.staffselect_spin.grid(column=0, row=8, sticky='ew')
		self.seperator_2 = Label(self.gridpanel, text='------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', 
		    bg=color_gui_light, fg='#c8c8c8', anchor='c', font=("courier"))
		self.seperator_2.grid(column=0, row=10, sticky='ew')
		# elements tree
		self.elements_label = Label(self.gridpanel, text='TOOL:', bg=color_gui_light, fg=color_gui_light, anchor='w', font=("courier", 16, 'bold'))
		self.elements_label.grid(column=0, row=11, sticky='ew')
		self.elements_treeview = Tree(self.gridpanel)
		self.elements_treeview.grid(column=0, row=12, sticky='ew')
		# editor
		self.root.update()
		self.editorpanel = Frame(self.main_paned, bg=color_gui_light, width=self.scrwidth / 3 * 1.54)
		self.main_paned.add(self.editorpanel)
		self.editor = Canvas(self.editorpanel, bg=color_light, relief='flat', cursor='cross')
		self.editor.place(relwidth=1, relheight=1)
		# print view
		self.printpanel = Frame(self.main_paned, bg=color_light)
		self.main_paned.add(self.printpanel)
		self.pview = Canvas(self.printpanel, bg=color_light, relief='flat')
		self.pview.place(relwidth=1, relheight=1)

if __name__ == '__main__':

	...