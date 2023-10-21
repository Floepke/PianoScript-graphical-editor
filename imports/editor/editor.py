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

# imports   
import platform, json
from imports.colors import * # TODO
from imports.editor.staff import DrawStaff
from imports.editor.mouse_handling import MouseHandling
from imports.editor.draw_viewport import DrawViewport
from imports.savefilestructure import BluePrint
from imports.tools import baseround, interpolation
from imports.editor.tools_editor import ToolsEditor
from tkinter import filedialog
from tkinter.messagebox import askyesnocancel
from tkinter import filedialog


class MainEditor():
    """docstring for Editor"""
    def __init__(self, io):

        self.io = io

        # caller; calls the corresponding function in mousehandling
        self.element_caller = {
            "note":MouseHandling.elm_note,
            "accidental":MouseHandling.elm_accidental,
            "beam":MouseHandling.elm_beam,
            "linebreak":MouseHandling.elm_linebreak,
            "ornament":MouseHandling.elm_ornament,
            "countline":MouseHandling.elm_countline
        }

        # universal editor binds for mac/windows/linux:
        self.io['editor'].bind('<Button-1>', lambda e: self.update(e, 'btn1click'))
        self.io['editor'].bind('<ButtonRelease-1>', lambda e: self.update(e, 'btn1release'))
        if platform.system() in ['Linux', 'Windows']:
            self.io['editor'].bind('<Button-2>', lambda e: self.update(e, 'btn2click'))
            self.io['editor'].bind('<ButtonRelease-2>', lambda e: self.update(e, 'btn2release'))
            self.io['editor'].bind('<Button-3>', lambda e: self.update(e, 'btn3click'))
            self.io['editor'].bind('<ButtonRelease-3>', lambda e: self.update(e, 'btn3release'))
        else:   
            self.io['editor'].bind('<Button-3>', lambda e: self.update(e, 'btn2click'))
            self.io['editor'].bind('<ButtonRelease-3>', lambda e: self.update(e, 'btn2release'))
            self.io['editor'].bind('<Button-2>', lambda e: self.update(e, 'btn3click'))
            self.io['editor'].bind('<ButtonRelease-2>', lambda e: self.update(e, 'btn3release'))
        
        self.io['editor'].bind('<Motion>', lambda e: self.update(e, 'motion'))
        self.io['root'].bind('<KeyPress>', self.on_key_press)
        self.io['root'].bind('<KeyRelease>', self.on_key_release)
        self.io['root'].bind('<Control-KeyPress>', lambda e: self.update(e, 'ctlpress'))
        self.io['root'].bind('<Control-KeyRelease>', lambda e: self.update(e, 'ctlrelease'))
        self.io['editor'].bind('<Leave>', lambda e: self.update(e, 'leave'))
        self.io['editor'].bind('<Enter>', lambda e: self.update(e, 'enter'))

        # scroll-bind:
        if platform.system() == 'Linux':
            self.io['editor'].bind('<5>', lambda e: self.scroll_up_callback_linux(e))
            self.io['editor'].bind('<4>', lambda e: self.scroll_down_callback_linux(e))
        if platform.system() in ['Windows', 'Darwin']:
            self.io['editor'].bind('<MouseWheel>', lambda e: self.scroll_callback_windows_darwin(e))

        # create a new initial project from template.pianoscript
        self.new()

        # draw the initial project
        self.redraw_editor(self.io)

        ToolsEditor.update_drawing_order(self.io)

    def scroll_up_callback_linux(self, e):
        self.io['editor'].yview('scroll', 1, 'units')
        self.update(e, 'scroll')

    def scroll_down_callback_linux(self, e):
        self.io['editor'].yview('scroll', -1, 'units')
        self.update(e, 'scroll')

    def scroll_callback_windows_darwin(self, e):
        if e.delta < 0:
            self.io['editor'].yview('scroll', 1, 'units')
        else:
            self.io['editor'].yview('scroll', -1, 'units')
        self.update(e, 'scroll')

    # fix for the detection of shift-keypress that doesn't work on linux
    def on_key_press(self, event):
        if event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
            self.update(event, 'shiftpress')
    def on_key_release(self, event):
        if event.keysym == 'Shift_L' or event.keysym == 'Shift_R':
            self.update(event, 'shiftrelease')

    













    def update(self, e, event_type):
        '''
            Keep track of mouse buttons pressed or not
            Update mouse position
            Update e pitch and time (based on mouse position)
            Run the right function based on the element_tree.get
        '''

        # update idle flag
        self.io['idle'] = False

        # unbind motion (because otherwise we can get recursiondept error if we move the mouse really quick)
        self.io['editor'].unbind('<Motion>')

        # check for leave or enter editor to run the update function or not
        if event_type == 'leave':
            self.io['editor'].delete('cursor', 'notecursor')
            self.io['cursor_on_editor'] = False
            return
        if event_type == 'enter':
            self.io['cursor_on_editor'] = True

        # update widget dimensions: # TODO update only at start of update() function.
        self.io['editor'].update()
        self.io['root'].update()
        self.io['sbar'].update()
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
        
        # update motion (mouse movemenelm_funcevent_type in ['motion', 'scroll']:
        if not event_type == 'space':    
            self.io['mouse']['x'] = self.io['editor'].canvasx(e.x)
            self.io['mouse']['y'] = self.io['editor'].canvasy(e.y)
        self.io['mouse']['ex'] = ToolsEditor.x2pitch(self.io['mouse']['x'], self.io)
        self.io['mouse']['ey'] = ToolsEditor.y2time(self.io['mouse']['y'], self.io)

        # update/read elements tree:
        self.io['element'] = self.io['tree'].get
        self.io['snap_grid'] = self.io['grid_selector'].get()
        
        # call the right elements tree function:
        if not self.io['keyboard']['shift']:
            self.element_caller[self.io['element']](event_type, self.io)

        # update cursor indicator:
        self.io['mouse_handling'].cursor_indicator(event_type, self.io)

        # check if we need to redraw the entire editor:
        if self.io['old_editor_width'] != self.io['editor_width']: # if editor-width has changed:
            self.io['old_editor_width'] = self.io['editor_width']
            ToolsEditor.update_tick_range(self.io)
            self.redraw_editor(self.io)

        # draw all objects that are in the current view/scroll position
        if event_type in ['scroll', 'btn1release', 'motion']:    
            ToolsEditor.update_tick_range(self.io)
            DrawViewport.draw(self.io)

        # delete note cursor if button1 is pressed
        if self.io['mouse']['button1']:
            self.io['editor'].delete('notecursor')

        # evaluate/update the selection if shift key is pressed
        if self.io['keyboard']['shift'] or self.io['selection']['rectangle_on']:
            self.io['selectoperations'].process_selection(event_type)

        # refresh the printview on any mouseclick on the editor
        if event_type in ['btn1release', 'btn2release', 'btn3release']: 
            self.io['engraver'].trigger_render()

        # rebind motion
        self.io['editor'].bind('<Motion>', lambda e: self.update(e, 'motion'))

        # update idle flag
        self.io['idle'] = True

    def redraw_editor(self, io):
        '''
            Runs the task of redrawing the entire editor drawing in case:
                - resized window
                - creating a new project
                - loading a existing project
                - loading a midi file (that replaces the current project)
        '''
        
        io['editor'].delete('note', 'midinote', 
            'stem', 'barline', 'gridline', 'connectstem', 
            'barnumbering', 'leftdot', 'linebreak', 'notestop', 'soundingdot')
        io['drawn_obj'] = []
        ToolsEditor.update_last_pianotick(io)
        DrawStaff.draw_staff(io)
        DrawStaff.draw_barlines_grid(io)
        ToolsEditor.set_scroll_region(io)
        DrawViewport.draw(io)
        ToolsEditor.update_drawing_order(io)



    












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
        print('new...')

        # check if user wants to save or cancel the task.
        if self.io['savefile_system']['filechanged']:
            ask = askyesnocancel('Wish to save?', 'Do you wish to save the current Score?')
            if ask == True:
                self.save()
            elif ask == False:
                ...
            elif ask == None:
                return
        else:
            ...

        # load template:
        try: # load template from disk
            self.io['score'] = json.load(open('template.pianoscript', 'r'))
        except: # if template not exists (if the user deleted the file or it's the first run)
            self.io['score'] = BluePrint # fallback to source template

        # redraw the editor
        self.redraw_editor(self.io)
        
        # trigger render
        try: self.io['engraver'].trigger_render()
        except KeyError: print('ignored trigger_render()')

        # renumbering tags
        ToolsEditor.renumber_tags(self.io)

        # empty drawn_obj
        self.io['drawn_obj'] = []

        # update filepath
        self.io['savefile_system']['filepath'] = 'New'
        self.io['savefile_system']['filechanged'] = False

        # reset ctlz
        try: self.io['ctlz'].reset_ctlz()
        except KeyError: print('ignored reset_ctlz()')

    def load(self):
        print('load...')

        # check if user wants to save or cancel the task.
        if self.io['savefile_system']['filechanged']:
            ask = askyesnocancel('Wish to save?', 'Do you wish to save the current Score?')
            if ask == True:
                self.save()
            elif ask == False:
                ...
            elif ask == None:
                return
        else:
            ...
        
        # choose file to open; ignore if user clicked cancel
        f = filedialog.askopenfile(parent=self.io['root'], 
            mode='r',
            title='Open *.pianoscript file...', 
            filetypes=[("PianoScript files", "*.pianoscript")])
        if f: f = f.name
        else: return

        # if the file was selected, load the file
        with open(f, 'r') as file:
            self.io['score'] = json.load(file)

        # renumbering tags
        ToolsEditor.renumber_tags(self.io)

        # empty drawn_obj
        self.io['drawn_obj'] = []

        # redraw the editor
        self.redraw_editor(self.io)

        # trigger render
        try: self.io['engraver'].trigger_render()
        except KeyError: print('ignored trigger_render()')

        # update filepath
        self.io['savefile_system']['filepath'] = f
        self.io['savefile_system']['filechanged'] = False

        # update window title
        self.io['root'].title(f"PianoScript - {self.io['savefile_system']['filepath']}")

        # reset ctlz
        try: self.io['ctlz'].reset_ctlz()
        except KeyError: print('ignored reset_ctlz()')

    def save(self):
        print('save...')

        if self.io['savefile_system']['filepath'] != 'New':
            with open(self.io['savefile_system']['filepath'], 'w') as f:
                f.write(json.dumps(self.io['score'], separators=(',', ':'), indent=2))
            self.io['savefile_system']['filechanged'] = False
        else:
            self.saveas()

    def saveas(self):
        print('saveas...')

        # ask user input and saveas if so
        f = filedialog.asksaveasfile(parent=self.io['root'], 
            mode='w', 
            filetypes=[("PianoScript files", "*.pianoscript")],
            title='Save as...',
            initialdir='~/Desktop/')
        f = f.name
        if not f.endswith('.pianoscript'): f = f + '.pianoscript'
        if f:
            self.io['root'].title('PianoScript - %s' % f)
            with open(f, 'w') as file:
                file.write(json.dumps(self.io['score'], separators=(',', ':'), indent=2))# indent=2
            
            # update filepath
            self.io['savefile_system']['filepath'] = f
            self.io['savefile_system']['filechanged'] = False
