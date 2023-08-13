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
        In this file/class the mouse handlings
        are programmed. every function get's the event_type
        ('btn123click', 'btn123release', 'motion', ...),
        io and changes the edited element if so...
    '''

    @staticmethod
    def cursor_indicator(event_type, io):
        '''Draws the cursor indicator on the left and right of the staff'''

        if event_type in ['motion', 'scroll'] and io['cursor_on_editor']:
            
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




    # note:
    @staticmethod
    def elm_note(event_type, io):

        obj_type = 'note'

        # right-left choice
        if io['hand'] == 'r':
            hand = 'r'
        else:
            hand = 'l'

        if event_type == 'btn1click':

            # detect if we are editing a note or
            # in case we click not on a note, we
            # create a new_note.
            tags = io['editor'].gettags("current")
            if tags:
                if obj_type in tags[0]:
                    for note in io['score']['events']['note']:
                        if note['tag'] == tags[0]:
                            # starting to edit a note...
                            io['edit_obj'] = note
                            return
            
            # create a new note
            new_note = {
                "tag":obj_type + str(ToolsEditor.add_tag(io)),
                "time":io['mouse']['ey'],
                "duration":io['snap_grid'],
                "pitch":io['mouse']['ex'],
                "hand":hand,
                "stem_visible":True,
                "accidental":0,
                "staff":0,
                "notestop":True
            }
            DrawElements.draw_note(new_note, io, new=True)
            io['edit_obj'] = new_note
            io['old_obj'] = new_note

        if event_type == 'motion' and io['cursor_on_editor']:

            if not io['mouse']['button1']:
                # draw the note cursor:
                cursor_note = {
                    "time":io['mouse']['ey'],
                    "duration":640.0,
                    "pitch":io['mouse']['ex'],
                    "hand":hand,
                    "id":"cursor",
                    "stem-visible":True,
                    "accidental":0
                }
                DrawElements.draw_note_cursor(cursor_note, io)
            elif io['edit_obj']:
                io['edit_obj']['duration'] = io['mouse']['ey'] - io['edit_obj']['time']
                DrawElements.draw_note(io['edit_obj'], io, new=False)
                    

        if event_type == 'btn1release':
            
            io['edit_obj'] = None
            io['old_obj'] = None

        if event_type == 'btn3click':
            
            # detect if we are clicking on a note and delete if so
            tags = io['editor'].gettags("current")
            if tags:
                if obj_type in tags[0]:
                    for note in io['score']['events']['note']:
                        if note['tag'] == tags[0]:
                            # delete note
                            io['editor'].delete(note['tag'])
                            io['score']['events']['note'].remove(note)

    # accidental:
    @staticmethod
    def elm_accidental(event_type, io):
        
        if event_type == 'btn1click':
            
            ...

        if event_type == 'motion':
            
            ...

        if event_type == 'btn1release':
            
            ...

        if event_type == 'btn3click':
            
            ...




    # beam:
    @staticmethod
    def elm_beam(event_type, io):
        
        if event_type == 'btn1click':
            
            ...

        if event_type == 'motion':
            
            ...

        if event_type == 'btn1release':
            
            ...

        if event_type == 'btn3click':
            
            ...



