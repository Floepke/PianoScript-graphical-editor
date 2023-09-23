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

from imports.editor.tools_editor import ToolsEditor
from imports.colors import color_highlight, color_dark, color_light
from imports.constants import BLACK


class DrawElements:

    @staticmethod
    def draw_cursor_indicator(cursor, io):
        '''
            Draws the cursor indicator for each individual 
        '''

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

    @staticmethod
    def draw_note_cursor(note, io):
        
        if not io['mouse']['button1']:

            # calculating dimensions...
            sbar_width = io['sbar'].winfo_width()
            editor_width = io['editor_width'] - sbar_width
            staff_width = editor_width * io['xscale']
            staff_margin = (editor_width - staff_width) / 2
            scale = staff_width / 1000

            p = ToolsEditor.pitch2x(note['pitch'], io)
            t = ToolsEditor.time2y(note['time'], io)

            io['editor'].delete('notecursor')

            # note
            if note['pitch'] in BLACK:
                io['editor'].create_oval(p-(10*scale), t,
                    p+(10*scale), t+(20*scale),
                    tag=('notecursor'),
                    fill=color_dark,
                    outline=color_dark,
                    width=4*scale,
                    state='disabled')
            else:
                io['editor'].create_oval(p-(10*scale), t,
                    p+(10*scale), t+(20*scale),
                    tag=('notecursor'),
                    fill=color_light,
                    outline=color_dark,
                    width=4*scale,
                    state='disabled')

            # leftdot (hand)
            if note['hand'] == 'l':
                if note['pitch'] in BLACK:
                    io['editor'].create_oval(p-(2 * scale), t+(8*scale),
                        p+(2 * scale), t+(12 * scale),
                        tag=('leftdot', 'notecursor'),
                        outline='',
                        fill=color_light,
                        state='disabled')
                else:
                    io['editor'].create_oval(p-(2 * scale), t+(8*scale),
                        p+(2 * scale), t+(12 * scale),
                        tag=('leftdot', 'notecursor'),
                        outline='',
                        fill=color_dark,
                        state='disabled')

            # stem (hand)
            if note['hand'] == 'l':
                io['editor'].create_line(p, t,
                    p - (50*scale), t, 
                    capstyle='round',
                    tag=('stem', 'notecursor'),
                    width=6*scale,
                    fill=color_dark,
                    state='disabled')
            else:
                io['editor'].create_line(p, t,
                    p + (50*scale), t, 
                    capstyle='round',
                    tag=('stem', 'notecursor'),
                    width=6*scale,
                    fill=color_dark,
                    state='disabled')
            io['editor'].tag_raise('notecursor')

    @staticmethod
    def draw_note(note, io, new=True, selected=False):
        '''
            draws or redraws the given 'note' in the editor.
            get's called for both creation and updating a note.
        '''
        x = ToolsEditor.pitch2x(note['pitch'], io)
        y = ToolsEditor.time2y(note['time'], io)
        d = ToolsEditor.time2y(note['time']+note['duration'], io)

        # calculating dimensions...
        sbar_width = io['sbar'].winfo_width()
        editor_width = io['editor_width'] - sbar_width
        staff_width = editor_width * io['xscale']
        staff_margin = (editor_width - staff_width) / 2
        scale = staff_width / 1000

        io['editor'].delete(note['tag'])

        # configure note color
        if selected: color = color_highlight
        else: color = color_dark
        if selected: color_midinote = color_highlight
        else: color_midinote = io['editor_settings']['note_color']

        # midinote:
        io['editor'].create_polygon(x, y,
            x+(10*scale), y+(10*scale),
            x+(10*scale), d,
            x-(10*scale), d,
            x-(10*scale), y+(10*scale),
            fill=color_midinote,
            outline=color_midinote,
            tag=(note['tag'], 'midinote'))

        # leftdot:
        if note['hand'] == 'l':
            
            if note['pitch'] in BLACK:
                io['editor'].create_oval(x-(2 * scale), y+(8*scale),
                    x+(2 * scale), y+(12 * scale),
                    tag=(note['tag'], 'leftdot'),
                    outline='',
                    fill=color_light)
            else:
                io['editor'].create_oval(x-(2 * scale), y+(8*scale),
                    x+(2 * scale), y+(12 * scale),
                    tag=(note['tag'], 'leftdot'),
                    outline='',
                    fill=color)
        
        # note:
        if note['pitch'] in BLACK:
            # black note
            io['editor'].create_oval(x-(10 * scale), y,
                x+(10 * scale), y+(20 * scale), 
                fill=color, 
                outline=color, 
                tag=(note['tag'], 'note', 'blacknote'), 
                width=4*scale)
        else:
            # white note
            io['editor'].create_oval(x-(10 * scale), y,
                x+(10 * scale), y+(20 * scale), 
                fill=color_light, 
                outline=color, 
                tag=(note['tag'], 'note', 'blacknote'), 
                width=4*scale)

        # stem (hand)
        if note['hand'] == 'l':
            io['editor'].create_line(x, y,
                x - (50*scale), y, 
                capstyle='round',
                tag=(note['tag'], 'stem'),
                width=6*scale,
                fill=color)
        else:
            io['editor'].create_line(x, y,
                x + (50*scale), y, 
                capstyle='round',
                tag=(note['tag'], 'stem'),
                width=6*scale,
                fill=color)

        # continuation dot
        ...

        # stop sign
        ...

        # add to drawn list
        io['drawn_obj'].append(note['tag'])

        # update the edited or new note in the save file (io['score']).
        if not new:
            for obj in io['score']['events']['note']:
                if obj['tag'] == note['tag']: 
                    obj = note
        else:
            io['score']['events']['note'].append(note)

        # update drawing order for note
        io['editor'].tag_lower(note['tag'])
        io['editor'].tag_raise('stem')
        io['editor'].tag_raise('continuationdot')
        io['editor'].tag_raise('note')
        io['editor'].tag_raise('blacknote')
        io['editor'].tag_raise('leftdot')

    @staticmethod
    def draw_selection_rectangle(io):
        
        io['editor'].delete('selectionrectangle')
        io['editor'].create_rectangle(io['selection']['x1'], io['selection']['y1'],
            io['selection']['x2'], io['selection']['y2'],
            fill='',
            outline=color_highlight,
            width=4,
            tag='selectionrectangle')

    @staticmethod
    def draw_beam(beam, io, new=True, selected=False):
        ...

    @staticmethod
    def draw_countline(countline, io, new=True, selected=False):
        ...

    @staticmethod
    def draw_slur(slur, io, new=True, selected=False):
        ...

    @staticmethod
    def draw_text(text, io, new=True, selected=False):
        ...

    @staticmethod
    def draw_pedal(pedal, io, new=True, selected=False):
        ...
