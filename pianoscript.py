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
from imports.editor.editor import MainEditor
from imports.savefilestructure import BluePrint
from imports.gui.gui import Gui
from imports.colors import color_light, color_gui_light
from imports.editor.elements import Elements

class App:

	def __init__(self):
		
		# root
		self.root = Tk()

		# gui
		self.gui = Gui(master=self.root)
		self.gui.editor.update()

		# the self.data stores all data from the app in one organized dict:
		self.io = {
			# root window
			'root':self.root,
			# editor canvas
			'editor':self.gui.editor,
			# printview canvas
			'pview':self.gui.pview,
			# the curstomized elements tree widget
			'tree':self.gui.treeview,
			# gridselector
			'grid_selector':self.gui.grid_selector,
			# the score object where all score data is
			'score':{},
			# this class stores all methods for elements
			'elm_func':Elements(),
			# the last pianotick of the score
			'last_pianotick':8192,
			# used to give every element a unique id
			'new_id':0,
			# the current selected grid from the grid selector
			'snap_grid':128,
			# zoom setting in the y axis; we define the size of one pianotick in px on the screen
			'ticksizepx':.5,
			# 1 == the staff is the width of the editor canvas.
			'xscale':0.8,
			# all info for the mouse
			'mouse':{
				'x':0, # x position of the mouse in the editor view
				'y':0, # y position of the mouse in the editor view
				'ex':0, # event x note position of the mouse in the editor view
				'ey':0, # event y pianotick position of the mouse in the editor view
				'button1':False, # True if the button is clicked and hold, False if not pressed
				'button2':False, # ...
				'button3':False # ...
			},
			# keep track wether an object on the editor is clicked; this variable is the 
			# unique id from a clicked object on the editor canvas if an object is clicked+hold
			'hold_id':'', 
			'keyboard':{ # keep track wheter shift or ctl is pressed
				'shift':False,
				'ctl':False,
			},
			'selection':{ # everything about making a selection; keep track
				'x1':None,
				'y1':None,
				'x2':None,
				'y2':None,
				'selection_buffer':[], # the buffer
				'copycut_buffer':[]
			},
			# a mm in pixels on the screen
			'mm': self.root.winfo_fpixels('1m'),
			'editor_width': self.gui.editor.winfo_width(),
			'editor_height': self.gui.editor.winfo_height(),
			'redraw_editor':True
		}

		# editor
		self.main_editor = MainEditor(self.io)

		# engraver
		...

		# menu (written in this area because commands are not accessable inside the GUI class, can't set it later)
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
		'''In run() we go into the mainloop of the app'''
		self.root.mainloop()

	def quit(self, event=''):
		
		# file-save-check
		...

		# quit (generates an error if mouse binds are still active TODO)
		self.root.destroy()
		



if __name__ == '__main__':
	app = App()
	app.run()
