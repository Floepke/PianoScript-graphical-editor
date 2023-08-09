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

class Elements():
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

        if event_type == 'leave':
            io['editor'].delete('cursor')
            io['draw_cursor'] = False
            return
        if event_type == 'enter':
            io['draw_cursor'] = True
            return

        if event_type == 'motion' and io['draw_cursor']:
            
            cursor = {
                'time':io['mouse']['ey'],
                'pitch':io['mouse']['ex'],
                'hand':'r',
                'zoom':io['ticksizepx']
            }
            DrawElements.draw_cursor_indicator(cursor, io)

    # right hand
    def elm_note_right(self, event_type, io):

        if event_type == 'leave':
            io['editor'].delete('cursor')
            io['draw_cursor'] = False
            return
        if event_type == 'enter':
            io['draw_cursor'] = True
            return

        if event_type == 'motion' and io['draw_cursor']:

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