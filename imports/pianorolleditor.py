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

from imports.tools import *
import random

def rcolor():
    random_color = lambda: random.randint(0,255)
    rc ='#%02X%02X%02X' % (random_color(),random_color(),random_color())
    return rc

def x2tick_editor(mx, editor, hbar, y_scale_percent, x_scale_quarter_mm, total_pianoticks, edit_grid, MM, literal=False):
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
    if literal:
        out = interpolation(start, end, mx) * total_pianoticks
    else:
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
    edit=False,
    select=False):
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
        note_color = '#268bd2'
    color_right_midinote = Score['properties']['color-right-hand-midinote']
    color_left_midinote = Score['properties']['color-left-hand-midinote']
    if select:
        color_right_midinote = '#268bd2'
        color_left_midinote = '#268bd2'
        note_color = '#268bd2'

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
        if note['stem-visible']:
            editor.create_line(x,
                y,
                x,
                y-(20*y_factor),
                width=2,
                fill=note_color,
                tag=(note['id'], 'stem'),
                state=state)
            # barline white space
            bl_times = barline_times(Score['events']['grid'])
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
        if note['stem-visible']:
            editor.create_line(x,
                y,
                x,
                y+(20*y_factor),
                width=2,
                fill=note_color,
                tag=(note['id'], 'stem'),
                state=state)
            # barline white space
            bl_times = barline_times(Score['events']['grid'])
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
            editor.create_polygon(x,y,x1,y0,x1,y1,
                fill=color_right_midinote,
                tag=(note['id'], 'midinote'))
        else:
            y0 = y - (5*y_factor)
            y1 = y + (5*y_factor)
            editor.create_polygon(x,y,x1,y0,x1,y1,
                fill=color_left_midinote,
                tag=(note['id'], 'midinote'))
        # notestop
        editor.create_line(x1,
            y-(5*y_factor),
            x1,
            y+(5*y_factor),
            width=2,
            fill=note_color,
            tag=(note['id'], 'notestop'))
    if note['stem-visible']:
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
    canvas.tag_raise('countline')
    canvas.tag_raise('texttext')
    canvas.tag_raise('staffsizer')
    canvas.tag_raise('startrepeat')
    canvas.tag_raise('endrepeat')


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
            editor_height * 0.2 / 2,
            width=4,
            tag=linebreak['id'],
            fill=color_highlight)
        editor.create_line(x,
            editor_height - (editor_height * 0.2 / 2),
            x,
            editor_height - (editor_height * 0.2 / 2) + editor_height * 0.2 / 2,
            width=4,
            tag=linebreak['id'],
            fill=color_highlight)
    else:
        editor.create_line(x,
            0,
            x,
            editor_height,
            width=2,
            dash=(10,6),
            tag=linebreak['id'],
            fill='green')
    editor.tag_raise(linebreak['id'])


def draw_cursor_editor(cursor,
    editor,
    hbar,
    y_scale_percent,
    x_scale_quarter_mm,
    MM,
    color_highlight,
    beam):
    '''draws a newline symbol in the editor'''
    
    editor.delete(cursor['id'])

    # define x and y position on the editor canvas:
    # calculate dimensions for staff (in px)
    editor_height = editor.winfo_height() - hbar.winfo_height()
    x = time2x_editor(cursor['time'],
        editor, 
        hbar, 
        y_scale_percent, 
        x_scale_quarter_mm,
        MM)
    if beam:
        if beam == 'up':
            editor.create_line(x,
                0,
                x,
                editor_height * 0.2 / 2,
                width=4,
                tag=cursor['id'],
                fill=color_highlight,
                arrow='first',
                arrowshape=(20,20,20))
            editor.create_line(x,
                editor_height - (editor_height * 0.2 / 2),
                x,
                editor_height - (editor_height * 0.2 / 2) + editor_height * 0.2 / 2,
                width=4,
                tag=cursor['id'],
                fill=color_highlight)
        else:
            editor.create_line(x,
                0,
                x,
                editor_height * 0.2 / 2,
                width=4,
                tag=cursor['id'],
                fill=color_highlight)
            editor.create_line(x,
                editor_height - (editor_height * 0.2 / 2),
                x,
                editor_height - (editor_height * 0.2 / 2) + editor_height * 0.2 / 2,
                width=4,
                tag=cursor['id'],
                fill=color_highlight,
                arrow='last',
                arrowshape=(20,20,20))
    else:
        editor.create_line(x,
            0,
            x,
            editor_height * 0.2 / 2,
            width=4,
            tag=cursor['id'],
            fill=color_highlight)
        editor.create_line(x,
            editor_height - (editor_height * 0.2 / 2),
            x,
            editor_height - (editor_height * 0.2 / 2) + editor_height * 0.2 / 2,
            width=4,
            tag=cursor['id'],
            fill=color_highlight)

    
