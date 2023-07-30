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

'''
This file contains all code for the editor:
	- All different modes and theur behavior
	- ...
'''

# imports
if not __name__ == '__main__':
	from imports.griddialog import GridDialog
	from imports.optionsdialog import OptionsDialog
import platform

class MainEditor():
	"""docstring for Editor"""
	def __init__(self, Editor, element_tree, Score):

		self.Editor = Editor # the editor canvas widget
		self.Score = Score # the savefile we are editing using the editor
		self.element_tree = element_tree

		self.io = { # purpose: keeping track of all data for the editors usage
			'last_pianotick':0, # the last pianotick of the Score
			'new_id':0, # used to give every element a unique id
			'edit_grid':128, # the current selected grid from the grid selector
			'element':'note_right', # lookup here which element is selected in the element_tree
			'ystaffzoom':1, # zoom setting in the y axis
			'mouse':{ # all info for the mouse
				'x':0, # x position of the mouse in the editor view
				'y':0, # y position of the mouse in the editor view
				'ex':0, # event x note position of the mouse in the editor view
				'ey':0, # event y pianotick position of the mouse in the editor view
				'hold_id':'', # keep track wether an object on the editor is clicked
				'button':{ # keep track wether button 1, 2 or 3 is pressed.
					'1':False,
					'2':False,
					'3':False
				}
			},
			'keyboard':{
				'shift':False,
				'ctl':False,
			},
			'selection':{
				'x1':None,
				'y1':None,
				'x2':None,
				'y2':None,
				'selection_buffer':[],
				'copycut_buffer':[]
			}
		}

		# binds
		self.Editor.bind('<Button-1>', lambda e: self.update(e, 'btn1click'))
		self.Editor.bind('<ButtonRelease-1>', lambda e: self.update(e, 'btn1release'))
		if platform.system() in ['Linux', 'Windows']:	
			self.Editor.bind('<Button-2>', lambda e: self.update(e, 'btn2click'))
			self.Editor.bind('<ButtonRelease-2>', lambda e: self.update(e, 'btn2release'))
			self.Editor.bind('<Button-3>', lambda e: self.update(e, 'btn3click'))
			self.Editor.bind('<ButtonRelease-3>', lambda e: self.update(e, 'btn3release'))
		if platform.system() == 'Darwin':	
			self.Editor.bind('<Button-3>', lambda e: self.update(e, 'btn2click'))
			self.Editor.bind('<ButtonRelease-3>', lambda e: self.update(e, 'btn2release'))
			self.Editor.bind('<Button-2>', lambda e: self.update(e, 'btn3click'))
			self.Editor.bind('<ButtonRelease-2>', lambda e: self.update(e, 'btn3release'))
		self.Editor.bind('<Motion>', lambda e: self.update(e, 'motion'))

		self.Editor.bind('<Shift-KeyPress>', lambda e: self.update(e, 'shiftpress'))
		self.Editor.bind('<Shift-KeyRelease>', lambda e: self.update(e, 'shiftrelease'))
		self.Editor.bind('<Control-KeyPress>', lambda e: self.update(e, 'ctlpress'))
		self.Editor.bind('<Control-KeyRelease>', lambda e: self.update(e, 'ctlrelease'))
		

	def update(self, event, event_type):
		'''
			Keep track of mouse buttons pressed or not
			Update mouse position
			Update event pitch and time
		'''

		# mouse buttons:
		if event_type == 'btn1click': self.io['mouse']['button']['1'] = True
		if event_type == 'btn1release': self.io['mouse']['button']['1'] = False
		if event_type == 'btn2click': self.io['mouse']['button']['2'] = True
		if event_type == 'btn2release': self.io['mouse']['button']['2'] = False
		if event_type == 'btn3click': self.io['mouse']['button']['3'] = True
		if event_type == 'btn3release': self.io['mouse']['button']['3'] = False

		# shift and ctl keys
		if event_type == 'shiftpress': self.io['keyboard']['shift'] = True
		if event_type == 'shiftrelease': self.io['keyboard']['shift'] = False
		if event_type == 'ctlpress': self.io['keyboard']['ctl'] = True
		if event_type == 'ctlrelease': self.io['keyboard']['ctl'] = False
		
		# motion
		if event_type == 'motion':

			self.io['mouse']['x'] = self.Editor.canvasx(event.x)
			self.io['mouse']['y'] = self.Editor.canvasx(event.y)
			self.io['mouse']['ex'] = self.Editor.canvasx(event.x)# replace for x2pitch() function
			self.io['mouse']['ey'] = self.Editor.canvasx(event.y)# replace for y2time() function

		# update element:
		self.io['element'] = self.element_tree.get

		# making decisions based on the currently selected element in de elements tree:
		if self.io['element'] == 'note_left': self.elm_noteleft(event_type)
		if self.io['element'] == 'note_right': self.elm_noteright(event_type)

	# ALL Elements:
	def elm_noteleft(self, event_type):
		'''code that handles the note input left element'''
		print('elm_noteleft')

	def elm_noteright(self, event_type):
		'''code that handles the note input right element'''
		print('elm_noteright')

	...
