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
from imports.editor.draw_staff import DrawStaff
from imports.editor.elements import Elements
from imports.savefilestructure import BluePrint
from imports.tools import baseround, interpolation
from tkinter import filedialog
import json

#from imports.elements
#from imports.tools import measure_length

class MainEditor():
    """docstring for Editor"""
    def __init__(self, io):

        self.io = io

        # universal editor binds for mac/windows/linux:
        self.io['editor'].bind('<Button-1>', lambda e: self.update(e, 'btn1click'))
        self.io['editor'].bind('<ButtonRelease-1>', lambda e: self.update(e, 'btn1release'))
        if platform.system() in ['Linux', 'Windows']:
            self.io['editor'].bind('<Button-2>', lambda e: self.update(e, 'btn2click'))
            self.io['editor'].bind('<ButtonRelease-2>', lambda e: self.update(e, 'btn2release'))
            self.io['editor'].bind('<Button-3>', lambda e: self.update(e, 'btn3click'))
            self.io['editor'].bind('<ButtonRelease-3>', lambda e: self.update(e, 'btn3release'))
        if platform.system() == 'Darwin':   
            self.io['editor'].bind('<Button-3>', lambda e: self.update(e, 'btn2click'))
            self.io['editor'].bind('<ButtonRelease-3>', lambda e: self.update(e, 'btn2release'))
            self.io['editor'].bind('<Button-2>', lambda e: self.update(e, 'btn3click'))
            self.io['editor'].bind('<ButtonRelease-2>', lambda e: self.update(e, 'btn3release'))
        
        self.io['editor'].bind('<Motion>', lambda e: self.update(e, 'motion'))
        self.io['editor'].bind('<Shift-KeyPress>', lambda e: self.update(e, 'shiftpress'))
        self.io['editor'].bind('<Shift-KeyRelease>', lambda e: self.update(e, 'shiftrelease'))
        self.io['editor'].bind('<Control-KeyPress>', lambda e: self.update(e, 'ctlpress'))
        self.io['editor'].bind('<Control-KeyRelease>', lambda e: self.update(e, 'ctlrelease'))

        self.new() # create a new initial project from template.pianoscript

    def update(self, event, event_type):
        '''
            Keep track of mouse buttons pressed or not
            Update mouse position
            Update event pitch and time (based on mouse position)
            Run the right function based on the element_tree.get
        '''

        # mouse buttons:
        if event_type == 'btn1click': self.io['mouse']['button1'] = True
        if event_type == 'btn1release': self.io['mouse']['button1'] = False
        if event_type == 'btn2click': self.io['mouse']['button2'] = True
        if event_type == 'btn2release': self.io['mouse']['button2'] = False
        if event_type == 'btn3click': self.io['mouse']['button3'] = True
        if event_type == 'btn3release': self.io['mouse']['button3']= False

        # shift and ctl keys
        if event_type == 'shiftpress': self.io['keyboard']['shift'] = True
        if event_type == 'shiftrelease': self.io['keyboard']['shift'] = False
        if event_type == 'ctlpress': self.io['keyboard']['ctl'] = True
        if event_type == 'ctlrelease': self.io['keyboard']['ctl'] = False
        
        # motion
        if event_type == 'motion':
            self.io['mouse']['x'] = self.io['editor'].canvasx(event.x)
            self.io['mouse']['y'] = self.io['editor'].canvasy(event.y)
            self.io['mouse']['ex'] = self.x2pitch(self.io['mouse']['x'])
            self.io['mouse']['ey'] = self.y2time(self.io['mouse']['y'])

        # update element:
        self.io['element'] = self.io['tree'].get
        #self.io['snap_grid'] = self.io['grid_selector'].get()

        # running the right element function:
        #eval(f"self.io['elm_func'].elm_{self.io['element']}(event_type, self.io)")

        DrawStaff.draw_staff(self.io)

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
            self.io['score'] = json.load(open('template.pianoscript', 'r'))
        except: # if template not exists (if the user deleted the file during the run of the program)
            self.io['score'] = BluePrint # fallback to source template

        # update several important values
        #self.io['last_pianotick'] = 1024

        return self.io['score']

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
        self.io['editor'].update()
        editor_width = self.io['editor'].winfo_width()
        staff_width = editor_width * self.io['xscale_staff'] # property?
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

        # closest = min(xlist, key=lambda m:abs(m-(x/factor)))

        # for idx, xx in enumerate(reversed(xlist)):
        #     if xx == closest:
        #         return idx + 1
        return 40

    def y2time(self, y):
        '''calculates time in pianoticks closest to mouse y position'''

        grid = self.io['snap_grid']
        zoom = self.io['yscale']
        last_tick = self.io['last_pianotick']

        self.io['editor'].update()
        editor_width = self.io['editor_width']
        staff_width = editor_width * self.io['xscale_staff']
        staff_margin = (editor_width - staff_width) / 2

        start = staff_margin
        end = staff_margin + (last_tick * zoom)

        time = baseround(interpolation(start, end, y), grid)
        if time < 0: time = 0
        print(time)
        return time