def draw_select_rectangle(selection, editor):
    '''
        We redraw the select rectangle in this function.
    '''

    editor.delete('selectionrectangle')

    x1 = selection['x1']#time2x_editor(selection['time1'], editor, hbar, y_scale_percent, x_scale_quarter_mm, MM)
    y1 = selection['y1']#pitch2y_editor(selection['pitch1'], editor, hbar, y_scale_percent)
    x2 = selection['x2']#time2x_editor(selection['time2'], editor, hbar, y_scale_percent, x_scale_quarter_mm, MM)
    y2 = selection['y2']#pitch2y_editor(selection['pitch2'], editor, hbar, y_scale_percent)
    editor.create_rectangle(x1,
        y1,
        x2,
        y2,
        outline='#268bd2',
        width=4,
        tag='selectionrectangle',
        fill='')


def slur_editor(editor, slur, idd, draw_scale, thickness=7.5, steps=100, drawcontrols=True):
    '''
    Draws a musical slur on the given tkinter canvas with the given parameters.
    controls is a list with four xy positions for drawing a bezier curve. This 
    function draws two bezier curves to form a slur.
    '''

    editor.delete(idd)

    def evaluate_cubic_bezier(t, control_points):
        p0, p1, p2, p3 = control_points
        x = (1 - t) ** 3 * p0[0] + 3 * t * (1 - t) ** 2 * p1[0] + 3 * t ** 2 * (1 - t) * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * t * (1 - t) ** 2 * p1[1] + 3 * t ** 2 * (1 - t) * p2[1] + t ** 3 * p3[1]
        return x, y
    
    # define control points
    ctl1 = slur[0]
    ctl2 = slur[1]
    ctl3 = slur[2]
    ctl4 = slur[3]

    # calculate slur
    slur_points = []
    for t in range(steps):
        x, y = evaluate_cubic_bezier(t / steps, slur)
        slur_points.append([x, y])
    thickness_x = thickness * (ctl4[0] / ctl1[1])
    thickness_y = thickness * (ctl4[1] / ctl1[0])
    for t in reversed(range(steps)):
        x, y = evaluate_cubic_bezier(t / steps, 
            [ctl1,(ctl2[0]+thickness_x,ctl2[1]+thickness_y),(ctl3[0]+thickness_x,ctl3[1]+thickness_y),ctl4])
        slur_points.append([x, y])
    
    # draw slur
    editor.create_polygon(slur_points, 
        fill='black', 
        tag=idd,
        width=4*draw_scale)
    
    # draw control points
    if drawcontrols:
        r = 10
        editor.create_oval(ctl1[0]-r,
            ctl1[1]-r,
            ctl1[0]+r,
            ctl1[1]+r,
            tag=idd,
            fill='yellow',
            outline='')
        editor.create_oval(ctl2[0]-r,
            ctl2[1]-r,
            ctl2[0]+r,
            ctl2[1]+r,
            tag=idd,
            fill='#268bd2',
            outline='')
        editor.create_oval(ctl3[0]-r,
            ctl3[1]-r,
            ctl3[0]+r,
            ctl3[1]+r,
            tag=idd,
            fill='#268bd2',
            outline='')
        editor.create_oval(ctl4[0]-r,
            ctl4[1]-r,
            ctl4[0]+r,
            ctl4[1]+r,
            tag=idd,
            fill='yellow',
            outline='')


