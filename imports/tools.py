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

'''
    In 'tools.py' are functions that are quickly invoked inside other 
    functions. Every function has a doc string to explain what it does
    or were it's used for.
'''
import time, math

def measure_length(numerator, denominator):
    '''
    returns the length in pianoticks (quarter == 256)
    '''
    return int(numerator * (1024 / denominator))


def interpolation(x, y, z):
    return (z - x) / (y - x)


def is_in_range(x, y, z):
    '''
    returns True if z is in between x and y.
    '''
    if z - x > 1 and y - z > 1:
        return True
    else:
        return False


def baseround(x, base=5):
    '''
        baseround rounds x to the closest base
    '''
    return round((x - (base / 2)) / base) * base


def barline_times(time_signatures):
    '''
        This function returns a list of
        times from every barline in the Score.
        It takes the grid from Score['events']['grid']
    '''
    bl_times = []
    count = 0
    for i,grid in enumerate(time_signatures):
        if i+1 == len(time_signatures): add = 1
        else: add = 0
        step = measure_length(grid['numerator'],grid['denominator'])
        for t in range(grid['amount']+add):
            bl_times.append(count)
            count += step
    return bl_times


def staff_height_width(mn, mx, scale):
    '''
    This function returns the height of a staff based on the
    lowest and highest piano-key-number.
    '''
    staffheight = 0

    if mx >= 81:
        staffheight = 260
    if mx >= 76 and mx <= 80:
        staffheight = 220
    if mx >= 69 and mx <= 75:
        staffheight = 190
    if mx >= 64 and mx <= 68:
        staffheight = 150
    if mx >= 57 and mx <= 63:
        staffheight = 120
    if mx >= 52 and mx <= 56:
        staffheight = 80
    if mx >= 45 and mx <= 51:
        staffheight = 50
    if mx >= 40 and mx <= 44:
        staffheight = 10
    if mx < 40:
        staffheight = 10
    if mn >= 33 and mn <= 39:
        staffheight += 40
    if mn >= 28 and mn <= 32:
        staffheight += 70
    if mn >= 21 and mn <= 27:
        staffheight += 110
    if mn >= 16 and mn <= 20:
        staffheight += 140
    if mn >= 9 and mn <= 15:
        staffheight += 180
    if mn >= 4 and mn <= 8:
        staffheight += 210
    if mn >= 1 and mn <= 3:
        staffheight += 230
    return staffheight * scale


def diff(x, y):
    if x >= y:
        return x - y
    else:
        return y - x


def do_popup(event, menu):
    try:
        menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()


def t_sig_start_tick(t_sig_map, n):
            out = []
            tick = 0
            for i in t_sig_map:
                out.append(tick)
                tick += measure_length(i['numerator'], i['denominator']) * i['amount']
            return out[n]


def update_bcounter(DOC, pageno):
    
    bcount = 0
    ret = False
    for pc, p in enumerate(DOC):
        if pc == pageno:
            ret = True
        for l in p:
            for e in l:
                if e['type'] == 'barline':
                    bcount += 1
                if ret:
                    return bcount

def note_split_processor(note, Score):
    '''
    Returns a list of notes and if the note 
    crosses a linebreak it creates a note split.
    '''
    splitted = []

    # creating a list of barline positions.
    line_breaks = Score['events']['linebreak']

    # detecting barline overlapping note.
    is_split = False
    split_points = []
    for i in line_breaks:
        if is_in_range(note['time'], note['time'] + note['duration'], i['time']):
            split_points.append(i['time'])
            is_split = True
    if not is_split:
        note['notestop'] = True
        splitted.append(note)
        return splitted
    elif is_split:
        start = note['time']
        end = note['time'] + note['duration']
        for i in range(0, len(split_points) + 1):
            if i == 0:  # if first iteration
                splitted.append({'type': 'note',
                            'pitch': note['pitch'],
                            'time': start,
                            'duration': split_points[0] - start,
                            'hand': note['hand'],
                            'notestop':False,
                            'stem-visible':note['stem-visible'],
                            'accidental':note['accidental'],
                            'staff':note['staff']})
            elif i == len(split_points):  # if last iteration
                splitted.append({'type': 'split',
                            'pitch': note['pitch'],
                            'time': split_points[i - 1],
                            'duration': end - split_points[i - 1],
                            'hand': note['hand'],
                            'notestop':True,
                            'stem-visible':note['stem-visible'],
                            'accidental':note['accidental'],
                            'staff':note['staff']})
                return splitted
            else:  # if not first and not last iteration
                splitted.append({'type': 'split', 
                            'pitch': note['pitch'], 
                            'time': split_points[i - 1],
                            'duration': split_points[i] - split_points[i - 1],
                            'hand': note['hand'],
                            'notestop':False,
                            'stem-visible':note['stem-visible'],
                            'accidental':note['accidental'],
                            'staff':note['staff']})


