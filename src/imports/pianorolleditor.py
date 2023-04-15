'''
Copyright 2023 Philip Bergwerf

This program is part of the pianoscript project: http://www.pianoscript.org/

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

from imports.tools import *

def x2tick_editor(mx, editor, hbar, y_scale_percent, x_scale_quarter_mm, total_pianoticks, edit_grid, MM):
    '''
        This function converts the mouse position to
        (start) time in pianoticks.
    '''
    editor_height = editor.winfo_height() - hbar.winfo_height()
    staff_y_margin = (editor_height - (y_scale_percent * editor_height)) / 2
    editor_x_margin = staff_y_margin
    start = editor_x_margin
    end = editor_x_margin + (((x_scale_quarter_mm / 256) * MM) * total_pianoticks)
    if end - start == 0:
        return 0
    out = baseround(interpolation(start, end, mx) * total_pianoticks, edit_grid)
    if out < 0:
        return 0
    else:
        return out


def y2pitch_editor(y, editor, hbar, y_scale_percent):
    '''
        This function converts the mouse y position in 
        the editor to pitch in pianokey number 1 to 88.
    '''

    editor_height = editor.winfo_height() - hbar.winfo_height()
    staff_height = editor_height * y_scale_percent
    y_factor = staff_height / 490
    center_key88 = (editor_height - staff_height) / 2 - (15 * y_factor)
    y = y - center_key88
    
    cf = [4, 9, 16, 21, 28, 33, 40, 45, 52, 57, 64, 69, 76, 81, 88]
    be = [3, 8, 15, 20, 27, 32, 39, 44, 51, 56, 63, 68, 75, 80, 87]

    ylist = [510, 505, 500, 490, 485, 480, 475, 470, 460, 455, 450, 445, 440, 
    435, 430, 420, 415, 410, 405, 400, 390, 385, 380, 375, 370, 365, 360, 350, 
    345, 340, 335, 330, 320, 315, 310, 305, 300, 295, 290, 280, 275, 270, 265, 
    260, 250, 245, 240, 235, 230, 225, 220, 210, 205, 200, 195, 190, 180, 175, 
    170, 165, 160, 155, 150, 140, 135, 130, 125, 120, 110, 105, 100, 95, 90, 
    85, 80, 70, 65, 60, 55, 50, 40, 35, 30, 25, 20, 15, 10, 0]

    for yl, idx in zip(ylist, range(len(ylist))):
        yl *= y_factor
        if idx + 1 in cf:
            if y >= yl - (2.5 * y_factor) and y < yl + (5 * y_factor):
                return idx + 1
        elif idx + 1 in be:
            if y >= yl - (5 * y_factor) and y < yl + (2.5 * y_factor):
                return idx + 1
        else:
            if y >= yl - (2.5 * y_factor) and y < yl + (2.5 * y_factor):
                return idx + 1

    if y < ylist[-1] * y_factor:
        return 88
    if y > ylist[0] * y_factor:
        return 1


def time2x_editor(pianotick, editor, hbar, y_scale_percent, x_scale_quarter_mm, MM):
    '''
        This funtion converts pianotick
        to x position on the editor staff
    '''
    # calculate dimensions for staff (in px)
    editor_height = editor.winfo_height() - hbar.winfo_height()
    staff_y_margin = (editor_height - (y_scale_percent * editor_height)) / 2
    return staff_y_margin + (((x_scale_quarter_mm / 256) * MM) * pianotick)


def pitch2y_editor(pitch, editor, hbar, y_scale_percent):
    '''
        This funtion converts pitch
        to y position on the editor staff
    '''
    # calculate dimensions for staff (in px)
    editor_height = editor.winfo_height() - hbar.winfo_height()
    staff_xy_margin = (editor_height - (y_scale_percent * editor_height)) / 2
    staff_height = editor_height - staff_xy_margin - staff_xy_margin
    y_factor = staff_height / 490

    ylist = [510, 505, 500, 490, 485, 480, 475, 470, 460, 455, 450, 445, 440, 435, 
    430, 420, 415, 410, 405, 400, 390, 385, 380, 375, 370, 365, 360, 350, 345, 340, 
    335, 330, 320, 315, 310, 305, 300, 295, 290, 280, 275, 270, 265, 260, 250, 245, 
    240, 235, 230, 225, 220, 210, 205, 200, 195, 190, 180, 175, 170, 165, 160, 155, 
    150, 140, 135, 130, 125, 120, 110, 105, 100, 95, 90, 85, 80, 70, 65, 60, 55, 50, 
    40, 35, 30, 25, 20, 15, 10, 0]

    return staff_xy_margin + ((ylist[pitch-1] - 15) * y_factor)


def draw_note_pianoroll(note, 
    cursor, 
    editor, 
    hbar, 
    y_scale_percent, 
    x_scale_quarter_mm, 
    MM, 
    color_notation_editor, 
    BLACK, 
    color_editor_canvas, 
    Score, 
    color_right_midinote, 
    color_left_midinote,
    edit=False):
    '''
        This function essentially redraws a note
        in the pianoroll editor. It redraws all
        nessesary elements:
            - stem
            - notehead
            - whitespace
            - leftdot
            - midinote
            - notestop
        afterwards it updates the drawing order.

        I used a if/else control flow for defining
        how to draw exactly and tried to make it as
        efficient as possible...
    '''

    editor.delete(note['id'])

    # define x and y position on the editor canvas:
    # calculate dimensions for staff (in px)
    editor_height = editor.winfo_height() - hbar.winfo_height()
    staff_xy_margin = (editor_height - (y_scale_percent * editor_height)) / 2
    staff_height = editor_height - staff_xy_margin - staff_xy_margin
    y_factor = staff_height / 490
    x = time2x_editor(note['time'], 
        editor, 
        hbar, 
        y_scale_percent, 
        x_scale_quarter_mm,
        MM)
    x1 = time2x_editor(note['time'] + note['duration'], 
        editor, 
        hbar, 
        y_scale_percent, 
        x_scale_quarter_mm,
        MM)
    y = pitch2y_editor(note['pitch'], editor, hbar, y_scale_percent)

    state = 'normal'
    note_color = color_notation_editor
    if cursor:
        state = 'disabled'
        note_color = 'blue'# before it was blue

    # with the xy positions we draw:
    # notehead
    if note['pitch'] in BLACK:
        editor.create_oval(x,
            y-(5*y_factor),
            x+(5*y_factor),
            y+(5*y_factor),
            fill=note_color,
            outline=note_color,
            tag=(note['id'], 'notehead', 'blacknote'),
            state=state)
    else:
        editor.create_oval(x,
            y-(5*y_factor),
            x+(10*y_factor),
            y+(5*y_factor),
            width=2,
            fill=color_editor_canvas,
            outline=note_color,
            tag=(note['id'], 'notehead'),
            state=state)
    # stem
    if note['hand'] == 'r':
        editor.create_line(x,
            y,
            x,
            y-(20*y_factor),
            width=2,
            fill=note_color,
            tag=(note['id'], 'stem'),
            state=state)
        # barline white space
        bl_times = barline_times(Score['properties']['grid'])
        if note['time'] in bl_times:
            editor.create_line(x,
                y-(20*y_factor),
                x,
                y-(25*y_factor),
                width=2,
                tag=(note['id'], 'whitespace'),
                fill=color_editor_canvas)
            editor.create_line(x,
                y,
                x,
                y+(7.5*y_factor),
                width=2,
                tag=(note['id'], 'whitespace'),
                fill=color_editor_canvas)
    else:
        editor.create_line(x,
            y,
            x,
            y+(20*y_factor),
            width=2,
            fill=note_color,
            tag=(note['id'], 'stem'),
            state=state)
        # barline white space
        bl_times = barline_times(Score['properties']['grid'])
        if note['time'] in bl_times:
            editor.create_line(x,
                y+(20*y_factor),
                x,
                y+(25*y_factor),
                width=2,
                tag=(note['id'], 'whitespace'),
                fill=color_editor_canvas)
            editor.create_line(x,
                y,
                x,
                y-(7.5*y_factor),
                width=2,
                tag=(note['id'], 'whitespace'),
                fill=color_editor_canvas)
        # left dot
        if note['pitch'] in BLACK:
            r = 1.5
            editor.create_oval((x+(2.5*y_factor))+r,
                y-r,
                (x+(2.5*y_factor))-r,
                y+r,
                fill=color_editor_canvas,
                outline=color_editor_canvas,
                tag=(note['id'], 'blackdot'),
                state=state)
        else:
            r = 2
            editor.create_oval((x+(5*y_factor))+r,
                y-r,
                (x+(5*y_factor))-r,
                y+r,
                fill=note_color,
                outline=note_color,
                tag=(note['id'], 'whitedot'),
                state=state)
    # midinote
    if not cursor:    
        if note['hand'] == 'r':
            y0 = y - (5*y_factor)
            y1 = y + (5*y_factor)
            editor.create_polygon(x,
                y,
                x + (5 * y_factor),
                y0,
                x1 - (5 * y_factor),
                y0,
                x1,
                y,
                x1 - (5 * y_factor),
                y1,
                x + (5 * y_factor),
                y1,
                fill=color_right_midinote,#82d4e2#a7a885
                tag=(note['id'], 'midinote'))
        else:
            y0 = y - (5*y_factor)
            y1 = y + (5*y_factor)
            editor.create_polygon(x,
                y,
                x + (5 * y_factor),
                y0,
                x1 - (5 * y_factor),
                y0,
                x1,
                y,
                x1 - (5 * y_factor),
                y1,
                x + (5 * y_factor),
                y1,
                fill=color_left_midinote,#eea561#a7a885
                tag=(note['id'], 'midinote'))
        # notestop
        editor.create_line(x1,
            y-(5*y_factor),
            x1,
            y+(5*y_factor),
            width=2,
            fill=note_color,
            tag=(note['id'], 'notestop'))
    update_connectstem(note,editor,hbar,y_scale_percent,x_scale_quarter_mm,MM,Score,color_notation_editor, False,'r')
    update_connectstem(note,editor,hbar,y_scale_percent,x_scale_quarter_mm,MM,Score,color_notation_editor, False,'l')
    
    if edit:
        update_drawing_order_editor(editor)


def update_connectstem(note, 
        editor, 
        hbar,
        y_scale_percent,
        x_scale_quarter_mm,
        MM,Score,
        color_notation_editor, 
        remove=False, 
        hand='r'):
    # define x and y position on the editor canvas:
    # calculate dimensions for staff (in px)
    editor_height = editor.winfo_height() - hbar.winfo_height()
    staff_xy_margin = (editor_height - (y_scale_percent * editor_height)) / 2
    staff_height = editor_height - staff_xy_margin - staff_xy_margin
    y_factor = staff_height / 490
    x = time2x_editor(note['time'], editor, hbar, y_scale_percent, x_scale_quarter_mm, MM)
    
    # connect stems if two notes are starting at the same time
    buffer = []
    for evt in Score['events']['note']:
        if abs(evt['time'] - note['time']) <= 1 and evt['pitch'] != note['pitch'] and evt['hand'] == hand:
            buffer.append(evt)
    if not remove and note['hand'] == hand:  buffer.append(note)
    buffer = sorted(buffer, key=lambda x: x['pitch'])
    tags = ['connectstem']
    for pos in buffer:
        tags.append(pos['id'])
    if len(buffer) > 1:
        editor.create_line(x,
            pitch2y_editor(buffer[0]['pitch'], editor, hbar, y_scale_percent),
            x,
            pitch2y_editor(buffer[-1]['pitch'], editor, hbar, y_scale_percent),
            width=2,
            fill=color_notation_editor,
            tag=tags)


def update_drawing_order_editor(canvas):
    canvas.tag_raise('midinote')
    canvas.tag_raise('midi_note')
    canvas.tag_raise('staffline')
    canvas.tag_raise('notestop')
    canvas.tag_raise('whitespace')
    canvas.tag_raise('notehead')
    canvas.tag_raise('whitedot')
    canvas.tag_raise('blacknote')
    canvas.tag_raise('blackdot')
    canvas.tag_raise('stem')   
    canvas.tag_raise('new')
    canvas.tag_raise('connectstem')
    canvas.tag_raise('cursor')


def draw_linebreak_editor(linebreak,
    editor,
    hbar,
    y_scale_percent,
    x_scale_quarter_mm,
    MM,
    color_notation_editor,
    color_highlight,
    cursor=False):
    '''draws a newline symbol in the editor'''
    
    editor.delete(linebreak['id'])

    # define x and y position on the editor canvas:
    # calculate dimensions for staff (in px)
    editor_height = editor.winfo_height() - hbar.winfo_height()
    staff_xy_margin = (editor_height - (y_scale_percent * editor_height)) / 2
    staff_height = editor_height - staff_xy_margin - staff_xy_margin
    y_factor = staff_height / 490
    x = time2x_editor(linebreak['time'],
        editor, 
        hbar, 
        y_scale_percent, 
        x_scale_quarter_mm,
        MM)
    if cursor:
        editor.create_line(x,
            0,
            x,
            editor_height,
            width=2,
            tag='cursor',
            fill=color_highlight,
            dash=(1,2))
    else:
        editor.create_line(x,
            0,
            x,
            editor_height,
            width=2,
            dash=(10,6),
            tag=linebreak['id'],
            fill=color_notation_editor)
    editor.tag_lower(linebreak['id'])
    
