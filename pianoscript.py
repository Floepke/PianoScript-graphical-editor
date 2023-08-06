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
from tkinter import filedialog, Label, Spinbox, StringVar, Listbox, ttk, Frame
import platform, ctypes

# own imports code :)
from imports.editor import MainEditor
from imports.savefilestructure import BluePrint
from imports.gui.gui import Gui

class App:

	def __init__(self):
		
		# root
		self.root = Tk()

		# gui
		self.gui = Gui(master=self.root)

		# editable objects
		self.score = BluePrint

		# binds
		self.root.bind('<Escape>', self.quit)


	def run(self):
		'''In run() we setup the main run structure of the app'''

		main_editor = MainEditor(self.root,
			self.gui.editor, 
			self.gui.elements_treeview, 
			self.score)

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