def round_rectangle(widget, x1, y1, x2, y2, radius=5, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]

    return widget.create_polygon(points, **kwargs, smooth=True)

def proper_round(num, dec=0):
    num = str(num)[:str(num).index('.')+dec+2]
    if num[-1]>='5':
        return float(num[:-2-(not dec)]+str(int(num[-2-(not dec)])+1))
    return float(num[:-1])


def set_pview_width(root,master_paned):
    w = root.winfo_width()
    for i in range(100):
        master_paned.configure(width=i)
        time.sleep(1000)

def get_first_available_staff(Score):
    
    staffs = Score['properties']['staff']
    for st in staffs:
        if st['onoff']:
            return st['staff-number']
    return -1

def evaluate_cubic_bezier(t, control_points):
    p0, p1, p2, p3 = control_points
    x = (1 - t) ** 3 * p0[0] + 3 * t * (1 - t) ** 2 * p1[0] + 3 * t ** 2 * (1 - t) * p2[0] + t ** 3 * p3[0]
    y = (1 - t) ** 3 * p0[1] + 3 * t * (1 - t) ** 2 * p1[1] + 3 * t ** 2 * (1 - t) * p2[1] + t ** 3 * p3[1]
    return x, y

def create_rotated_rectangle(canvas, x1, y1, x2, y2, angle=0, **kwargs):
    # Calculate the center of the rectangle
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    # Negate the angle to reverse the rotation direction
    angle = -angle

    # Convert the angle to radians
    angle_rad = math.radians(angle)

    # Calculate the sine and cosine of the angle
    cos_val = math.cos(angle_rad)
    sin_val = math.sin(angle_rad)

    # Calculate the rotated coordinates for the four corners
    x1_rot = center_x + cos_val * (x1 - center_x) - sin_val * (y1 - center_y)
    y1_rot = center_y + sin_val * (x1 - center_x) + cos_val * (y1 - center_y)
    x2_rot = center_x + cos_val * (x1 - center_x) - sin_val * (y2 - center_y)
    y2_rot = center_y + sin_val * (x1 - center_x) + cos_val * (y2 - center_y)
    x3_rot = center_x + cos_val * (x2 - center_x) - sin_val * (y2 - center_y)
    y3_rot = center_y + sin_val * (x2 - center_x) + cos_val * (y2 - center_y)
    x4_rot = center_x + cos_val * (x2 - center_x) - sin_val * (y1 - center_y)
    y4_rot = center_y + sin_val * (x2 - center_x) + cos_val * (y1 - center_y)

    # Draw the rotated rectangle on the canvas
    canvas.create_polygon(x1_rot, y1_rot, x2_rot, y2_rot, x3_rot, y3_rot, x4_rot, y4_rot, **kwargs)


def fit_printview(io, event=''):
    '''
        Sets the width of the printview in a way
        that the whole page fits on the screen.
    '''
    pview_height = io['pview'].winfo_height()
    page_width = io['score']['properties']['page-width']
    page_height = io['score']['properties']['page-height']
    app_width = io['root'].winfo_width()
    width = app_width - 215 - (page_width / page_height * pview_height) + 3 # correction
    io['main_paned'].paneconfig(io['toolbarpanel'], width=200)
    io['main_paned'].paneconfig(io['editorpanel'], width=width)
    io['root'].update()