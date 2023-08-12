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
from imports.colors import color_dark, color_light
from imports.constants import BLACK

class DrawViewport:
    '''
        All elements in the editor viewport that are vissible 
        get refreshed. All outside the view are ignored. This
        means once a note is drawn it stays there.
    '''

    @staticmethod
    def draw(io):
        
        for note in io['score']['events']['note']:

            if note['time'] >= io['view_start_tick']-1024 and note['time']+note['duration'] < io['view_end_tick']+1024 or note['time']+note['duration'] >= io['view_start_tick']-1024 and note['time'] < io['view_end_tick']+1024:
                if not note['id'] in io['drawn_obj']: 
                    x = ToolsEditor.pitch2x(note['pitch'], io)
                    y = ToolsEditor.time2y(note['time'], io)
                    d = ToolsEditor.time2y(note['time']+note['duration'], io)

                    if note['pitch'] in BLACK:
                        fill = color_dark
                        width = 2
                    else:
                        fill = color_light
                        width = 4

                    sbar_width = io['sbar'].winfo_width()
                    editor_width = io['editor'].winfo_width() - sbar_width
                    editor_height = io['editor'].winfo_height()
                    staff_width = editor_width * io['xscale']
                    staff_margin = (editor_width - staff_width) / 2
                    scale = staff_width / 1024

                    # note:
                    io['editor'].create_oval(x-(10 * scale), y,
                        x+(10 * scale), y+(20 * scale), 
                        fill=fill, 
                        outline=color_dark, 
                        tag=(note['id'], 'note'), 
                        width=width*scale)
                    
                    # midinote:
                    io['editor'].create_polygon(x, y,
                        x+(10*scale), y+(10*scale),
                        x+(10*scale), d,
                        x-(10*scale), d,
                        x-(10*scale), y+(10*scale),
                        fill='grey', 
                        outline='grey',
                        tag=(note['id'], 'midinote'))

                    # stem (hand)
                    io['editor'].create_line(x, y,
                        x + (50*scale), y, 
                        capstyle='round',
                        tag=(note['id'], 'stem'),
                        width=6*scale,
                        fill=color_dark)

                    io['editor'].tag_lower('midinote')
                    io['drawn_obj'].append(note['id'])

            if note['time']+note['duration'] > io['view_end_tick']+1024:
                return

        
    