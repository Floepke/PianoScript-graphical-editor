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
from imports.colors import color_dark, color_light, color_highlight
from imports.constants import BLACK
from imports.editor.editor_draw_elements import DrawElements

class DrawViewport:
    '''
        All elements in the editor viewport that are vissible 
        get refreshed. All outside the view are ignored. This
        means once a note is drawn it stays there.
    '''

    @staticmethod
    def draw(io):

        # NOTE:
        for note in io['score']['events']['note']:
            if note['time'] >= io['view_start_tick'] and note['time'] < io['view_end_tick'] or note['time']+note['duration'] >= io['view_start_tick'] and note['time']+note['duration'] < io['view_end_tick']:
                if not note['tag'] in io['drawn_obj']:
                    DrawElements.draw_note(note, io, new=False, selected=False)

        # LINEBREAK:
        for lbreak in io['score']['events']['linebreak']:

            if lbreak['time'] >= io['view_start_tick'] and lbreak['time'] < io['view_end_tick']:

                if not lbreak['tag'] in io['drawn_obj']: 
                    # draw linebreak
                    y = ToolsEditor.time2y(lbreak['time'], io)
                    sbar_width = io['sbar'].winfo_width()
                    editor_width = io['editor'].winfo_width() - sbar_width
                    editor_height = io['editor'].winfo_height()
                    staff_width = editor_width * io['xscale']
                    staff_margin = (editor_width - staff_width) / 2
                    scale = staff_width / 1000

                    io['editor'].create_line(sbar_width,y,editor_width+sbar_width,y,
                        dash=(10,10),
                        tag=('linebreak'),
                        width=4*scale,
                        fill='red')

                    # add to drawn list
                    io['drawn_obj'].append(lbreak['tag'])

        
    
