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

    # CURSOR:
    @staticmethod
    def cursor_indicator(event_type, io):
        '''Draws the cursor indicator on the left and right of the staff'''

        if event_type in ['motion', 'scroll'] and io['cursor_on_editor']:
            
            cursor = {
                'time':io['mouse']['ey'],
                'pitch':io['mouse']['ex'],
                'hand':'r',
                'tag':'cursor'
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




    # NOTE:
    @staticmethod
    def elm_note(event_type, io):

        obj_type = '#note'

        if event_type == 'btn1click':

            # set filechanged flag
            io['savefile_system']['filechanged'] = True

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
                            # assign the currently selected hand:
                            io['edit_obj']['hand'] = io['hand']
                            return
            
            # create a new note
            new_note = {
                "tag":obj_type + str(ToolsEditor.add_tag(io)),
                "time":io['mouse']['ey'],
                "duration":io['snap_grid'],
                "pitch":io['mouse']['ex'],
                "hand":io['hand'],
                "accidental":0,
                "staff":0
            }
            DrawElements.draw_note(new_note, io, new=True)
            io['edit_obj'] = new_note
            io['old_obj'] = new_note

        if event_type in ['motion', 'space'] and io['cursor_on_editor']:

            # this gets executed if no mousebutton is pressed but we only move the mouse on the editor:
            if not io['mouse']['button1']:
                # draw the note cursor:
                cursor_note = {
                    "time":io['mouse']['ey'],
                    "pitch":io['mouse']['ex'],
                    "hand":io['hand'],
                    "stemless":False,
                }
                DrawElements.draw_note_cursor(cursor_note, io)
            
            # this gets executed if the mousebtn1 is pressed:
            elif io['edit_obj']:
                # edit the notes length or pitch in the specific pianoscript way:
                if io['mouse']['ey'] >= io['edit_obj']['time']:
                    if io['mouse']['ey'] >= io['snap_grid'] + io['edit_obj']['time']:
                        io['edit_obj']['duration'] = io['mouse']['ey'] - io['edit_obj']['time']
                else:
                    io['edit_obj']['pitch'] = io['mouse']['ex']
                    
                DrawElements.draw_note(io['edit_obj'], io, new=False)
                    
        if event_type == 'btn1release':
            
            io['edit_obj'] = None
            io['old_obj'] = None
            io['ctlz'].add_ctlz(io['score'])

        if event_type == 'btn3click':
            
            # detect if we are clicking on a note and delete if so
            tags = io['editor'].gettags("current")
            if tags:
                if obj_type in tags[0]:
                    for note in io['score']['events']['note']:
                        if note['tag'] == tags[0]:
                            # delete note
                            # try to remove this note also from the selection buffer
                            try: io['selection']['selection_buffer']['note'].remove(note)
                            except: ... # if it fails the note isn't in the selection
                            io['editor'].delete(note['tag'])
                            io['score']['events']['note'].remove(note)
                            io['ctlz'].add_ctlz(io['score'])

    # ORNAMENT:
    @staticmethod
    def elm_ornament(event_type, io):

        obj_type = '#ornament'

        if event_type == 'btn1click':

            # set filechanged flag
            io['savefile_system']['filechanged'] = True

            # detect if we are editing a ornament or
            # in case we click not on a ornament, we
            # create a new_ornament.
            tags = io['editor'].gettags("current")
            if tags:
                if obj_type in tags[0]:
                    for orn in io['score']['events']['ornament']:
                        if orn['tag'] == tags[0]:
                            # starting to edit a note...
                            io['edit_obj'] = orn
                            # assign the currently selected hand:
                            io['edit_obj']['hand'] = io['hand']
                            return
            
            # create a new note
            new_ornament = {
                "tag":obj_type + str(ToolsEditor.add_tag(io)),
                "time":io['mouse']['ey'],
                "duration":io['snap_grid'],
                "pitch":io['mouse']['ex'],
                "hand":io['hand'],
                "accidental":0,
                "staff":0
            }
            DrawElements.draw_ornament(new_ornament, io, new=True)
            io['edit_obj'] = new_ornament
            io['old_obj'] = new_ornament

        if event_type in ['motion', 'space'] and io['cursor_on_editor']:

            # this gets executed if no mousebutton is pressed but we only move the mouse on the editor:
            if not io['mouse']['button1']:
                # draw the note cursor:
                cursor_note = {
                    "time":io['mouse']['ey'],
                    "pitch":io['mouse']['ex'],
                    "hand":io['hand'],
                    "stemless":True
                }
                DrawElements.draw_note_cursor(cursor_note, io)
            
            # this gets executed if the mousebtn1 is pressed:
            elif io['edit_obj']:
                # edit the notes length or pitch in the specific pianoscript way:
                if io['mouse']['ey'] >= io['edit_obj']['time']:
                    if io['mouse']['ey'] >= io['snap_grid'] + io['edit_obj']['time']:
                        io['edit_obj']['duration'] = io['mouse']['ey'] - io['edit_obj']['time']
                else:
                    io['edit_obj']['pitch'] = io['mouse']['ex']
                    
                DrawElements.draw_ornament(io['edit_obj'], io, new=False)
                    
        if event_type == 'btn1release':
            
            io['edit_obj'] = None
            io['old_obj'] = None
            io['ctlz'].add_ctlz(io['score'])

        if event_type == 'btn3click':
            
            # detect if we are clicking on a ornament and delete if so
            tags = io['editor'].gettags("current")
            if tags:
                if obj_type in tags[0]:
                    for ornament in io['score']['events']['ornament']:
                        if ornament['tag'] == tags[0]:
                            # delete ornament
                            # try to remove this ornament also from the selection buffer
                            try: io['selection']['selection_buffer']['ornament'].remove(ornament)
                            except: ... # if it fails the ornament isn't in the selection
                            io['editor'].delete(ornament['tag'])
                            io['score']['events']['ornament'].remove(ornament)
                            io['ctlz'].add_ctlz(io['score'])


    # COUNTLINE:
    @staticmethod
    def elm_countline(event_type, io):
        
        if event_type == 'btn1click':
            
            ...

        if event_type == 'motion':
            
            ...

        if event_type == 'btn1release':
            
            ...

        if event_type == 'btn3click':
            
            ...

    
    # BEAM:
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


    # ACCIDENTAL:
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


    # LINEBREAK:
    @staticmethod
    def elm_linebreak(event_type, io):
        
        if event_type == 'btn1click':
            
            # set filechanged flag
            io['savefile_system']['filechanged'] = True

            # ignore if click time == 0
            if io['mouse']['ey'] == 0:
                return
            
            # we use selection variables in io to determine dragging a linebreak if we do so
            io['selection']['y1'] = io['mouse']['ey']

            # hold_tag is used to detect the linebreak if we click on a linebreak time.
            for lbreak in io['score']['events']['linebreak']:
                if lbreak['time'] == io['mouse']['ey']:
                    io['hold_tag'] = lbreak
                    break

        if event_type == 'motion':
            
            if io['mouse']['button1']:
                io['selection']['y2'] = io['mouse']['ey']

        if event_type == 'btn1release':
            
            # if we edit/release an existing linebreak
            edit_flag = False
            if io['hold_tag']:
                for lbreak in io['score']['events']['linebreak']:
                    if lbreak == io['hold_tag']:
                        edit_flag = True

                    if edit_flag:
                        add = io['selection']['y2'] - io['selection']['y1']
                        lbreak['time'] += add

                        if lbreak['time'] >= io['last_pianotick']:
                            io['score']['events']['linebreak'].remove(lbreak)

            # if we didn't click on an existing linebreak we have to add a new one on the button release position
            else:
                new_linebreak = {
                    "tag":'linebreak' + str(ToolsEditor.add_tag(io)),
                    "time":io['mouse']['ey'],
                    "margin-staff1-left":10,
                    "margin-staff1-right":10,
                    "margin-staff2-left":10,
                    "margin-staff2-right":10,
                    "margin-staff3-left":10,
                    "margin-staff3-right":10,
                    "margin-staff4-left":10,
                    "margin-staff4-right":10
                  }
                io['new_tag'] += 1
                # add linebreak to file
                io['score']['events']['linebreak'].append(new_linebreak)
                io['score']['events']['linebreak'] = sorted(io['score']['events']['linebreak'], key=lambda time: time['time'])

            # update editor and engraver
            io['main_editor'].redraw_editor(io)
            io['engraver'].trigger_render()
            io['ctlz'].add_ctlz(io['score'])

            # empty selection variables
            io['selection']['y1'] = None
            io['selection']['y2'] = None
            io['hold_tag'] = ''

        if event_type == 'btn3click':

            # ignore if click time == 0
            if io['mouse']['ey'] == 0:
                return
            
            for lbreak in io['score']['events']['linebreak']:
                if lbreak['time'] == io['mouse']['ey']:
                    io['score']['events']['linebreak'].remove(lbreak)

            # update editor and engraver
            io['main_editor'].redraw_editor(io)
            io['engraver'].trigger_render()
            io['ctlz'].add_ctlz(io['score'])




