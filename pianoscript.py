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

# third party imports
from tkinter import Tk, Canvas, Menu, Scrollbar, messagebox, PanedWindow, PhotoImage
from tkinter import Label, Spinbox, StringVar, Listbox, ttk, Frame
import platform, ctypes

# own imports code :)
from imports.editor import MainEditor
from imports.savefilestructure import BluePrint
from imports.gui.gui import Gui
from imports.colors import color_light, color_gui_light

class App:

	def __init__(self):
		
		# root
		self.root = Tk()

		# gui
		self.gui = Gui(master=self.root)

		# editor
		self.main_editor = MainEditor(self.root,
			self.gui.editor, 
			self.gui.elements_treeview)

		# menu
		self.menubar = Menu(self.root, relief='flat', bg=color_gui_light, fg=color_light, font=('courier', 16))
		self.root.config(menu=self.menubar)
		self.fileMenu = Menu(self.menubar, tearoff=0)
		self.fileMenu.add_command(label='New [ctl+n]', command=self.main_editor.new, font=('courier', 16))
		self.fileMenu.add_command(label='Open [ctl+o]', command=self.main_editor.load, font=('courier', 16))
		self.fileMenu.add_command(label='Save [ctl+s]', command=None, font=('courier', 16))
		self.fileMenu.add_command(label='Save as... [alt+s]', command=None, font=('courier', 16))
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label='Load midi [ctl+m]', command=None, font=('courier', 16))
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Export ps", command=None, font=('courier', 16))
		self.fileMenu.add_command(label="Export pdf [ctl+e]", command=None, font=('courier', 16))
		self.fileMenu.add_command(label="Export midi*", command=None, font=('courier', 16))
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Grid editor... [g]", underline=None, command=None, font=('courier', 16))
		self.fileMenu.add_command(label="Score options... [s]", underline=None, command=None, font=('courier', 16))
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Exit", underline=None, command=None, font=('courier', 16))
		self.menubar.add_cascade(label="File", underline=None, menu=self.fileMenu, font=('courier', 16))

		# binds
		self.root.bind('<Escape>', self.quit)


	def run(self):
		'''In run() we setup the main run structure of the app'''

		# main_render = MainRender(self.editor,
		# 	self.elements_treeview, 
		# 	self.score, 
		# 	self.root)

		self.root.mainloop()

	def quit(self, event=''):
		
		# file-save-check
		...

		# quit
		self.root.destroy()
		



if __name__ == '__main__':
	app = App()
	app.run()