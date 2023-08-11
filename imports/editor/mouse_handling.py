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

from imports.editor.editor_draw_elements import DrawElements
from imports.editor.tools_editor import ToolsEditor
from imports.colors import color_dark

class MouseHandling():
    '''
        The elements class stores all element modes.
        In this file/class the mouse and keyboard handlings
        are programmed. every function get's the event_type
        ('btn123click', 'btn123release', 'motion', ...),
        self.editor/canvas, self.score and returns the 
        (maybe) edited score.
    '''
    def __init__(self):
        ...

    def cursor_indicator(self, event_type, io):
        '''Draws the cursor indicator on the left and right of the staff'''

        if not event_type == 'leave':
            io['cursor_on_editor'] = True
        else:
            io['editor'].delete('cursor')
            io['cursor_on_editor'] = False
            return

        if event_type == 'motion' and io['cursor_on_editor']:
            
            cursor = {
                'time':io['mouse']['ey'],
                'pitch':io['mouse']['ex'],
                'hand':'r',
                'zoom':io['ticksizepx']
            }
            io['editor'].update()
            io['editor'].delete('cursor')

            time = ToolsEditor.time2y(cursor['time'], io)
            sbar_width = io['sbar'].winfo_width()
            editor_width = io['editor_width'] - sbar_width
            staff_width = editor_width * io['xscale']
            staff_margin = (editor_width - staff_width) / 2
            
            io['editor'].create_line(sbar_width, time,
                sbar_width+staff_margin, time,
                tag='cursor', 
                width=4, 
                fill=color_dark,
                arrow='last',
                arrowshape=(40, 40, 20))
            io['editor'].create_line(sbar_width+editor_width-staff_margin, time,
                sbar_width+editor_width, time,
                tag='cursor', 
                width=4, 
                fill=color_dark,
                arrow='first',
                arrowshape=(40, 40, 20))




    # right hand
    def elm_note_right(self, event_type, io):

        if event_type == 'leave':
            io['editor'].delete('cursor')
            io['draw_cursor'] = False
            return
        if event_type == 'enter':
            io['draw_cursor'] = True
            return

        if event_type == 'motion' and io['cursor_on_editor']:

            # draw the note cursor:
            cursor_note = {
                "time":io['mouse']['ey'],
                "duration":640.0,
                "pitch":io['mouse']['ex'],
                "hand":"l",
                "id":"cursor",
                "stem-visible":True,
                "accidental":0
            }
            DrawElements.draw_note_lr(cursor_note, io)
        
        if event_type == 'btn1click':
            
            ...

        if event_type == 'btn1release':
            
            ...

        if event_type == 'btn3click':
            
            ...




    # left hand
    def elm_note_left(self, event_type, io):
        
        if event_type == 'btn1click':
            
            ...

        if event_type == 'motion':
            
            ...

        if event_type == 'btn1release':
            
            ...

        if event_type == 'btn3click':
            
            ...

    # accidental
    def elm_accidental(self, event_type, io):
        
        if event_type == 'btn1click':
            
            ...

        if event_type == 'motion':
            
            ...

        if event_type == 'btn1release':
            
            ...

        if event_type == 'btn3click':
            
            ...




    # beam
    def elm_beam(self, event_type, io):
        
        if event_type == 'btn1click':
            
            ...

        if event_type == 'motion':
            
            ...

        if event_type == 'btn1release':
            
            ...

        if event_type == 'btn3click':
            
            ...