def draw_countline_editor(countline, 
    editor, hbar, y_scale_percent, 
    x_scale_quarter_mm, MM, color_notation_editor='#002b66'):
    
    editor.delete(countline['id'])

    t = time2x_editor(countline['time'], editor, hbar, y_scale_percent, x_scale_quarter_mm, MM)
    p1 = pitch2y_editor(countline['pitch1'], editor, hbar, y_scale_percent)
    p2 = pitch2y_editor(countline['pitch2'], editor, hbar, y_scale_percent)
    editor.create_line(t,p1,t,p2,
        fill=color_notation_editor,
        width=1,
        dash=(2,2),
        tag=(countline['id'], 'countline'))
    editor.create_rectangle(t-5,p1-5,t+5,p1+5,
        fill='green',
        outline='',
        tag=(countline['id'], 'handle1', 'countline'))
    editor.create_rectangle(t-5,p2-5,t+5,p2+5,
        fill='green',
        outline='',
        tag=(countline['id'], 'handle2', 'countline'))


def draw_text_editor(text,
    editor, hbar, y_scale_percent, 
    x_scale_quarter_mm, MM, color_notation_editor='#002b66'):
    
    editor.delete(text['id'])

    t = time2x_editor(text['time'], editor, hbar, y_scale_percent, x_scale_quarter_mm, MM)
    p = pitch2y_editor(text['pitch'], editor, hbar, y_scale_percent)
    if text['vert'] == 1:
        angle = 90
        anchor = 'nw'
    else:
        angle = 0
        anchor = 'w'

    mytext = editor.create_text(t,p,
        text=text['text'],
        anchor=anchor,
        tag=(text['id'], 'textfg', 'texttext'),
        angle=angle)
    bb = editor.bbox(mytext)
    w = bb[2]-bb[0]
    h = bb[3]-bb[1]
    if text['vert'] == 1:
        editor.create_rectangle(t,p,
            t+w,p-h,
            fill='#eee8d5',
            outline='#268bd2',
            tag=(text['id'],'textbg', 'texttext'))
    else:
        editor.create_rectangle(t,p-(h/2),
            t+w,p+(h/2),
            fill='#eee8d5',
            outline='#268bd2',
            tag=(text['id'],'textbg', 'texttext'))
    editor.tag_raise('textbg')
    editor.tag_raise('textfg')

def draw_staffsizer_editor(sizer, 
    editor, hbar, y_scale_percent, 
    x_scale_quarter_mm, MM, color_notation_editor='#002b66'):
    
    editor.delete(sizer['id'])
    t = time2x_editor(sizer['time'], editor, hbar, y_scale_percent, x_scale_quarter_mm, MM)
    p = pitch2y_editor(sizer['pitch'], editor, hbar, y_scale_percent)
    if sizer['pitch'] < 40:
        editor.create_polygon(t-10,p-10,t+10,p-10,t,p+10,outline='',fill='red',tag=(sizer['id'], 'staffsizer'))
    else:
        editor.create_polygon(t-10,p+10,t+10,p+10,t,p-10,outline='',fill='red',tag=(sizer['id'], 'staffsizer'))

