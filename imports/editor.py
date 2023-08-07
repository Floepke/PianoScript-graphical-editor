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
# if not __name__ == '__main__':
#     from imports.griddialog import GridDialog
#     from imports.optionsdialog import OptionsDialog
import platform
from imports.colors import *
from imports.draw_staff import DrawStaff
from imports.elements import Elements
from imports.savefilestructure import BluePrint
from imports.tools import baseround, interpolation
from tkinter import filedialog
import json

#from imports.elements
#from imports.tools import measure_length

class MainEditor():
    """docstring for Editor"""
    def __init__(self, root, editor, element_tree):

        self.root = root
        self.editor = editor # the editor canvas widget
        self.element_tree = element_tree
        self.score = self.new() # the savefile we are editing using this editor
        self.elements = Elements()

        self.MM = self.root.winfo_fpixels('1m')

        self.edit_data = { # purpose: keeping track of all data for the editors usage
            'editor':editor,
            'last_pianotick':4096, # the last pianotick of the Score
            'new_id':0, # used to give every element a unique id
            'snap_grid':128, # the current selected grid from the grid selector
            'element':self.element_tree.get, # lookup here which element is selected in the element_tree
            'zoom(1pianotick==mm)':1, # zoom setting in the y axis, 4096 pianoticks will fit on the screen.
            'mouse':{ # all info for the mouse
                'x':0, # x position of the mouse in the editor view
                'y':0, # y position of the mouse in the editor view
                'ex':0, # event x note position of the mouse in the editor view
                'ey':0, # event y pianotick position of the mouse in the editor view
                'hold_id':'', # keep track wether an object on the editor is clicked; so this string == 'notex' where x is a number that is unique.
                'button1':False,
                'button2':False,
                'button3':False
            },
            'keyboard':{ # keep track wheter shift or ctl is pressed
                'shift':False,
                'ctl':False,
            },
            'selection':{ # everything about making a selection; keep track
                'x1':None,
                'y1':None,
                'x2':None,
                'y2':None,
                'selection_buffer':[],
                'copycut_buffer':[]
            },
            'editor_width':self.editor.winfo_width(),
            'editor_height':self.editor.winfo_height(),
        }

        # universal editor binds for mac/windows/linux:
        self.editor.bind('<Button-1>', lambda e: self.update(e, 'btn1click'))
        self.editor.bind('<ButtonRelease-1>', lambda e: self.update(e, 'btn1release'))
        if platform.system() in ['Linux', 'Windows']:
            self.editor.bind('<Button-2>', lambda e: self.update(e, 'btn2click'))
            self.editor.bind('<ButtonRelease-2>', lambda e: self.update(e, 'btn2release'))
            self.editor.bind('<Button-3>', lambda e: self.update(e, 'btn3click'))
            self.editor.bind('<ButtonRelease-3>', lambda e: self.update(e, 'btn3release'))
        if platform.system() == 'Darwin':   
            self.editor.bind('<Button-3>', lambda e: self.update(e, 'btn2click'))
            self.editor.bind('<ButtonRelease-3>', lambda e: self.update(e, 'btn2release'))
            self.editor.bind('<Button-2>', lambda e: self.update(e, 'btn3click'))
            self.editor.bind('<ButtonRelease-2>', lambda e: self.update(e, 'btn3release'))
        
        self.editor.bind('<Motion>', lambda e: self.update(e, 'motion'))
        self.editor.bind('<Shift-KeyPress>', lambda e: self.update(e, 'shiftpress'))
        self.editor.bind('<Shift-KeyRelease>', lambda e: self.update(e, 'shiftrelease'))
        self.editor.bind('<Control-KeyPress>', lambda e: self.update(e, 'ctlpress'))
        self.editor.bind('<Control-KeyRelease>', lambda e: self.update(e, 'ctlrelease'))

        DrawStaff.draw_staff(self.edit_data, self.score)

        self.new()

    def update(self, event, event_type):
        '''
            Keep track of mouse buttons pressed or not
            Update mouse position
            Update event pitch and time (based on mouse position)
            Run the right function based on the element_tree.get
        '''

        # mouse buttons:
        if event_type == 'btn1click': self.edit_data['mouse']['button1'] = True
        if event_type == 'btn1release': self.edit_data['mouse']['button1'] = False
        if event_type == 'btn2click': self.edit_data['mouse']['button2'] = True
        if event_type == 'btn2release': self.edit_data['mouse']['button2'] = False
        if event_type == 'btn3click': self.edit_data['mouse']['button3'] = True
        if event_type == 'btn3release': self.edit_data['mouse']['button3']= False

        # shift and ctl keys
        if event_type == 'shiftpress': self.edit_data['keyboard']['shift'] = True
        if event_type == 'shiftrelease': self.edit_data['keyboard']['shift'] = False
        if event_type == 'ctlpress': self.edit_data['keyboard']['ctl'] = True
        if event_type == 'ctlrelease': self.edit_data['keyboard']['ctl'] = False
        
        # motion
        if event_type == 'motion':
            self.edit_data['mouse']['x'] = self.editor.canvasx(event.x)
            self.edit_data['mouse']['y'] = self.editor.canvasy(event.y)
            self.edit_data['mouse']['ex'] = self.x2pitch(self.edit_data['mouse']['x'])
            self.edit_data['mouse']['ey'] = self.y2time(self.edit_data['mouse']['y'])

        # update element:
        self.edit_data['element'] = self.element_tree.get

        # running the right element function:
        eval(f"self.elements.elm_{self.edit_data['element']}(event_type, self.edit_data, self.score)")

        DrawStaff.draw_staff(self.edit_data, self.score)

    '''
        FILE MANAGEMENT:
            - new; creates new project
            - load; opens new project
            - save; saves current project
            - save as; saves current project but asks for save location
    '''
    def new(self):
        '''
            creates a new project by loading from the template file.
            If the file is not on disk it creates one from the "BluePrint".
        '''
        
        # load template:
        try: # load template from disk
            self.score = json.load(open('template.pianoscript', 'r'))
        except: # if template not exists (if the user deleted the file during the run of the program)
            self.score = BluePrint # fallback to source template
        return self.score

    def load(self):
        
        # choose file to open; ignore if user clicked cancel
        f = filedialog.askopenfile(parent=self.root, 
            mode='r',
            title='Open *.pianoscript file...', 
            filetypes=[("PianoScript files", "*.pianoscript")])
        if f: f = f.name
        else: return self.score

        # if the file was selected, load the file
        with open(f, 'r') as f:
            self.score = json.load(f)

    def x2pitch(self, x):
        '''calculates the pitch which is closest to mouse x position'''

        # calculating dimensions
        self.editor.update()
        editor_width = self.editor.winfo_width()
        staff_width = editor_width * 0.8 # property?
        staff_margin = (editor_width - staff_width) / 2
        factor = staff_width / 490
        x -= staff_margin

        cf = [4, 9, 16, 21, 28, 33, 40, 45, 52, 57, 64, 69, 76, 81, 88]
        be = [3, 8, 15, 20, 27, 32, 39, 44, 51, 56, 63, 68, 75, 80, 87]

        xlist = [505, 500, 490, 485, 480, 475, 470, 460, 455, 450, 445, 440, 
        435, 430, 420, 415, 410, 405, 400, 390, 385, 380, 375, 370, 365, 360, 350, 
        345, 340, 335, 330, 320, 315, 310, 305, 300, 295, 290, 280, 275, 270, 265, 
        260, 250, 245, 240, 235, 230, 225, 220, 210, 205, 200, 195, 190, 180, 175, 
        170, 165, 160, 155, 150, 140, 135, 130, 125, 120, 110, 105, 100, 95, 90, 
        85, 80, 70, 65, 60, 55, 50, 40, 35, 30, 25, 20, 15, 10, 0, -5]

        closest = min(xlist, key=lambda m:abs(m-(x/factor)))

        for idx, xx in enumerate(reversed(xlist)):
            if xx == closest:
                return idx + 1

    def y2time(self, y):
        '''calculates time in pianoticks closest to mouse y position'''

        editor_height = self.editor.winfo_height()
        last_tick = self.edit_data['last_pianotick']
        zoom = self.edit_data['zoom(1pianotick==mm)'] * self.MM
        grid = self.edit_data['snap_grid']
        time = baseround(interpolation(0, last_tick, y) * last_tick, grid)
        print(time)
        return time