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
from imports.editor.staff import DrawStaff
from imports.editor.elements import Elements
from imports.savefilestructure import BluePrint
from imports.tools import baseround, interpolation
from imports.editor.tools_editor import ToolsEditor
from tkinter import filedialog
import json
from imports.editor.update_elements_in_view import UpdateElementsInView

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
        # to force the editor to update on mouse release when resizing the window for example.
        self.io['root'].bind('<ButtonRelease-1>', lambda e: self.update(e, 'motion')) 
        self.io['editor'].bind('<Shift-KeyPress>', lambda e: self.update(e, 'shiftpress'))
        self.io['editor'].bind('<Shift-KeyRelease>', lambda e: self.update(e, 'shiftrelease'))
        self.io['editor'].bind('<Control-KeyPress>', lambda e: self.update(e, 'ctlpress'))
        self.io['editor'].bind('<Control-KeyRelease>', lambda e: self.update(e, 'ctlrelease'))
        self.io['editor'].bind('<Leave>', lambda e: self.update(e, 'leave'))
        self.io['editor'].bind('<Enter>', lambda e: self.update(e, 'enter'))

        # scroll-bind:
        if platform.system() == 'Linux':
            self.io['editor'].bind('<5>', lambda event: self.scroll_up_callback_linux(event))
            self.io['editor'].bind('<4>', lambda event: self.scroll_down_callback_linux(event))
        if platform.system() in ['Windows', 'Darwin']:
            self.io['editor'].bind('<MouseWheel>', lambda event: self.scroll_callback_windows(event))

        # create a new initial project from template.pianoscript
        self.new()

        # draw the initial barlines and grid
        ToolsEditor.update_last_pianotick(self.io)
        DrawStaff.draw_barlines_grid(self.io)
        DrawStaff.draw_staff(self.io)
        self.io['editor'].update()
        self.io['sbar'].update()
        ToolsEditor.update_tick_range(self.io)
        UpdateElementsInView.draw_note(self.io)

        # call the automatic note drawer on scroll position to life:
        #self.update_elements_in_view = UpdateElementsInView.(self.io)

    def scroll_up_callback_linux(self, event):
        print(event.delta)
        self.io['editor'].yview('scroll', 1, 'units')
        self.update(event, 'scroll')

    def scroll_down_callback_linux(self, event):
        print(event.delta)
        self.io['editor'].yview('scroll', -1, 'units')
        self.update(event, 'scroll')

    def scroll_callback_windows(self, event):
        if event.delta < 0:
            self.io['editor'].yview('scroll', 1, 'units')
        else:
            self.io['editor'].yview('scroll', -1, 'units')
        self.update(event, 'scroll')

    def update(self, event, event_type):
        '''
            Keep track of mouse buttons pressed or not
            Update mouse position
            Update event pitch and time (based on mouse position)
            Run the right function based on the element_tree.get
        '''
        # unbind motion (because otherwise we can get recursiondept error if we move the mouse really quick)
        self.io['editor'].unbind('<Motion>')

        # update widget dimensions:
        self.io['editor'].update()
        self.io['editor_width'] = self.io['editor'].winfo_width()
        self.io['editor_height'] = self.io['editor'].winfo_height()

        # update mouse buttons:
        if event_type == 'btn1click': self.io['mouse']['button1'] = True
        if event_type == 'btn1release': self.io['mouse']['button1'] = False
        if event_type == 'btn2click': self.io['mouse']['button2'] = True
        if event_type == 'btn2release': self.io['mouse']['button2'] = False
        if event_type == 'btn3click': self.io['mouse']['button3'] = True
        if event_type == 'btn3release': self.io['mouse']['button3']= False

        # update shift and ctl keys
        if event_type == 'shiftpress': self.io['keyboard']['shift'] = True
        if event_type == 'shiftrelease': self.io['keyboard']['shift'] = False
        if event_type == 'ctlpress': self.io['keyboard']['ctl'] = True
        if event_type == 'ctlrelease': self.io['keyboard']['ctl'] = False
        
        # update motion (mouse movement)
        if event_type in ['motion', 'scroll']:
            self.io['mouse']['x'] = self.io['editor'].canvasx(event.x)
            self.io['mouse']['y'] = self.io['editor'].canvasy(event.y)
            self.io['mouse']['ex'] = ToolsEditor.x2pitch(self.io['mouse']['x'], self.io)
            self.io['mouse']['ey'] = ToolsEditor.y2time(self.io['mouse']['y'], self.io)

        # update scroll position
        self.io['scroll_position'] = self.update_scroll()

        # update element:
        self.io['element'] = self.io['tree'].get
        self.io['snap_grid'] = self.io['grid_selector'].get()
        #self.io['grid_selector'].set(self.io['snap_grid'])

        # update cursor indicator:
        self.io['elm_func'].cursor_indicator(event_type, self.io)

        # updating the right element function:
        eval(f"self.io['elm_func'].elm_{self.io['element']}(event_type, self.io)")

        # check if we need to redraw everything:
        if self.io['old_editor_width'] != self.io['editor_width']: # if editor-width has changed:
            self.io['old_editor_width'] = self.io['editor_width']
            self.redraw_editor(self.io)

        # draw all objects that are in the current view/scroll position
        if event_type in ['scroll', 'btn1release', 'motion']:    
            ToolsEditor.update_tick_range(self.io)
            UpdateElementsInView.draw_note(self.io)


        # rebind motion
        self.io['editor'].bind('<Motion>', lambda e: self.update(e, 'motion'))

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
        f = filedialog.askopenfile(parent=self.io['root'], 
            mode='r',
            title='Open *.pianoscript file...', 
            filetypes=[("PianoScript files", "*.pianoscript")])
        if f: f = f.name
        else: return

        # if the file was selected, load the file
        with open(f, 'r') as f:
            self.io['score'] = json.load(f)

        # redraw the editor
        self.io['editor'].delete('note', 'midinote')
        ToolsEditor.update_last_pianotick(self.io)
        self.io['editor'].update()
        self.io['sbar'].update()
        DrawStaff.draw_barlines_grid(self.io)
        DrawStaff.draw_staff(self.io)
        ToolsEditor.update_tick_range(self.io)
        ToolsEditor.set_scroll_region(self.io)
        self.io['drawn_obj'] = []
        UpdateElementsInView.draw_note(self.io)


    def update_scroll(self):
        '''
            Updates the current scroll position.
            scroll position is a float 0..1
        '''
        ...
        return 0

    def redraw_editor(self, io):
        '''Runs the task of redrawing the entire editor drawing'''
        
        io['editor'].delete('note', 'midinote', 'stem')
        io['drawn_obj'] = []
        ToolsEditor.update_last_pianotick(io)
        DrawStaff.draw_staff(io)
        DrawStaff.draw_barlines_grid(io)
        ToolsEditor.set_scroll_region(io)

if __name__ == '__main__':
    from .....pianoscript import App
    app = App()
    app.run()