def draw_startrepeat_editor(repeat, 
    editor, hbar, y_scale_percent, 
    x_scale_quarter_mm, MM, color_notation_editor='#002b66'):
    
    editor.delete(repeat['id'])
    t = time2x_editor(repeat['time'], editor, hbar, y_scale_percent, x_scale_quarter_mm, MM)
    editor_height = editor.winfo_height() - hbar.winfo_height()
    staff_xy_margin = (editor_height - (y_scale_percent * editor_height)) / 2  
    
    editor.create_line(t,staff_xy_margin,
        t,staff_xy_margin/2,
        width=2,
        tag=(repeat['id'],'startrepeat'),
        fill='purple')
    editor.create_line(t,staff_xy_margin/2,
        t+40,staff_xy_margin/2,
        arrow='last',
        width=4,
        tag=(repeat['id'], 'startrepeat'),
        fill='purple')

def draw_endrepeat_editor(repeat, 
    editor, hbar, y_scale_percent, 
    x_scale_quarter_mm, MM, color_notation_editor='#002b66'):
    
    editor.delete(repeat['id'])
    t = time2x_editor(repeat['time'], editor, hbar, y_scale_percent, x_scale_quarter_mm, MM)
    editor_height = editor.winfo_height() - hbar.winfo_height()
    staff_xy_margin = (editor_height - (y_scale_percent * editor_height)) / 2  
    
    editor.create_line(t,staff_xy_margin,
        t,staff_xy_margin/2,
        width=2,
        tag=(repeat['id'], 'endrepeat'),
        fill='purple')
    editor.create_line(t,staff_xy_margin/2,
        t-40,staff_xy_margin/2,
        arrow='last',
        width=4,
        tag=(repeat['id'], 'endrepeat'),
        fill='purple')


def draw_beam_editor(beam,
    editor, hbar, y_scale_percent, 
    x_scale_quarter_mm, MM, color_notation_editor='#002b66'):

    editor_height = editor.winfo_height() - hbar.winfo_height()
    staff_xy_margin = (editor_height - (y_scale_percent * editor_height)) / 2  
    staff_height = editor_height - staff_xy_margin - staff_xy_margin

    editor.delete(beam['id'])

    start = time2x_editor(beam['time'], editor, hbar, y_scale_percent, x_scale_quarter_mm, MM)
    end = time2x_editor(beam['time']+beam['duration'], editor, hbar, y_scale_percent, x_scale_quarter_mm, MM)
    if beam['hand'] == 'r':    
        editor.create_line(start,staff_xy_margin/2,
                        end,staff_xy_margin/2,
                        fill='#c83f49',
                        width=5,
                        capstyle='round',
                        tag=(beam['id'],'beam') )
        editor.create_line(start,staff_xy_margin/2,
                        start,staff_xy_margin/2+20,
                        fill='#c83f49',
                        width=2,
                        capstyle='round',
                        tag=(beam['id'],'beam'))
        editor.create_line(end,staff_xy_margin/2,
                        end,staff_xy_margin/2+20,
                        end-10,staff_xy_margin/2+25,
                        fill='#c83f49',
                        width=2,
                        capstyle='round',
                        tag=(beam['id'],'beam'))
    else:    
        editor.create_line(start,staff_xy_margin+staff_height+(staff_xy_margin/2),
                        end,staff_xy_margin+staff_height+(staff_xy_margin/2),
                        fill='#c83f49',
                        width=5,
                        capstyle='round',
                        tag=(beam['id'],'beam'))
        editor.create_line(start,staff_xy_margin+staff_height+(staff_xy_margin/2),
                        start,staff_xy_margin+staff_height+(staff_xy_margin/2)-20,
                        fill='#c83f49',
                        width=2,
                        capstyle='round',
                        tag=(beam['id'],'beam'))
        editor.create_line(end,staff_xy_margin+staff_height+(staff_xy_margin/2),
                        end,staff_xy_margin+staff_height+(staff_xy_margin/2)-20,
                        end-10,staff_xy_margin+staff_height+(staff_xy_margin/2)-25,
                        fill='#c83f49',
                        width=2,
                        capstyle='round',
                        tag=(beam['id'],'beam'))
    
    
