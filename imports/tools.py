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


def measure_length(tsig):
    '''
    tsig is a tuple that contains: (numerator, denominator)
    returns the length in pianoticks (quarter == 256)
    '''
    n = tsig[0]
    d = 1024 / tsig[1]
    return int(n * d)


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
        It takes the grid from Savefile
    '''
    bl_times = []
    count = 0
    for i,grid in enumerate(time_signatures):
        if i+1 == len(time_signatures): add = 1
        else: add = 0
        step = measure_length((grid['numerator'],grid['denominator']))
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
                tick += measure_length((i['numerator'], i['denominator'])) * i['amount']
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
    line_breaks = Score['events']['line-break']

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
                            'notestop':False})
            elif i == len(split_points):  # if last iteration
                splitted.append({'type': 'split',
                            'pitch': note['pitch'],
                            'time': split_points[i - 1],
                            'duration': end - split_points[i - 1],
                            'hand': note['hand'],
                            'notestop':True})
                return splitted
            else:  # if not first and not last iteration
                splitted.append({'type': 'split', 
                            'pitch': note['pitch'], 
                            'time': split_points[i - 1],
                            'duration': split_points[i] - split_points[i - 1],
                            'hand': note['hand'],
                            'notestop':False})