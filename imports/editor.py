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
#from imports.tools import measure_length

class MainEditor():
    """docstring for Editor"""
    def __init__(self, root, editor, element_tree, score):

        self.root = root
        self.editor = editor # the editor canvas widget
        self.element_tree = element_tree
        self.score = score # the savefile we are editing using the editor

        self.edit_data = { # purpose: keeping track of all data for the editors usage
            'last_pianotick':100, # the last pianotick of the Score
            'new_id':0, # used to give every element a unique id
            'snap_grid':128, # the current selected grid from the grid selector
            'element':self.element_tree.get, # lookup here which element is selected in the element_tree
            'zoom(pianotick)':4096, # zoom setting in the y axis
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

        DrawStaff.draw_staff(self.editor, self.edit_data, self.score)

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
            self.edit_data['mouse']['ex'] = self.x2pitch(event.x)
            self.edit_data['mouse']['ey'] = self.y2time(event.y)

        # update element:
        self.edit_data['element'] = self.element_tree.get

        # running the element function:
        try: eval(f'self.elm_{self.edit_data["element"]}(event_type)')
        except AttributeError:
            raise print('ERROR; this element is not yet implemented. ignoring click or mouse movement')

        self.draw_cursor()
        DrawStaff.draw_staff(self.editor, self.edit_data, self.score)

        # draw all elements. We check if we have to draw, delete or both.
        
        # # note
        # for note in self.score['events']['note']:
        #     print(note)
        #     # if event_type in ['btn1click', 'btn1release']:
        #     #     note['id'] = 'note%i'%self.edit_data['new_id']
        #     #     self.edit_data['new_id'] += 1



    '''
    ELEMENTS TREE PART:
    In the following part all methods are listed that are used
    to edit the current selected element in the elements tree.
    For example: if elements tree 'accidental' is selected
    update() calls elm_accidental() so the names below always
    start with 'elm_' followed by the element label in the 
    function name.
    '''
    def elm_note_left(self, event_type):
        '''code that handles the note input left element'''
        ...

        # self.editor.delete('note')
        # self.editor.create_oval(self.edit_data['mouse']['ex'], self.edit_data['mouse']['ey'],
        #   self.edit_data['mouse']['ex']+10, self.edit_data['mouse']['ey']+10,
        #   fill='red',
        #   tag='note')

    def elm_note_right(self, event_type):
        '''code that handles the note input right element'''
        ...

    def elm_accidental(self, event_type):
        '''code that handles the accidental element'''
        ...

    def elm_beam(self, event_type):
        '''code that handles the beam element'''
        ...

    def draw_cursor(self):
        '''
            (re)-draws the cursor indicator that's always updated 
            no matter what tool is selected in the elements tree
        '''
        ...


    def x2pitch(self, x):
        '''calculates the pitch which is closest to mouse x position'''
        ...
        return 0

    def y2time(self, y):
        '''calculates time in pianoticks closest to mouse y position'''
        ...
        return 0