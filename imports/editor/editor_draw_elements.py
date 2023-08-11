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
            tag='cursor', width=4, fill=color_dark)
        io['editor'].create_line(sbar_width+editor_width-staff_margin, time,
            sbar_width+editor_width, time,
            tag='cursor', width=4, fill=color_dark)

        if cursor['pitch'] in BLACK:
            fill = color_dark
        else:
            fill = color_light
        x = ToolsEditor.pitch2x(cursor['pitch'], io)
        y = ToolsEditor.time2y(cursor['time'], io)
        io['editor'].create_oval(x-(10 * io['xscale']), y,
            x+(10 * io['xscale']), y+20, fill=fill, outline=color_dark, tag='cursor', width=2)

    @staticmethod
    def draw_note_lr(note, io):
        
        ...
