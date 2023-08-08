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

from imports.colors import color_dark

class DrawStaff():

    @staticmethod
    def draw_staff(io):
        '''Draws/updates staff-lines, grid and barlines in the editor'''
        
        # calculating dimensions
        score = io['score']
        io['editor'].update()
        editor_width = io['editor'].winfo_width()
        editor_height = io['editor'].winfo_height()
        staff_width = editor_width * io['xscale']
        staff_margin = (editor_width - staff_width) / 2
        x_factor = staff_width / 490
        yscale = io['ticksizepx']

        # check if we need to redraw the stafflines:
        if io['editor_width'] != editor_width or io['redraw_editor']:
            # first delete old stafflines
            io['editor'].delete('staffline')
            # draw staff
            x_curs = staff_margin

            #io['last_pianotick'] = editor_height

            io['editor'].create_line(x_curs,0,
                                    x_curs,io['last_pianotick']*yscale,
                                    width=2,
                                    tag='staffline',
                                    fill=color_dark,
                                    state='disabled')

            x_curs += 20 * x_factor

            for staff in range(7):

                for line in range(2):
                    if staff == 3:
                        io['editor'].create_line(x_curs,0,
                            x_curs,io['last_pianotick']*yscale,
                            width=1,
                            tag='staffline',
                            dash=(6,6),
                            fill=color_dark,
                            state='disabled')
                    else:
                        io['editor'].create_line(x_curs,0,
                            x_curs,io['last_pianotick']*yscale,
                            width=1,
                            tag='staffline',
                            fill=color_dark,
                            state='disabled')
                    x_curs += 10 * x_factor

                x_curs += 10 * x_factor

                for line in range(3):
                    io['editor'].create_line(x_curs,0,
                                            x_curs,io['last_pianotick']*yscale,
                                            width=2,
                                            tag='staffline',
                                            fill=color_dark,
                                            state='disabled')
                    x_curs += 10 * x_factor

                x_curs += 10 * x_factor
