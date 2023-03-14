
# --------------------
# IMPORTS
# --------------------
from tkinter import Tk, Canvas, Menu, Scrollbar, messagebox, PanedWindow, Listbox, Text
from tkinter import filedialog, Button, Label, Spinbox, StringVar
from tkinter import simpledialog
import ast, platform, subprocess, os, math, threading, random
from mido import MidiFile
from shutil import which
import tkinter.ttk as ttk

# --------------------
# GUI
# --------------------
color1 = '#444444'  # d9d9d9
# root
root = Tk()
root.title('PianoScript')
ttk.Style(root).theme_use("alt")
scrwidth = root.winfo_screenwidth()
scrheight = root.winfo_screenheight()
root.geometry("%sx%s+0+0" % (int(scrwidth), int(scrheight)))
# PanedWindow
orient = 'h'
# master
panedmaster = PanedWindow(root, orient='h', sashwidth=0, relief='flat', bg=color1)
panedmaster.place(relwidth=1, relheight=1)
leftpanel = PanedWindow(panedmaster, relief='flat', bg=color1, width=50)
panedmaster.add(leftpanel)
midpanel = PanedWindow(panedmaster, relief='flat', bg=color1, orient='h', sashwidth=10, width=scrwidth * 0.8)
panedmaster.add(midpanel)
rightpanel = PanedWindow(midpanel, relief='flat', bg=color1)
midpanel.add(rightpanel)
# editor panel
root.update()
editorpanel = PanedWindow(midpanel, relief='groove', orient='h', bg=color1, width=(scrwidth - 50) / 3 * 2)
midpanel.add(editorpanel)
# print panel
printpanel = PanedWindow(midpanel, relief='groove', orient='h', bg=color1)
midpanel.add(printpanel)
# editor --> editorpanel
editor = Canvas(editorpanel, bg='white', relief='flat')
editor.place(relwidth=1, relheight=1)
hbar = Scrollbar(editor, orient='horizontal', width=20, relief='flat', bg=color1)
hbar.pack(side='bottom', fill='x')
hbar.config(command=editor.xview)
editor.configure(xscrollcommand=hbar.set)
# printview --> printpanel
pview = Canvas(printpanel, bg='white', relief='flat')
pview.place(relwidth=1, relheight=1)

separator2 = ttk.Separator(leftpanel, orient='horizontal').pack(fill='x')
noteinput_label = Label(leftpanel, text='GRID', bg=color1, fg='white', anchor='w', font=("courier"))
noteinput_label.pack(fill='x')
list_dur = Listbox(leftpanel, height=8, bg='grey')
list_dur.pack(fill='x')
list_dur.insert(0, "1")
list_dur.insert(1, "2")
list_dur.insert(2, "4")
list_dur.insert(3, "8")
list_dur.insert(4, "16")
list_dur.insert(5, "32")
list_dur.insert(6, "64")
list_dur.insert(7, "128")
list_dur.select_set(3)
divide_label = Label(leftpanel, text='÷', font=("courier", 20, "bold"), bg=color1, fg='white', anchor='w')
divide_label.pack(fill='x')
divide_spin = Spinbox(leftpanel, from_=1, to=100, bg='grey', font=('', 15, 'normal'))
divide_spin.pack(fill='x')
times_label = Label(leftpanel, text='×', font=("courier", 20, "bold"), bg=color1, fg='white', anchor='w')
times_label.pack(fill='x')
times_spin = Spinbox(leftpanel, from_=1, to=100, bg='grey', font=('', 15, 'normal'))
times_spin.pack(fill='x')
separator3 = ttk.Separator(rightpanel, orient='horizontal').pack(fill='x')
fill_label5 = Label(rightpanel, text='GRID MAP EDITOR', bg=color1, fg='white', anchor='w', font=("courier"))
fill_label5.pack(fill='x')
help_button1 = Button(rightpanel, text='?', font=("courier", 12, 'bold'))
help_button1.pack(fill='x')
gridedit_text = Text(rightpanel, bg='grey', height=6)
gridedit_text.pack(fill='x')
applygrid_button = Button(rightpanel, text='Apply', anchor='w')
applygrid_button.pack(fill='x')
separator4 = ttk.Separator(rightpanel, orient='horizontal').pack(fill='x')
fill_label9 = Label(rightpanel, text='', bg=color1, fg='white', anchor='w', font=("courier"))
fill_label9.pack(fill='x')
fill_label7 = Label(rightpanel, text='SYSTEM MARGIN EDITOR', bg=color1, fg='white', anchor='w', font=("courier"))
fill_label7.pack(fill='x')
help_button2 = Button(rightpanel, text='?', font=("courier", 12, 'bold'))
help_button2.pack(fill='x')
systemspace_text = Text(rightpanel, bg='grey', height=6)
systemspace_text.pack(fill='x')
applyspace_button = Button(rightpanel, text='Apply', anchor='w')
applyspace_button.pack(fill='x')
separator5 = ttk.Separator(rightpanel, orient='horizontal').pack(fill='x')
fill_label10 = Label(rightpanel, text='', bg=color1, fg='white', anchor='w', font=("courier"))
fill_label10.pack(fill='x')
fill_label11 = Label(rightpanel, text='MEASURE DIVISION EDITOR', bg=color1, fg='white', anchor='w', font=("courier"))
fill_label11.pack(fill='x')
help_button3 = Button(rightpanel, text='?', font=("courier", 12, 'bold'))
help_button3.pack(fill='x')
measureseachline_text = Text(rightpanel, bg='grey', height=6)
measureseachline_text.pack(fill='x')
applymeasures_button = Button(rightpanel, text='Apply', anchor='w')
applymeasures_button.pack(fill='x')

# ------------------
# constants
# ------------------
QUARTER = 256
MM = root.winfo_fpixels('1m')
PAPER_HEIGHT = MM * 297  # a4 210x297 mm
PAPER_WIDTH = MM * 210
XYMARGIN = 50
XYPAPER = 50
MARGIN = 30
PRINTEAREA_WIDTH = PAPER_WIDTH - (MARGIN * 2)
PRINTEAREA_HEIGHT = PAPER_HEIGHT - (MARGIN * 2)
MIDINOTECOLOR = '#b4b4b4'
BLACK = [2, 5, 7, 10, 12, 14, 17, 19, 22, 24, 26, 29, 31, 34, 36, 38, 41, 43, 46,
         48, 50, 53, 55, 58, 60, 62, 65, 67, 70, 72, 74, 77, 79, 82, 84, 86]
FULLSTAFFHEIGHT = 490
HELP1 = '''Grid map editor is used to define the grid of the music.
You can enter the grid by passing a row of values 
seperated by space on each line. The values are:
time-signature|amount-of-measures|grid-division|t-sig-visible-on-paper(1 or 0)
"4/4 16 4 1" creates 16 measures of 4/4 time-signature with a grid-division of 
4 and the time-signature change is visible on the sheet.

You can create as many messages (one each line) as you want to form the grid.'''

HELP2 = '''System margin editor is used to be able to set
the margin for each individual line of music in the score.

You can enter a list of integers(in mm) how much space you want around the lines
of music. If you enter one value it will apply to the current and all following lines.'''

HELP3 = ''''''


# --------------------------------------------------------
# TOOLS (notation design, help functions etc...)
# --------------------------------------------------------
def measure_length(tsig):
    '''
    tsig is a tuple containg; (numerator, denominator)
    returns the length in ticks where tpq == ticks per quarter
    '''
    n = tsig[0]
    d = 1024 / tsig[1]
    return int(n * d)


def interpolation(x, y, z):
    return (z - x) / (y - x)


def is_in_range(x, y, z):
    '''
    returns true if z is in between x and y.
    '''
    if z - x > 1 and y - z > 1:
        return True
    else:
        return False


def barline_ticks(FILE):
    '''
    This functions returns a list of all barline
    positions in the score based on the time signatures in FILE.
    also adds the endline-tick
    '''
    bln_time = []
    time = 0

    for grid, idx in zip(FILE[0][0], range(len(FILE[0][0]))):
        length = measure_length((grid['numerator'], grid['denominator']))
        for bl in range(grid['amount']):
            bln_time.append(time)
            time += length
        # adding endline-tick
        if idx == len(FILE[0][0]) - 1:
            bln_time.append(time)

    return bln_time


def note_split_processor(note):
    '''
    Returns a list of notes and if nessesary note split
    '''
    out = []

    # creating a list of barline positions.
    b_lines = barline_ticks(FILE)

    # detecting barline overlapping note.
    is_split = False
    split_points = []
    for i in b_lines:
        if is_in_range(note['time'], note['time'] + note['duration'], i):
            split_points.append(i)
            is_split = True
    if is_split == False:
        out.append(note)
        return out
    elif is_split == True:
        start = note['time']
        end = note['time'] + note['duration']
        for i in range(0, len(split_points) + 1):
            if i == 0:  # if first iteration
                out.append({'type': 'note',
                            'note': note['note'],
                            'time': start,
                            'duration': split_points[0] - start,
                            'hand': note['hand'],
                            'beam': note['beam'],
                            'slur': note['slur']})
            elif i == len(split_points):  # if last iteration
                out.append({'type': 'split',
                            'note': note['note'],
                            'time': split_points[i - 1],
                            'duration': end - split_points[i - 1],
                            'hand': note['hand'],
                            'beam': note['beam'],
                            'slur': note['slur']})
                return out
            else:  # if not first and not last iteration
                out.append({'type': 'split', 'note': note['note'], 'time': split_points[i - 1],
                            'duration': split_points[i] - split_points[i - 1], 'hand': 0, 'beam': 0, 'slur': 0})


def bbox_offset(bbox, offset):
    x1, y1, x2, y2 = bbox
    return (x1 - offset, y1 - offset, x2 + offset, y2 + offset)


def rndmcolor():
    color = '#'

    for i in range(6):
        color += random.choice('0123456789ABCDEF')

    return color


def staff_height(mn, mx, scale):
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


def new_line_pos(FILE, mp_line):
    '''
    returns a list of the position of every new line of music.
    '''
    bl_pos = barline_ticks(FILE)
    new_lines = []

    count = 0
    for bl in range(len(bl_pos)):
        try:
            new_lines.append(bl_pos[count])
        except IndexError:
            new_lines.append(end_bar_tick(t_sig_map))
            break
        try:
            count += mp_line[bl]
        except IndexError:
            count += mp_line[-1]

    return new_lines


def draw_staff_lines(y, mn, mx, scale):
    '''
    'y' takes the y-position of the uppper line of the staff.
    'mn' and 'mx' take the lowest and highest note in the staff
    so the function can draw the needed lines.
    'scale' prints the staff on a different scale where 1 is
    the default/normal size.
    '''

    def draw3line(y):
        x = MARGIN
        pview.create_line(x, y, x + PRINTEAREA_WIDTH, y, width=2, capstyle='round', fill='black', tag='staff')
        pview.create_line(x, y + (10 * scale), x + PRINTEAREA_WIDTH, y + (10 * scale), width=2, capstyle='round',
                          fill='black', tag='staff')
        pview.create_line(x, y + (20 * scale), x + PRINTEAREA_WIDTH, y + (20 * scale), width=2, capstyle='round',
                          fill='black', tag='staff')

    def draw2line(y):
        x = MARGIN
        pview.create_line(x, y, x + PRINTEAREA_WIDTH, y, width=0.5, capstyle='round', fill='black', tag='staff')
        pview.create_line(x, y + (10 * scale), x + PRINTEAREA_WIDTH, y + (10 * scale), width=0.5, capstyle='round',
                          fill='black', tag='staff')

    def draw_dash2line(y):
        x = MARGIN
        if platform.system() == 'Linux' or platform.system() == 'Darwin':
            pview.create_line(x, y, x + PRINTEAREA_WIDTH, y, width=1, dash=(6, 6), capstyle='round', fill='black',
                              tag='staff')
            pview.create_line(x, y + (10 * scale), x + PRINTEAREA_WIDTH, y + (10 * scale), width=1, dash=(6, 6),
                              capstyle='round', fill='black', tag='staff')
        elif platform.system() == 'Windows':
            pview.create_line(x, y, x + PRINTEAREA_WIDTH, y, width=1, dash=4, capstyle='round', fill='black',
                              tag='staff')
            pview.create_line(x, y + (10 * scale), x + PRINTEAREA_WIDTH, y + (10 * scale), width=1, dash=4,
                              capstyle='round', fill='black', tag='staff')

    keyline = 0

    if mx >= 81:
        draw3line(0 + y)
        draw2line((40 * scale) + y)
        draw3line((70 * scale) + y)
        draw2line((110 * scale) + y)
        draw3line((140 * scale) + y)
        draw2line((180 * scale) + y)
        draw3line((210 * scale) + y)
        keyline = (250 * scale)
    if mx >= 76 and mx <= 80:
        draw2line(0 + y)
        draw3line((30 * scale) + y)
        draw2line((70 * scale) + y)
        draw3line((100 * scale) + y)
        draw2line((140 * scale) + y)
        draw3line((170 * scale) + y)
        keyline = (210 * scale)
    if mx >= 69 and mx <= 75:
        draw3line(0 + y)
        draw2line((40 * scale) + y)
        draw3line((70 * scale) + y)
        draw2line((110 * scale) + y)
        draw3line((140 * scale) + y)
        keyline = 180 * scale
    if mx >= 64 and mx <= 68:
        draw2line(0 + y)
        draw3line((30 * scale) + y)
        draw2line((70 * scale) + y)
        draw3line((100 * scale) + y)
        keyline = 140 * scale
    if mx >= 57 and mx <= 63:
        draw3line(0 + y)
        draw2line((40 * scale) + y)
        draw3line((70 * scale) + y)
        keyline = 110 * scale
    if mx >= 52 and mx <= 56:
        draw2line(0 + y)
        draw3line((30 * scale) + y)
        keyline = 70 * scale
    if mx >= 45 and mx <= 51:
        draw3line(0 + y)
        keyline = 40 * scale

    draw_dash2line(keyline + y)

    if mn >= 33 and mn <= 39:
        draw3line(keyline + (30 * scale) + y)
    if mn >= 28 and mn <= 32:
        draw3line(keyline + (30 * scale) + y)
        draw2line(keyline + (70 * scale) + y)
    if mn >= 21 and mn <= 27:
        draw3line(keyline + (30 * scale) + y)
        draw2line(keyline + (70 * scale) + y)
        draw3line(keyline + (100 * scale) + y)
    if mn >= 16 and mn <= 20:
        draw3line(keyline + (30 * scale) + y)
        draw2line(keyline + (70 * scale) + y)
        draw3line(keyline + (100 * scale) + y)
        draw2line(keyline + (140 * scale) + y)
    if mn >= 9 and mn <= 15:
        draw3line(keyline + (30 * scale) + y)
        draw2line(keyline + (70 * scale) + y)
        draw3line(keyline + (100 * scale) + y)
        draw2line(keyline + (140 * scale) + y)
        draw3line(keyline + (170 * scale) + y)
    if mn >= 4 and mn <= 8:
        draw3line(keyline + (30 * scale) + y)
        draw2line(keyline + (70 * scale) + y)
        draw3line(keyline + (100 * scale) + y)
        draw2line(keyline + (140 * scale) + y)
        draw3line(keyline + (170 * scale) + y)
        draw2line(keyline + (210 * scale) + y)
    if mn >= 1 and mn <= 3:
        draw3line(keyline + (30 * scale) + y)
        draw2line(keyline + (70 * scale) + y)
        draw3line(keyline + (100 * scale) + y)
        draw2line(keyline + (140 * scale) + y)
        draw3line(keyline + (170 * scale) + y)
        draw2line(keyline + (210 * scale) + y)
        editor.create_line(XYMARGIN + MARGIN, (keyline + (240 * scale) + y), XYMARGIN + MARGIN + PRINTEAREA_WIDTH,
                           (keyline + (240 * scale) + y), width=2)


def get_staff_height(line, scale):
    # create linenotelist
    linenotelist = []
    for note in line:
        if note['type'] in ['note', 'split', 'invis']:
            linenotelist.append(note['note'])
    if linenotelist:
        minnote = min(linenotelist)
        maxnote = max(linenotelist)
    else:
        minnote = 40
        maxnote = 44
    return staff_height(minnote, maxnote, scale), minnote, maxnote


def end_bar_tick(t_sig_map):
    '''
    Returns the tick of the end-barline.
    '''
    bln_time = 0
    for i in t_sig_map:
        meas_len = measure_length((i['numerator'], i['denominator']))
        for meas in range(0, i['amount']):
            bln_time += meas_len
    return bln_time


def event_x_pos_pianoroll(pos, start_line_tick, end_line_tick):
    '''
    returns the x position on the paper.
    '''
    factor = interpolation(start_line_tick, end_line_tick, pos)
    return XYMARGIN + MARGIN + (PRINTEAREA_WIDTH * factor)


def event_x_pos_engrave(pos, start_line_tick, end_line_tick):
    '''
    returns the x position on the paper.
    '''
    factor = interpolation(start_line_tick, end_line_tick, pos)
    return MARGIN + (PRINTEAREA_WIDTH * factor)


def t_sig_start_tick(t_sig_map, n):
    out = []
    tick = 0
    for i in t_sig_map:
        out.append(tick)
        tick += measure_length((i['numerator'], i['denominator'])) * i['amount']
    return out[n]


def process_margin(value):
    global MARGIN, PRINTEAREA_WIDTH, PRINTEAREA_HEIGHT
    MARGIN = value
    PRINTEAREA_WIDTH = PAPER_WIDTH - (MARGIN * 2)
    PRINTEAREA_HEIGHT = PAPER_HEIGHT - (MARGIN * 2)


def note_active_grey(x0, x1, y, linenr, new_line):
    '''draws a midi note with a stop sign(vertical line at the end of the midi-note).'''
    x0 = event_x_pos_pianoroll(x0, linenr, new_line)
    x1 = event_x_pos_pianoroll(x1, linenr, new_line)
    editor.create_rectangle(x0, y - 5, x1, y + 5, fill='#e3e3e3', outline='')  # e3e3e3
    editor.create_line(x1, y - 5, x1, y + 5, width=2)
    editor.create_line(x0, y - 5, x0, y + 5, width=2, fill='#e3e3e3')


def note_y_pos(note, mn, mx, cursy, scale):
    '''
    returns the position of the given note relative to 'cursy'(the y axis staff cursor).
    '''

    ylist = [495, 490, 485, 475, 470, 465, 460, 455, 445, 440, 435, 430, 425, 420, 415,
             405, 400, 395, 390, 385, 375, 370, 365, 360, 355, 350, 345, 335, 330, 325, 320, 315,
             305, 300, 295, 290, 285, 280, 275, 265, 260, 255, 250, 245, 235, 230, 225, 220, 215,
             210, 205, 195, 190, 185, 180, 175, 165, 160, 155, 150, 145, 140, 135, 125, 120, 115,
             110, 105, 95, 90, 85, 80, 75, 70, 65, 55, 50, 45, 40, 35, 25, 20, 15, 10, 5, 0, -5, -15]

    sub = 0

    if mx >= 81:
        sub = 0
    if mx >= 76 and mx <= 80:
        sub = 40
    if mx >= 69 and mx <= 75:
        sub = 70
    if mx >= 64 and mx <= 68:
        sub = 110
    if mx >= 57 and mx <= 63:
        sub = 140
    if mx >= 52 and mx <= 56:
        sub = 180
    if mx >= 45 and mx <= 51:
        sub = 210
    if mx <= 44:
        sub = 250

    return cursy + (ylist[note - 1] * scale) - (sub * scale)


def diff(x, y):
    if x >= y:
        return x - y
    else:
        return y - x


def note_active_gradient(x0, x1, y, linenr, scale):
    '''draws a midi note with gradient'''
    width = diff(x0, x1)
    if width == 0:
        width = 1
    (r1, g1, b1) = root.winfo_rgb('white')
    (r2, g2, b2) = root.winfo_rgb(MIDINOTECOLOR)
    r_ratio = float(r2 - r1) / width
    g_ratio = float(g2 - g1) / width
    b_ratio = float(b2 - b1) / width
    for i in range(math.ceil(width)):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
        editor.create_line(x0 + i, y - (5 * scale), x0 + i, y + (5 * scale), fill=color)
    editor.create_line(x1, y - (5 * scale), x1, y + (5 * scale), width=2)
    editor.create_line(x0, y - (5 * scale), x0, y + (5 * scale), width=2, fill='white')


def newpage_linenr(no, lst):
    p_counter = 0
    l_counter = 0
    for page in lst:
        if p_counter == no:
            return l_counter
        p_counter += 1
        for line in page:
            l_counter += 1


def newpage_barnr(no, lst):
    p_counter = 0
    b_counter = 0
    for page in lst:
        if p_counter == no:
            return b_counter
        p_counter += 1
        for line in page:
            for bar in line:
                if bar[0] == 'barline':
                    b_counter += 1


def baseround(x, base=5):
    return base * round(x / base)


def mx2tick(mx, edit_grid, length_of_music, x_scale):
    '''
        This function converts the mouse position to
        (start) time in pianoticks.
    '''
    # defining the tick
    start = XYMARGIN
    end = XYMARGIN + (length_of_music * x_scale)
    tick = baseround(interpolation(start, end, mx) * length_of_music, edit_grid)

    return tick


def my2pitch(my, y_scale):
    '''
        This function converts the mouse position to
        pitch in pianokeynumber 1..88.
    '''
    my -= center_pianoroll + 15

    ylist = [535, 530, 525, 515, 510, 505, 500, 495, 485, 480, 475, 470, 465, 460,
             455, 445, 440, 435, 430, 425, 415, 410, 405, 400, 395, 390, 385, 375, 370, 365,
             360, 355, 345, 340, 335, 330, 325, 320, 315, 305, 300, 295, 290, 285, 275, 270,
             265, 260, 255, 250, 245, 235, 230, 225, 220, 215, 205, 200, 195, 190, 185, 180,
             175, 165, 160, 155, 150, 145, 135, 130, 125, 120, 115, 110, 105, 95, 90, 85, 80,
             75, 65, 60, 55, 50, 45, 40, 35, 25]

    cf = [4, 9, 16, 21, 28, 33, 40, 45, 52, 57, 64, 69, 76, 81, 88]
    be = [3, 8, 15, 20, 27, 32, 39, 44, 51, 56, 63, 68, 75, 80, 87]

    for yl, idx in zip(ylist, range(len(ylist))):
        yl *= y_scale
        if idx + 1 in cf:
            if my >= yl - (2.5 * y_scale) and my < yl + (5 * y_scale):
                return idx + 1
        elif idx + 1 in be:
            if my >= yl - (5 * y_scale) and my < yl + (2.5 * y_scale):
                return idx + 1
        else:
            if my >= yl - (2.5 * y_scale) and my < yl + (2.5 * y_scale):
                return idx + 1

    if my < ylist[-1] * y_scale:
        return 88
    if my > ylist[0] * y_scale:
        return 1


def note_design_rolleditor(note):
    '''
        this function draws a note on the pianoroll editor
        based on a note message. example note:
        {'type': 'note', 'time': 0.0, 'duration': 64.0, 'note': 56, 'hand': 0, 'beam': 0, 'slur': 0}
    '''

    editor.delete(note['id'])

    # coordanates for midinote rectangle and notestart
    x0 = XYMARGIN + (note['time'] * x_scale)
    x1 = XYMARGIN + (((note['time'] + note['duration']) * x_scale))
    y = (note_y_pos(note['note'], 1, 88, XYMARGIN * y_scale, y_scale))
    y0 = y - (5 * y_scale)
    y1 = y + (5 * y_scale)

    # draw midi-note
    editor.create_polygon(x0,
                          y + center_pianoroll,
                          x0 + (5 * y_scale),
                          y0 + center_pianoroll,
                          x1 - (5 * y_scale),
                          y0 + center_pianoroll,
                          x1,
                          y + center_pianoroll,
                          x1 - (5 * y_scale),
                          y1 + center_pianoroll,
                          x0 + (5 * y_scale),
                          y1 + center_pianoroll,
                          fill=MIDINOTECOLOR,
                          tag=(note['id'], 'midinote'),
                          width=20 * x_scale)
    editor.create_line(x1,
                       y0 + center_pianoroll,
                       x1,
                       y1 + center_pianoroll,
                       fill='black',
                       width=2,
                       tag=(note['id'], 'midinote'))

    # draw stem
    if note['hand'] == 'l':
        editor.create_line(x0,
                           y + center_pianoroll,
                           x0,
                           y + (20 * y_scale) + center_pianoroll,
                           width=2,
                           tag=(note['id'], 'stem'),
                           fill='black')
    else:
        editor.create_line(x0,
                           y + center_pianoroll,
                           x0,
                           y - (20 * y_scale) + center_pianoroll,
                           width=2,
                           tag=(note['id'], 'stem'),
                           fill='black')

    # draw note-head
    if note['note'] in BLACK:
        editor.create_oval(x0,
                           y0 + center_pianoroll,
                           x0 + (7.5 * y_scale),
                           y1 + center_pianoroll,
                           outline='black',
                           fill='black',
                           width=2,
                           tag=(note['id'], 'notehead', 'black'))
        if note['hand'] == 'l':
            editor.create_oval(x0 + (2.5 * y_scale),
                               y0 + (3.5 * y_scale) + center_pianoroll,
                               x0 + (5.5 * y_scale),
                               y1 - (3.5 * y_scale) + center_pianoroll,
                               outline='',
                               fill='white',
                               tag=(note['id'], 'notehead', 'black'),
                               width=2)
    else:
        editor.create_oval(x0,
                           y0 + center_pianoroll,
                           x0 + (10 * y_scale),
                           y1 + center_pianoroll,
                           outline='black',
                           fill='white',
                           width=2,
                           tag=(note['id'], 'notehead'))
        if note['hand'] == 'l':
            editor.create_oval(x0 + (3.5 * y_scale),
                               y0 + (3.5 * y_scale) + center_pianoroll,
                               x0 + (6.5 * y_scale),
                               y1 - (3.5 * y_scale) + center_pianoroll,
                               outline='',
                               fill='black',
                               tag=(note['id'], 'notehead'))

    for bl in barline_ticks(FILE):

        # draw tie-dot if a note crosses a barline
        if bl > note['time'] and bl < note['time'] + note['duration'] and diff(bl, note['time'] + note['duration']) > 1:
            editor.create_oval(XYMARGIN + (bl * x_scale) + (5 * x_scale),
                               y0 + (2.5 * y_scale) + center_pianoroll,
                               XYMARGIN + (bl * x_scale) + (15 * x_scale),
                               y1 - (2.5 * y_scale) + center_pianoroll,
                               fill='black',
                               tag=(note['id'], 'tiedot'),
                               outline='')

        if diff(bl, note['time']) < 1:

            # draw white space if on barline
            if note['hand'] == 'r':

                editor.create_line(x0,
                                   y - (25 * y_scale) + center_pianoroll,
                                   x0,
                                   y + (10 * y_scale) + center_pianoroll,
                                   fill='white',
                                   tag=(note['id'], 'whitespace'),
                                   width=2)
            else:
                editor.create_line(x0,
                                   y - (10 * y_scale) + center_pianoroll,
                                   x0,
                                   y + (25 * y_scale) + center_pianoroll,
                                   fill='white',
                                   tag=(note['id'], 'whitespace'),
                                   width=2)

    for msg in FILE[1]:

        # connect stems if two notes are starting on the same time
        if msg['type'] == 'note':
            if msg['time'] == note['time'] and msg['note'] != note['note'] and msg['hand'] == note['hand']:
                stem_y = (note_y_pos(msg['note'], 1, 88, XYMARGIN * y_scale, y_scale))
                editor.create_line(x0,
                                   stem_y + center_pianoroll,
                                   x0,
                                   y + center_pianoroll,
                                   width=2,
                                   capstyle='round',
                                   tag=(note['id'], 'connect_stem'),
                                   fill='black')


def update_drawing_order_pianoroll():
    editor.tag_raise('midinote')
    editor.tag_raise('staff')
    editor.tag_raise('barnumbering')
    editor.tag_raise('leftdot')
    editor.tag_raise('tiedot')
    editor.tag_raise('whitespace')
    editor.tag_raise('notehead')
    editor.tag_raise('black')
    editor.tag_raise('stem')
    editor.tag_raise('connect_stem')
    editor.tag_raise('textbg')
    editor.tag_raise('text')
    editor.tag_raise('countline')
    editor.tag_raise('pedal')


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


def text_design_rolleditor(txt):
    # coordanates
    x = XYMARGIN + (txt['time'] * x_scale)
    y = (note_y_pos(txt['note'], 1, 88, XYMARGIN * y_scale, y_scale))
    y0 = y - (5 * y_scale)
    y1 = y + (5 * y_scale)

    t = editor.create_text(x,
                           y + center_pianoroll,
                           font=('', 12, 'normal'),
                           tag=(txt['id'], 'text'),
                           text=txt['text'],
                           anchor='w',
                           fill='black')
    round_rectangle(editor, editor.bbox(t)[0],
                    editor.bbox(t)[1],
                    editor.bbox(t)[2],
                    editor.bbox(t)[3],
                    fill='white',
                    outline=MIDINOTECOLOR,
                    width=.5,
                    tag=(txt['id'], 'textbg'))


def count_design_rolleditor(count):
    # coordanates
    x = XYMARGIN + (count['time'] * x_scale)
    y1 = (note_y_pos(count['note1'], 1, 88, XYMARGIN * y_scale, y_scale))
    y2 = (note_y_pos(count['note2'], 1, 88, XYMARGIN * y_scale, y_scale))

    editor.create_line(x,
                       y1 + center_pianoroll,
                       x,
                       y2 + center_pianoroll,
                       dash=(2, 2),
                       width=1,
                       tag=(count['id'], 'countline'),
                       fill='black')
    editor.create_rectangle(x - 2.5,
                            y1 + center_pianoroll - 2.5,
                            x + 2.5,
                            y1 + center_pianoroll + 2.5,
                            fill='grey',
                            outline='black',
                            tag=(count['id'], 'countline'))


def pedal_design_rolleditor(pedal):
    
    # coordanates
    x = XYMARGIN + (pedal['time'] * x_scale)
    y = (note_y_pos(pedal['note'], 1, 88, XYMARGIN * y_scale, y_scale)) + center_pianoroll

    if pedal['updown'] == 'd':
        editor.create_line(x,
                        y,
                        x,
                        y + 20,
                        width=2,
                        tag=(pedal['id'], 'pedal'),
                        fill='black',
                        arrow='last')
    else:
        editor.create_line(x,
                        y,
                        x,
                        y + 20,
                        width=2,
                        tag=(pedal['id'], 'pedal'),
                        fill='black',
                        arrow='first')

















# ---------------------
# save FILE structure
# ---------------------
'''
File structure:
A *.pnoscript FILE consists of a python list which contains
two parts(in nested lists):
* score setup; 
    * time signatures
    * page layout(like margins, measures each line etc)
    * titles(like title, composer etc)
    * cursor
* musical data; 
    * notes
    * text; to describe the music/how to play the sequense
'''

FILE = [
    # score setup part:
    [
        # t_sig_map; inside list because the order of the t_sig messages defines the time changes/score.
        [
            {'type': 'time_signature', 'amount': 16, 'numerator': 4, 'denominator': 4, 'grid': 4, 'visible': 1},
            # {'type':'time_signature','amount':4, 'numerator':6, 'denominator':8, 'grid':2, 'visible':1},
        ],

        # mp_line
        {'type': 'mp_line', 'string': '5'},

        # titles
        {'type': 'title', 'text': 'Test_Version'},
        {'type': 'composer', 'text': 'PianoScript'},
        {'type': 'copyright', 'text': 'copyrights reserved 2022'},

        # scale; global scale
        {'type': 'scale', 'value': .85},

        # page margins
        {'type': 'margin', 'value': 50},

        # space under systems / in between
        {'type': 'system_space', 'value': '60'}
    ],

    # musical data part:
    [
        # notes
        {'type': 'note', 'time': 0.0, 'duration': 2048.0, 'note': 55, 'hand': 0, 'beam': 0, 'slur': 0}

        # text
        # {'type':'text', 'time':0, 'text':'play', 'bold':0, 'italic':1, 'underline':0},

        # slur
        # {'type':'slur', 'time':0, 'duration':2048, 'interpolx':.5, 'y':20, 'hand':0}
    ]
]



















# ------------------
# FILE management
# ------------------
file_changed = 0


def new_file():
    if file_changed == 1:
        save_quest()

    global FILE
    FILE = [
        # score setup part/settings:
        [
            # t_sig_map; inside list because the order of the t_sig messages defines the time changes/score.
            [
                {'type': 'time_signature', 'amount': 8, 'numerator': 4, 'denominator': 4, 'grid': 4, 'visible': 1},
            ],

            # mp_line
            {'type': 'mp_line', 'string': '4'},

            # titles
            {'type': 'title', 'text': 'Untitled'},
            {'type': 'composer', 'text': 'PianoScript'},
            {'type': 'copyright', 'text': 'copyrights reserved 2022'},

            # scale; global scale
            {'type': 'scale', 'value': .85},

            # page margins; bottom,top,left,right together
            {'type': 'margin', 'value': 50},

            # space under systems / in between
            {'type': 'system_space', 'value': '60'},
        ],

        # musical data part:
        [
            # time and duration are in piano-ticks; note 1..88 == pianokey; hand 0=left, 1=right
            #{'type': 'pedal', 'time': 0.0, 'note': 44, 'updown':'d'}
        ]
    ]
    threading.Thread(target=run_pianroll).start()
    do_engrave('')

    # update all textboxes from FILE
    update_textboxes()


def open_file():
    print('open_file')
    f = filedialog.askopenfile(parent=root, mode='Ur', title='Open', filetypes=[("PianoScript files", "*.pnoscript")],
                               initialdir='~/Desktop/')
    # f = 'moonlight.pnoscript'
    # if f:
    #     mpline_entry.delete(0,'end')
    #     title_entry.delete(0,'end')
    #     composer_entry.delete(0,'end')
    #     copyright_entry.delete(0,'end')
    #     filepath = f
    #     root.title('PnoScript - %s' % f)
    #     f = open(f, 'r', newline=None)
    #     global FILE
    #     FILE = ast.literal_eval(f.read())
    #     f.close()
    #     threading.Thread(target=run_pianroll).start()
    if f:
        filepath = f.name
        root.title('PnoScript - %s' % f.name)
        f = open(f.name, 'r', newline=None)
        global FILE
        FILE = ast.literal_eval(f.read())
        f.close()
        threading.Thread(target=run_pianroll).start()
        do_engrave('')
    return


def save_file():
    save_as()


def save_as():
    f = filedialog.asksaveasfile(parent=root, mode='w', filetypes=[("PianoScript files", "*.pnoscript")],
                                 initialdir='~/Desktop/')
    if f:
        root.title('PnoScript - %s' % f.name)
        f = open(f.name, 'w')
        f.write(str(FILE))
        f.close()
        return


def save_quest():
    if messagebox.askyesno('Wish to save?', 'Do you wish to save the current FILE?'):
        save_file()
    else:
        return


def quit_editor(event='dummy'):
    # close thread
    global program_is_running
    with thread_auto_render.condition:
        program_is_running = False
        thread_auto_render.condition.notify()
    thread_auto_render.join()

    # close program
    root.destroy()
















# --------------
# piano-roll
# --------------

needs_to_render = True
program_is_running = True

x_scale = .4
y_scale = 1

# piano-roll editor
length_of_music = 0
new_id = 0
edit_grid = 128
note_start_times = []
center_pianoroll = 0
input_mode = StringVar()
click_y = None

# mouse edit
btn1_click = False
btn2_click = False
btn3_click = False
shift_key = False
ctl_key = False
alt_key = False
holdid = ''

# keyboard edit
writing_note = False
cursor_time = 0
cursor_note = 40
selection = {'time1': 0, 'note1': 40, 'time2': 0, 'note2': 40}


def run_pianroll(event='event'):
    global length_of_music, FILE, y_scale, x_scale, center_pianoroll

    # remove all objects from the canvas.
    editor.delete('all')

    # calc y_scale
    root.update()
    y_scale = editor.winfo_height() / (FULLSTAFFHEIGHT + (XYMARGIN * 2))
    if y_scale > 1.5:
        y_scale = 1.5
    center_pianoroll = (editor.winfo_height() - (
                (FULLSTAFFHEIGHT + (XYMARGIN * 2) + hbar.winfo_height()) * y_scale)) / 2
    x_scale = y_scale * .3

    # DRAW GRID AND BARLINES
    length_staff = 0
    gx = 0
    bl_count = 1
    gridtext = ''
    for ts, idx_ts in zip(FILE[0][0], range(len(FILE[0][0]))):
        numerator = ts['numerator']
        denominator = ts['denominator']
        amount = ts['amount']
        grid = ts['grid']
        visible = ts['visible']

        # add text to grid editor
        gridtext += f'{numerator}/{denominator} {amount} {grid} {visible}\n'

        l = measure_length((numerator, denominator)) * x_scale
        length_of_music += measure_length((numerator, denominator)) * amount

        # draw grid
        grid_dist = l / grid
        for grid1 in range(amount):

            length_staff += l

            tc = ''
            if grid1 == 0 and visible >= 1:
                tc = f'(t-sig:{numerator}/{denominator})'

            # draw barline and barnumbering
            editor.create_line(XYMARGIN + gx,
                               XYMARGIN * y_scale + center_pianoroll,
                               XYMARGIN + gx,
                               (XYMARGIN + FULLSTAFFHEIGHT) * y_scale + center_pianoroll,
                               width=2,
                               fill='black',
                               tag='staff')
            editor.create_text(XYMARGIN + gx,
                               (XYMARGIN - 15) * y_scale + center_pianoroll,
                               text=str(bl_count),
                               anchor='sw',
                               font=('courier', round(12 * y_scale), "bold"),
                               tag='barnumbering')
            editor.create_text(XYMARGIN + gx,
                               (XYMARGIN + FULLSTAFFHEIGHT + 30) * y_scale + center_pianoroll,
                               text=tc,
                               anchor='sw',
                               font=('courier', round(12 * y_scale), "bold"),
                               tag='barnumbering')

            for grid2 in range(grid):
                # draw gridline
                editor.create_line(XYMARGIN + gx + (grid_dist * grid2),
                                   XYMARGIN * y_scale + center_pianoroll,
                                   XYMARGIN + gx + (grid_dist * grid2),
                                   (XYMARGIN + FULLSTAFFHEIGHT) * y_scale + center_pianoroll,
                                   dash=(6, 6),
                                   fill='black',
                                   tag='staff')

            gx += l
            bl_count += 1

        # draw endline
        if idx_ts + 1 == len(FILE[0][0]):
            editor.create_line(XYMARGIN + length_staff,
                               XYMARGIN * y_scale + center_pianoroll,
                               XYMARGIN + length_staff,
                               (XYMARGIN + FULLSTAFFHEIGHT) * y_scale + center_pianoroll,
                               fill='black',
                               width=4,
                               tag='staff')

    # DRAW STAFF
    y_axis = 0
    for staff in range(7):
        editor.create_line(XYMARGIN,
                           (XYMARGIN + y_axis) * y_scale + center_pianoroll,
                           XYMARGIN + length_staff,
                           (XYMARGIN + y_axis) * y_scale + center_pianoroll,
                           fill='black',
                           width=2,
                           tag='staff')
        editor.create_line(XYMARGIN,
                           (XYMARGIN + y_axis + 10) * y_scale + center_pianoroll,
                           XYMARGIN + length_staff,
                           (XYMARGIN + y_axis + 10) * y_scale + center_pianoroll,
                           fill='black',
                           width=2,
                           tag='staff')
        editor.create_line(XYMARGIN,
                           (XYMARGIN + y_axis + 20) * y_scale + center_pianoroll,
                           XYMARGIN + length_staff,
                           (XYMARGIN + y_axis + 20) * y_scale + center_pianoroll,
                           fill='black',
                           width=2,
                           tag='staff')
        if staff == 3:
            editor.create_line(XYMARGIN,
                               (XYMARGIN + y_axis + 40) * y_scale + center_pianoroll,
                               XYMARGIN + length_staff,
                               (XYMARGIN + y_axis + 40) * y_scale + center_pianoroll,
                               fill='black',
                               width=1,
                               tag='staff',
                               dash=(6, 6))
            editor.create_line(XYMARGIN,
                               (XYMARGIN + y_axis + 50) * y_scale + center_pianoroll,
                               XYMARGIN + length_staff,
                               (XYMARGIN + y_axis + 50) * y_scale + center_pianoroll,
                               fill='black',
                               width=1,
                               tag='staff',
                               dash=(6, 6))
        else:
            editor.create_line(XYMARGIN,
                               (XYMARGIN + y_axis + 40) * y_scale + center_pianoroll,
                               XYMARGIN + length_staff,
                               (XYMARGIN + y_axis + 40) * y_scale + center_pianoroll,
                               fill='black',
                               width=1,
                               tag='staff')
            editor.create_line(XYMARGIN,
                               (XYMARGIN + y_axis + 50) * y_scale + center_pianoroll,
                               XYMARGIN + length_staff,
                               (XYMARGIN + y_axis + 50) * y_scale + center_pianoroll,
                               fill='black',
                               width=1,
                               tag='staff')
        y_axis += 70
    editor.create_line(XYMARGIN,
                       (XYMARGIN + y_axis) * y_scale + center_pianoroll,
                       XYMARGIN + length_staff,
                       (XYMARGIN + y_axis) * y_scale + center_pianoroll,
                       fill='black',
                       width=2,
                       tag='staff')

    sh = staff_height(1, 88, 1)
    global new_id
    new_id = 0
    for note in FILE[1]:

        # DRAW NOTES
        if note['type'] == 'note':

            note['id'] = 'note%i' % new_id
            if note['note'] > 88:
                note['note'] = 88
            if note['note'] < 1:
                note['note'] = 1
            note_design_rolleditor(note)
            new_id += 1

        # DRAW TEXT
        if note['type'] == 'text':
            note['id'] = 'text%i' % new_id
            text_design_rolleditor(note)
            new_id += 1

        # DRAW COUNT_LINES
        if note['type'] == 'count_line':
            note['id'] = 'count%i' % new_id
            count_design_rolleditor(note)
            new_id += 1

        if note['type'] == 'pedal':
            note['id'] = 'count%i' % new_id
            pedal_design_rolleditor(note)
            new_id += 1

    update_drawing_order_pianoroll()

    # update bbox
    _, _, bbox3, bbox4 = editor.bbox('all')
    editor.configure(scrollregion=(0, 0, bbox3 + XYMARGIN, bbox4 + XYMARGIN))

    # update textboxes from FILE
    update_textboxes()
















def mouse_handling(event, event_type):
    '''
        event = event
        event_type = 'btn1click', 'btn1release', 'motion'...
    '''
    global btn1_click, btn2_click, btn3_click, holdid
    global new_id, cursor_note, cursor_time, click_y

    mx = editor.canvasx(event.x)
    my = editor.canvasy(event.y)

    ###### mouse handling for input_mode 'note' ###########

    if input_mode.get() == 'note':

        if event_type == 'btn1click':

            btn1_click = True
            taglst = editor.gettags(editor.find_withtag('current'))

            # detecting if we are editing or adding
            editoradd = 'edit'
            if not taglst:
                editoradd = 'add'
            else:
                if not 'note' in taglst[0] or 'stem' in taglst:
                    editoradd = 'add'

            if editoradd == 'add':

                new_id += 1

                note = {'type': 'note',
                        'time': mx2tick(mx, edit_grid, length_of_music, x_scale),
                        'duration': edit_grid,
                        'note': my2pitch(my, y_scale),
                        'hand': 'l',
                        'beam': 0,
                        'slur': 0,
                        'id': 'note%i' % new_id}

                FILE[1].append(note)

                holdid = note['id']

                note_design_rolleditor(note)

            # we are editing
            else:

                holdid = taglst[0]

                # delete the note drawing
                editor.delete(holdid)

                # edit note in FILE and redraw note
                for note in FILE[1]:

                    if note['type'] == 'note':

                        if note['id'] == holdid:

                            duration_time = mx2tick(mx, edit_grid, length_of_music, x_scale) - note['time']
                            if duration_time < edit_grid:
                                duration_time = edit_grid
                            note['duration'] = duration_time
                            note['note'] = my2pitch(my, y_scale)
                            note['hand'] = 'l'

                            note_design_rolleditor(note)


        elif event_type == 'btn1release':

            btn1_click = False
            holdid = ''
            do_engrave('')


        elif event_type == 'double-btn1':

            ...

        if event_type == 'btn3click':

            btn3_click = True
            taglst = editor.gettags(editor.find_withtag('current'))

            # detecting if we are editing or adding
            editoradd = 'edit'
            if not taglst:
                editoradd = 'add'
            else:
                if not 'note' in taglst[0] or 'stem' in taglst:
                    editoradd = 'add'

            if editoradd == 'add':

                new_id += 1

                note = {'type': 'note',
                        'time': mx2tick(mx, edit_grid, length_of_music, x_scale),
                        'duration': edit_grid,
                        'note': my2pitch(my, y_scale),
                        'hand': 'r',
                        'beam': 0,
                        'slur': 0,
                        'id': 'note%i' % new_id}

                FILE[1].append(note)

                holdid = note['id']

                note_design_rolleditor(note)

            # we are editing
            else:

                holdid = taglst[0]

                # delete the note drawing
                editor.delete(holdid)

                # edit note in FILE and redraw note
                for note in FILE[1]:

                    if note['type'] == 'note':

                        if note['id'] == holdid:

                            duration_time = mx2tick(mx, edit_grid, length_of_music, x_scale) - note['time']
                            if duration_time < edit_grid:
                                duration_time = edit_grid
                            note['duration'] = duration_time
                            note['note'] = my2pitch(my, y_scale)
                            note['hand'] = 'r'

                            note_design_rolleditor(note)


        elif event_type == 'btn3release':

            btn3_click = False
            holdid = ''
            do_engrave('')

        elif event_type == 'btn2click':

            find_selected = editor.gettags(editor.find_withtag('current'))
            if find_selected:
                holdid = find_selected[0]
            else:
                holdid = ''

            if 'note' in holdid:

                # delete the note drawing
                editor.delete(holdid)

                # delete the note from FILE
                for note in FILE[1]:

                    if note['type'] == 'note':

                        if note['id'] == holdid:
                            FILE[1].remove(note)
                            break

        elif event_type == 'btn2release':

            btn2_click = False
            holdid = None

            do_engrave('')

        elif event_type == 'motion':  # movement of mouse

            if btn1_click and holdid or btn3_click and holdid:

                if 'note' in holdid:

                    # delete the note drawing
                    editor.delete(holdid)

                    # edit note in FILE and redraw note
                    for note in FILE[1]:

                        if note['type'] == 'note':

                            if note['id'] == holdid:

                                duration_time = mx2tick(mx, edit_grid, length_of_music, x_scale) - note['time']
                                if duration_time < edit_grid:
                                    duration_time = edit_grid
                                note['duration'] = duration_time
                                note['note'] = my2pitch(my, y_scale)

                                note_design_rolleditor(note)

    ########## TEXT EDIT MOUSE HANDLING ##########

    if input_mode.get() == 'text':

        if event_type == 'btn1click':

            btn1_click = True
            taglst = editor.gettags(editor.find_withtag('current'))

            # if we are not clicking on text, add text to FILE.
            if not 'text' in taglst:

                new_id += 1

                txt = {'type': 'text',
                       'time': mx2tick(mx, edit_grid, length_of_music, x_scale),
                       'note': my2pitch(my, y_scale),
                       'id': 'text%i' % new_id,
                       'text': simpledialog.askstring('Add text', 'Please enter the new text here:'),
                       'xoffset': 0,
                       'yoffset': 0}

                FILE[1].append(txt)

                holdid = txt['id']

                text_design_rolleditor(txt)

            # we are editing
            else:
                try:
                    holdid = taglst[0]
                except IndexError:
                    ...

                # delete the text drawing
                editor.delete(holdid)

                # edit text in FILE and redraw note
                for txt in FILE[1]:

                    if txt['type'] == 'text':

                        if txt['id'] == holdid:
                            txt['time'] = mx2tick(mx, edit_grid, length_of_music, x_scale)
                            txt['note'] = my2pitch(my, y_scale)

                            text_design_rolleditor(txt)


        elif event_type == 'btn1release':

            btn1_click = False
            holdid = None
            do_engrave('')


        elif event_type == 'btn2click':

            btn2_click = True
            taglst = editor.gettags(editor.find_withtag('current'))

            if 'text' in taglst:

                holdid = taglst[0]

                # delete the text drawing
                editor.delete(holdid)

                # remove text in FILE
                for txt in FILE[1]:

                    if txt['type'] == 'text' and txt['id'] == holdid:
                        FILE[1].remove(txt)




        elif event_type == 'btn2release':

            btn2_click = False
            holdid = None
            do_engrave('')

        elif event_type == 'btn3click':

            btn3_click = True
            taglst = editor.gettags(editor.find_withtag('current'))

            if 'text' in taglst:

                holdid = taglst[0]

                # delete the old text drawing
                editor.delete(holdid)

                # edit text in FILE and redraw note
                for txt in FILE[1]:

                    if txt['type'] == 'text' and txt['id'] == holdid:
                        txt['text'] = simpledialog.askstring('Edit text', 'Please edit your text here',
                                                             initialvalue=txt['text'])

                        text_design_rolleditor(txt)

                        do_engrave('')

        elif event_type == 'btn3release':

            btn3_click = False
            holdid = None



        elif event_type == 'motion':  # movement of mouse

            if btn1_click and holdid:

                if 'text' in holdid:

                    # delete the old text drawing
                    editor.delete(holdid)

                    # edit note in FILE and redraw note
                    for txt in FILE[1]:

                        if txt['type'] == 'text':

                            if txt['id'] == holdid:
                                txt['time'] = mx2tick(mx, edit_grid, length_of_music, x_scale)
                                txt['note'] = my2pitch(my, y_scale)

                                text_design_rolleditor(txt)

    ###### mouse handling for input_mode 'left/right' ###########

    if input_mode.get() == 'l/r':

        if event_type == 'btn1click':

            btn1_click = True
            taglst = editor.gettags(editor.find_withtag('current'))

            # if we are clicking on a note
            if taglst:
                if 'note' in taglst[0] and not 'stem' in taglst:

                    holdid = taglst[0]

                    # delete the old note drawing
                    editor.delete(holdid)

                    # edit note in FILE and redraw note
                    for note in FILE[1]:

                        if note['type'] == 'note':

                            if note['id'] == holdid:
                                note['hand'] = 'l'

                    for note in FILE[1]:

                        if note['type'] == 'note':

                            if note['id'] == holdid:

                                # redraw all notes which are on the same start position
                                for evt in FILE[1]:

                                    if evt['type'] == 'note':

                                        if evt['time'] == note['time']:
                                            note_design_rolleditor(evt)

                                # note_design_rolleditor(note)


        elif event_type == 'btn1release':

            btn1_click = False
            holdid = None
            do_engrave('')

        if event_type == 'btn3click':

            btn3_click = True
            taglst = editor.gettags(editor.find_withtag('current'))

            # if we are clicking on a note
            if taglst:
                if 'note' in taglst[0] and not 'stem' in taglst:

                    holdid = taglst[0]

                    # delete the old note drawing
                    editor.delete(holdid)

                    # edit note in FILE and redraw note
                    for note in FILE[1]:

                        if note['type'] == 'note':

                            if note['id'] == holdid:

                                note['hand'] = 'r'

                                # redraw all notes which are on the same start position
                                for evt in FILE[1]:

                                    if evt['type'] == 'note':

                                        if evt['time'] == note['time']:
                                            note_design_rolleditor(evt)


        elif event_type == 'btn3release':

            btn3_click = False
            holdid = ''
            do_engrave('')

    ########## COUNT EDIT MOUSE HANDLING ##########

    if input_mode.get() == 'countline':

        if event_type == 'btn1click':

            btn1_click = True
            taglst = editor.gettags(editor.find_withtag('current'))

            # if we are not clicking on countline, add countline to FILE.
            if not 'countline' in taglst:

                new_id += 1
                click_y = my
                count = {'type': 'count_line',
                         'time': mx2tick(mx, edit_grid, length_of_music, x_scale),
                         'note1': my2pitch(my, y_scale),
                         'note2': my2pitch(my, y_scale),
                         'id': 'count%i' % new_id}

                FILE[1].append(count)

                holdid = count['id']

                count_design_rolleditor(count)

            # we are editing
            else:

                holdid = taglst[0]

                # delete the count drawing
                editor.delete(holdid)

                # edit count in FILE and redraw note
                for cnt in FILE[1]:

                    if cnt['type'] == 'count_line':

                        if cnt['id'] == holdid:
                            cnt['note2'] = my2pitch(my, y_scale)
                            count_design_rolleditor(cnt)


        elif event_type == 'btn1release':

            btn1_click = False
            holdid = None
            do_engrave('')


        elif event_type == 'btn2click':

            btn2_click = True
            taglst = editor.gettags(editor.find_withtag('current'))

            if 'countline' in taglst:

                holdid = taglst[0]

                # delete the text drawing
                editor.delete(holdid)

                # remove text in FILE
                for cnt in FILE[1]:

                    if cnt['type'] == 'count_line' and cnt['id'] == holdid:
                        FILE[1].remove(cnt)




        elif event_type == 'btn2release':

            btn2_click = False
            holdid = None
            do_engrave('')

        elif event_type == 'btn3click':

            btn3_click = True
            taglst = editor.gettags(editor.find_withtag('current'))

            if 'countline' in taglst:
                holdid = taglst[0]

        elif event_type == 'btn3release':

            btn3_click = False
            holdid = None



        elif event_type == 'motion':  # movement of mouse

            if btn1_click and holdid:

                if 'count' in holdid:

                    # edit note in FILE and redraw note
                    for cnt in FILE[1]:

                        if cnt['type'] == 'count_line':

                            if cnt['id'] == holdid:
                                # delete the old text drawing
                                editor.delete(holdid)
                                print('!')
                                cnt['note2'] = my2pitch(my, y_scale)
                                count_design_rolleditor(cnt)

            if btn3_click and holdid:

                if 'count' in holdid:

                    # edit note in FILE and redraw note
                    for cnt in FILE[1]:

                        if cnt['type'] == 'count_line':

                            if cnt['id'] == holdid:
                                # delete the old text drawing
                                editor.delete(holdid)
                                cnt['note1'] = my2pitch(my, y_scale)
                                cnt['time'] = mx2tick(mx, edit_grid, length_of_music, x_scale)
                                count_design_rolleditor(cnt)

    ###### mouse handling for input_mode 'pedal' ###########

    if input_mode.get() == 'pedal':

        if event_type == 'btn1click':

            btn1_click = True
            taglst = editor.gettags(editor.find_withtag('current'))

            # detecting if we are editing or adding
            editoradd = 'edit'
            if not taglst:
                editoradd = 'add'
            else:
                if not 'note' in taglst[0] or 'stem' in taglst:
                    editoradd = 'add'

            if editoradd == 'add':

                new_id += 1

                pedal = {'type': 'pedal',
                        'time': mx2tick(mx, edit_grid, length_of_music, x_scale),
                        'note': my2pitch(my, y_scale),
                        'updown': 'd',
                        'id': 'pedal%i' % new_id}

                FILE[1].append(pedal)

                holdid = pedal['id']

                pedal_design_rolleditor(pedal)

            # we are editing
            else:

                holdid = taglst[0]

                # delete the note drawing
                editor.delete(holdid)

                # edit note in FILE and redraw note
                for note in FILE[1]:

                    if note['type'] == 'note':

                        if note['id'] == holdid:

                            duration_time = mx2tick(mx, edit_grid, length_of_music, x_scale) - note['time']
                            if duration_time < edit_grid:
                                duration_time = edit_grid
                            note['duration'] = duration_time
                            note['note'] = my2pitch(my, y_scale)
                            note['hand'] = 'l'

                            note_design_rolleditor(note)


        elif event_type == 'btn1release':

            btn1_click = False
            holdid = ''
            do_engrave('')


        elif event_type == 'double-btn1':

            ...

        if event_type == 'btn3click':

            btn3_click = True
            taglst = editor.gettags(editor.find_withtag('current'))

            # detecting if we are editing or adding
            editoradd = 'edit'
            if not taglst:
                editoradd = 'add'
            else:
                if not 'note' in taglst[0] or 'stem' in taglst:
                    editoradd = 'add'

            if editoradd == 'add':

                new_id += 1

                note = {'type': 'note',
                        'time': mx2tick(mx, edit_grid, length_of_music, x_scale),
                        'duration': edit_grid,
                        'note': my2pitch(my, y_scale),
                        'hand': 'r',
                        'beam': 0,
                        'slur': 0,
                        'id': 'note%i' % new_id}

                FILE[1].append(note)

                holdid = note['id']

                note_design_rolleditor(note)

            # we are editing
            else:

                holdid = taglst[0]

                # delete the note drawing
                editor.delete(holdid)

                # edit note in FILE and redraw note
                for note in FILE[1]:

                    if note['type'] == 'note':

                        if note['id'] == holdid:

                            duration_time = mx2tick(mx, edit_grid, length_of_music, x_scale) - note['time']
                            if duration_time < edit_grid:
                                duration_time = edit_grid
                            note['duration'] = duration_time
                            note['note'] = my2pitch(my, y_scale)
                            note['hand'] = 'r'

                            note_design_rolleditor(note)


        elif event_type == 'btn3release':

            btn3_click = False
            holdid = ''
            do_engrave('')

        elif event_type == 'btn2click':

            find_selected = editor.gettags(editor.find_withtag('current'))
            if find_selected:
                holdid = find_selected[0]
            else:
                holdid = ''

            if 'note' in holdid:

                # delete the note drawing
                editor.delete(holdid)

                # delete the note from FILE
                for note in FILE[1]:

                    if note['type'] == 'note':

                        if note['id'] == holdid:
                            FILE[1].remove(note)
                            break

        elif event_type == 'btn2release':

            btn2_click = False
            holdid = None

            do_engrave('')

        elif event_type == 'motion':  # movement of mouse

            if btn1_click and holdid or btn3_click and holdid:

                if 'note' in holdid:

                    # delete the note drawing
                    editor.delete(holdid)

                    # edit note in FILE and redraw note
                    for note in FILE[1]:

                        if note['type'] == 'note':

                            if note['id'] == holdid:

                                duration_time = mx2tick(mx, edit_grid, length_of_music, x_scale) - note['time']
                                if duration_time < edit_grid:
                                    duration_time = edit_grid
                                note['duration'] = duration_time
                                note['note'] = my2pitch(my, y_scale)

                                note_design_rolleditor(note)

    update_drawing_order_pianoroll()

def keyboard_handling(event):
    ...
















#--------------
# textboxes
#--------------
def grid_selector(event='event'):
    global edit_grid
    value = ''

    for i in list_dur.curselection():
        value = list_dur.get(i)

    lengthdict = {1: 1024, 2: 512, 4: 256, 8: 128, 16: 64, 32: 32, 64: 16, 128: 8}
    edit_grid = ((lengthdict[eval(value)] / eval(divide_spin.get())) * eval(times_spin.get()))

    root.focus()


def process_grid_editor(event='event'):
    global FILE

    t = gridedit_text.get('1.0', 'end').split('\n')
    ignore = False

    FILE[0][0] = []

    for ts in t:

        numerator = None
        denominator = None
        amount = None
        grid_div = None
        visible = None

        if ts:
            try:
                numerator = eval(ts.split()[0].split('/')[0])
                denominator = eval(ts.split()[0].split('/')[1])
                amount = eval(ts.split()[1])
                grid_div = eval(ts.split()[2])
                visible = eval(ts.split()[3])
            except IndexError:
                print(
                    'Please read the documentation about how to provide the grid mapping correctly.\na correct gridmap:\n4/4 16 4 1')
                messagebox.showinfo(title="Can't export PDF!",
                                    message='Please read the documentation about how to provide the grid mapping correctly.\na correct gridmap:\n4/4 16 4 1')
                ignore = True

                break
        else:
            continue

        if ignore == True:
            return

        # gridmap add to FILE
        FILE[0][0].append(
            {'type': 'time_signature', 'amount': amount, 'numerator': numerator, 'denominator': denominator,
             'grid': grid_div, 'visible': visible})

    run_pianroll()
    do_engrave('')


def process_margin_editor():
    m = systemspace_text.get('1.0', 'end')[:-1]

    # write to FILE
    global FILE
    for i in FILE[0][1:]:
        if i['type'] == 'system_space':
            i['value'] = m

    # update textbox
    systemspace_text.delete('1.0','end')
    systemspace_text.insert('1.0', m)

    # re-render
    do_engrave('')


def process_division_editor():
    m = measureseachline_text.get('1.0', 'end')[:-1]

    # write to FILE
    global FILE
    for i in FILE[0][1:]:
        if i['type'] == 'mp_line':
            i['string'] = m

    # update textbox
    measureseachline_text.delete('1.0','end')
    measureseachline_text.insert('1.0', m)

    # re-render
    do_engrave('')


def update_textboxes():
    '''
        This function updates the gui textboxes from FILE
    '''

    # time-sig
    txt = ''
    for ts,idx in zip(FILE[0][0],range(len(FILE[0][0]))):

        numerator = ts['numerator']
        denominator = ts['denominator']
        amount = ts['amount']
        grid_div = ts['grid']
        visible = ts['visible']

        if not idx == len(FILE[0][0])-1:
            txt += str(numerator) + '/' + str(denominator) + ' ' + str(amount) + ' ' + str(grid_div) + ' ' + str(visible) + '\n'
        else:
            txt += str(numerator) + '/' + str(denominator) + ' ' + str(amount) + ' ' + str(grid_div) + ' ' + str(visible)
    gridedit_text.delete('1.0','end')
    gridedit_text.insert('1.0', txt)

    # margin editor
    for marg in FILE[0][1:]:

        if marg['type'] == 'margin':

            systemspace_text.delete('1.0','end')
            systemspace_text.insert('1.0', marg['value'])

    # measures each line
    for meas in FILE[0][1:]:

        if meas['type'] == 'mp_line':

            measureseachline_text.delete('1.0','end')
            measureseachline_text.insert('1.0', meas['string'])




















def midi_import():
    global FILE
    FILE = [
        # score setup part:
        [
            # t_sig_map; inside list because the order of the t_sig messages defines the time changes/score.
            [

            ],

            # mp_line
            {'type': 'mp_line', 'string': '4'},

            # titles
            {'type': 'title', 'text': 'Test_Version'},
            {'type': 'composer', 'text': 'PianoScript'},
            {'type': 'copyright', 'text': 'copyrights reserved 2022'},

            # scale; global scale
            {'type': 'scale', 'value': 1},

            # page margins
            {'type': 'margin', 'value': 40},

            # space under systems / in between
            {'type': 'system_space', 'value': '40'}
        ],

        # musical data part:
        [

        ]
    ]

    # ---------------------------------------------
    # translate midi data to note messages with
    # the right start and stop (piano)ticks.
    # ---------------------------------------------
    midifile = filedialog.askopenfile(parent=root,
                                      mode='Ur',
                                      title='Open midi (experimental)...',
                                      filetypes=[("MIDI files", "*.mid")]).name
    mesgs = []
    mid = MidiFile(midifile)
    tpb = mid.ticks_per_beat
    msperbeat = 1
    for i in mid:
        mesgs.append(i.dict())
    ''' convert time to pianotick '''
    for i in mesgs:
        i['time'] = tpb * (1 / msperbeat) * 1000000 * i['time'] * (256 / tpb)
        if i['type'] == 'set_tempo':
            msperbeat = i['tempo']
    ''' change time values from delta to relative time. '''
    memory = 0
    for i in mesgs:
        i['time'] += memory
        memory = i['time']
        # change every note_on with 0 velocity to note_off.
        if i['type'] == 'note_on' and i['velocity'] == 0:
            i['type'] = 'note_off'
    ''' get note_on, note_off, time_signature durations. '''
    index = 0
    for i in mesgs:
        if i['type'] == 'note_on':
            for n in mesgs[index:]:
                if n['type'] == 'note_off' and i['note'] == n['note']:
                    i['duration'] = n['time'] - i['time']
                    break

        if i['type'] == 'time_signature':
            for t in mesgs[index + 1:]:
                if t['type'] == 'time_signature' or t['type'] == 'end_of_track':
                    i['duration'] = t['time'] - i['time']
                    break
        index += 1

    # write time_signatures:
    count = 0
    for i in mesgs:
        if i['type'] == 'time_signature':
            tsig = (i['numerator'], i['denominator'])
            amount = int(round(i['duration'] / measure_length(tsig), 0))
            gridno = i['numerator']
            if tsig == '6/8':
                gridno = 2
            if tsig == '12/8':
                gridno = 4
            FILE[0][0].append(
                {'type': i['type'], 'amount': amount, 'numerator': i['numerator'], 'denominator': i['denominator'],
                 'grid': gridno, 'visible': 1})
            count += 1

    # write notes
    for i in mesgs:
        if i['type'] == 'note_on' and i['channel'] == 0:
            FILE[1].append(
                {'type': 'note', 'time': i['time'], 'duration': i['duration'], 'note': i['note'] - 20, 'hand': 'r',
                 'beam': 0, 'slur': 0})
        if i['type'] == 'note_on' and i['channel'] >= 1:
            FILE[1].append(
                {'type': 'note', 'time': i['time'], 'duration': i['duration'], 'note': i['note'] - 20, 'hand': 'l',
                 'beam': 0, 'slur': 0})

    threading.Thread(target=run_pianroll).start()
    do_engrave('')

















# ------------------
# export
# ------------------
def exportPDF():
    def is_tool(name):
        """Check whether `name` is on PATH and marked as executable."""
        return which(name) is not None
        print('exportPDF')

    if platform.system() == 'Linux':
        if is_tool('ps2pdfwr') == 0:
            messagebox.showinfo(title="Can't export PDF!",
                                message='PianoScript cannot export the PDF because function "ps2pdfwr" is not '
                                        'installed on your computer.')
            return

        f = filedialog.asksaveasfile(mode='w', parent=root, filetypes=[("pdf file", "*.pdf")], initialfile=title,
                                     initialdir='~/Desktop')
        if f:
            pslist = []
            for rend in range(engrave('export')):
                pview.postscript(file=f"/tmp/tmp{rend}.ps", 
                    x=10000, 
                    y=rend * PAPER_HEIGHT, 
                    width=PAPER_WIDTH,
                    height=PAPER_HEIGHT, 
                    rotate=False,
                    fontmap='-*-Courier-Bold-R-Normal--*-120-*')
                process = subprocess.Popen(
                    ["ps2pdfwr", "-sPAPERSIZE=a4", "-dFIXEDMEDIA", "-dEPSFitPage", "/tmp/tmp%s.ps" % rend,
                     "/tmp/tmp%s.pdf" % rend])
                process.wait()
                os.remove("/tmp/tmp%s.ps" % rend)
                pslist.append("/tmp/tmp%s.pdf" % rend)
            cmd = 'pdfunite '
            for i in range(len(pslist)):
                cmd += pslist[i] + ' '
            cmd += '"%s"' % f.name
            process = subprocess.Popen(cmd, shell=True)
            process.wait()
            return
        else:
            return

    elif platform.system() == 'Windows':
        f = filedialog.asksaveasfile(mode='w', parent=root, filetypes=[("pdf FILE", "*.pdf")], initialfile=title,
                                     initialdir='~/Desktop')
        if f:
            print(f.name)
            counter = 0
            pslist = []
            for export in range(engrave('export')):
                counter += 1
                print('printing page ', counter)
                pview.postscript(file=f"{f.name}{counter}.ps", 
                    colormode='gray', 
                    x=10000, 
                    y=export * PAPER_HEIGHT,
                    width=PAPER_WIDTH, 
                    height=PAPER_HEIGHT, 
                    rotate=False,
                    fontmap='-*-Courier-Bold-R-Normal--*-120-*')
                pslist.append(str('"' + str(f.name) + str(counter) + '.ps' + '"'))
            try:
                run_pianroll = subprocess.Popen(
                    f'''"{windowsgsexe}" -dQUIET -dBATCH -dNOPAUSE -dFIXEDMEDIA -sPAPERSIZE=a4 -dEPSFitPage -sDEVICE=pdfwrite -sOutputFile="{f.name}.pdf" {' '.join(pslist)}''',
                    shell=True)
                run_pianroll.wait()
                run_pianroll.terminate()
                for i in pslist:
                    os.remove(i.strip('"'))
                f.close()
                os.remove(f.name)
            except:
                messagebox.showinfo(title="Can't export PDF!",
                                    message='Be sure you have selected a valid path in the default.pnoscript FILE. You have to set the path+gswin64c.exe. example: ~windowsgsexe{C:/Program Files/gs/gs9.54.0/bin/gswin64c.exe}')















def set_xscale(event='event'):
    global x_scale

    value = simpledialog.askfloat('Set editor x-scale',
                                  'x-scale is how big the x direction is zoomed. 0.4 = default; 0.8 = twice the default.')

    if value:
        x_scale = value

    run_pianroll()


def exportPostscript():

    f = filedialog.asksaveasfile(mode='w', 
        parent=root, 
        filetypes=[("postscript file", "*.ps")], 
        initialfile=title,
        initialdir='~/Desktop')

    if f:
        for export in range(engrave('export')):
            print('printing page ', export)
            pview.postscript(file=f"{f.name}{export}.ps", 
                colormode='gray', 
                x=10000, 
                y=export * PAPER_HEIGHT,
                width=PAPER_WIDTH, 
                height=PAPER_HEIGHT, 
                rotate=False,
                fontmap='-*-Courier-Bold-R-Normal--*-120-*')

















# --------------
# engraving
# --------------
t_sig_map = []
mp_line = []
msg = []
page_space = []
new_line = []
title = ''
composer = ''
copyright = ''
system_space = []
header_space = 50
scale = .75
paper_color = 0
view_page = 0


def engrave(render_type=''):
    # check if there is a time_signature in the FILE.
    if not FILE[0][0]:
        print('ERROR: There is no time signature in the FILE!')
        return

    def read():
        '''
        This function reads the FILE and translates it
        to a msg list; list containing nested lists:
        [pages[lines[notes]lines]pages]
        and it writes all settings to the right variables.
        '''
        # init utils lists and variables.
        global t_sig_map, mp_line, msg, title, composer, copyright
        global system_space, new_line, page_space, scale
        t_sig_map = []
        mp_line = []
        msg = []
        page_space = []
        title = ''
        composer = ''
        copyright = ''
        system_space = []

        # score setup part:
        # time_signature
        bln_time = 0
        grd_time = 0
        count = 0
        for i in FILE[0][0]:
            if i['type'] == 'time_signature':
                t_sig_map.append(i)
                # barline and grid messages
                meas_len = measure_length((i['numerator'], i['denominator']))
                grid_len = meas_len / i['grid']
                for meas in range(0, i['amount']):
                    msg.append({'type': 'barline', 'time': bln_time})
                    for grid in range(0, i['grid']):
                        msg.append({'type': 'grid-line', 'time': grd_time})
                        grd_time += grid_len
                    bln_time += meas_len
                if i['visible'] == 1:
                    msg.append({'type': 'time_signature_text', 'time': t_sig_start_tick(t_sig_map, count),
                                'duration': meas_len, 'text': str(i['numerator']) + '/' + str(i['denominator'])})
                count += 1

            # mp_line
        for i in FILE[0][1:]:
            if i['type'] == 'mp_line':
                try:
                    mpline = i['string'].split()
                    for mp in mpline:
                        mp_line.append(eval(mp))
                except:
                    print('ERROR: mp_line string is not valid! mp_line is set to default value 4.')
                    mp_line.append(4)

            # titles
            if i['type'] == 'title':
                title = i['text']
            if i['type'] == 'composer':
                composer = i['text']
            if i['type'] == 'copyright':
                copyright = i['text']

            # scale
            if i['type'] == 'scale':
                scale = i['value']

            # margin
            if i['type'] == 'margin':
                MARGIN = i['value']
                process_margin(MARGIN)

            # system_spacing
            if i['type'] == 'system_space':

                system_space = i['value'].split()
                try:
                    for val in system_space:
                        val = int(val)
                except:
                    print('Error in system space. Provide a list of numbers.')
                
                if not system_space:
                    print('Error; empty system_space. Default value "60px" will be used')
                    system_space = ['60']

        # musical data part:
        for i in FILE[1]:
            # note
            if i['type'] == 'note':
                for note in note_split_processor(i):
                    msg.append(
                        {'type': note['type'], 'time': note['time'], 'duration': note['duration'], 'note': note['note'],
                         'hand': note['hand'], 'beam': note['beam']})

            # invisible note
            if i['type'] == 'invis':
                msg.append(
                    {'type': note['type'], 'time': note['time'], 'duration': note['duration'], 'note': note['note']})

            # text
            if i['type'] == 'text':
                msg.append({'type': i['type'], 'time': i['time'], 'note': i['note'], 'text': i['text']})

            # count_line
            if i['type'] == 'count_line':
                msg.append({'type': i['type'], 'time': i['time'], 'note1': i['note1'], 'note2': i['note2']})

            # endline
            msg.append({'type': 'endline', 'time': end_bar_tick(t_sig_map)})

        # placing the events in lists of lines.
        new_line = new_line_pos(FILE, mp_line)
        msgs = msg
        msg = []
        count = 0
        for ln in new_line[:-1]:
            hlplst = []
            for evt in msgs:
                if evt['time'] >= new_line[count] - 0.1 and evt['time'] < new_line[count + 1] - 0.1:
                    hlplst.append(evt)
            msg.append(hlplst)
            count += 1
        # remove 
        for i in msg:
            if not i:
                msg.remove(i)

        # placing the lines in lists of pages.
        lineheight = []
        for line in msg:

            notelst = []
            for note in line:
                if note['type'] in ['note', 'split', 'invis']:
                    notelst.append(note['note'])
                else:
                    pass
            try:
                lineheight.append(staff_height(min(notelst), max(notelst), scale))
            except ValueError:
                lineheight.append(10 * scale)

        msgs = msg
        msg = []
        curs_y = header_space
        pagelist = []
        resspace = 0
        header = header_space
        for line, height, idx in zip(msgs, lineheight, range(len(msgs))):
            try:
                ss = system_space[idx]
            except IndexError:
                ss = system_space[-1]
            curs_y += height + int(ss)  # fix later
            if idx == len(lineheight) - 1:  # if this is the last iteration
                if curs_y <= PRINTEAREA_HEIGHT - header:
                    pagelist.append(line)
                    msg.append(pagelist)
                    resspace = PRINTEAREA_HEIGHT - curs_y
                    page_space.append(resspace)
                    break
                elif curs_y > PRINTEAREA_HEIGHT - header:
                    msg.append(pagelist)
                    pagelist = []
                    pagelist.append(line)
                    msg.append(pagelist)
                    page_space.append(resspace)
                    curs_y = 0
                    resspace = PRINTEAREA_HEIGHT - curs_y
                    page_space.append(resspace)
                    break
                else:
                    pass
            else:
                if curs_y <= PRINTEAREA_HEIGHT - header:  # does fit on paper
                    pagelist.append(line)
                    resspace = PRINTEAREA_HEIGHT - curs_y
                elif curs_y > PRINTEAREA_HEIGHT - header:  # does not fit on paper
                    msg.append(pagelist)
                    pagelist = []
                    pagelist.append(line)
                    curs_y = 0
                    curs_y += height + int(system_space[0])
                    page_space.append(resspace)
                    header = 0
                else:
                    pass

        # for page in msg:
        #     print('newpage:')
        #     for line in page:
        #         print('newline:')
        #         for note in line:
        #             print(note)

    read()

    def draw():

        curs_y = 0

        l_counter = 0
        b_counter = 1

        b_ticks = barline_ticks(FILE)

        if not render_type == 'export':
            pview.create_line(0,
                              curs_y,
                              PAPER_WIDTH,
                              curs_y,
                              fill='black',
                              dash=(6, 6),
                              tag='endpaper')

        # PAGE in message list
        for page, idx_page in zip(msg, range(len(msg))):

            # draw paper
            pview.create_rectangle(0,
                                   curs_y,
                                   PAPER_WIDTH,
                                   curs_y + PAPER_HEIGHT,
                                   fill='white',
                                   outline='')

            if not render_type == 'export':
                pview.create_line(0,
                                  PAPER_HEIGHT + curs_y,
                                  PAPER_WIDTH,
                                  PAPER_HEIGHT + curs_y,
                                  fill='black',
                                  dash=(6, 6),
                                  tag='endpaper')

            # copyrights / footer
            pview.create_text(MARGIN,
                              PAPER_HEIGHT - MARGIN + curs_y,
                              text='page %s of %s | %s | %s' % (idx_page + 1, len(msg), title, copyright),
                              anchor='nw',
                              font=('courier', round(12 * scale), "normal"),
                              tag='titles',
                              fill='black')

            curs_y += MARGIN

            if idx_page == 0:
                # create title and composer text
                pview.create_text(MARGIN,
                                  curs_y,
                                  text=title,
                                  font=('courier', round(18 * scale), "normal"),
                                  anchor='nw',
                                  fill='black')
                pview.create_text(MARGIN + PRINTEAREA_WIDTH,
                                  curs_y,
                                  text=composer,
                                  font=('courier', round(12 * scale), "normal"),
                                  anchor='ne',
                                  fill='black')

                curs_y += header_space

            # LINE of music
            for line, idx_line in zip(page, range(len(page))):

                staffheight, minnote, maxnote = get_staff_height(line, scale)

                # update curs_y
                try:
                    sys_space = system_space[l_counter]
                except IndexError:
                    sys_space = system_space[-1]
                if len(msg) - 1 == idx_page:
                    curs_y += (eval(sys_space) / 2)
                else:
                    curs_y += ((eval(sys_space) / 2) + (page_space[idx_page] / (len(msg[idx_page]))) / 2)

                # draw end-of-line barline
                pview.create_line(MARGIN + PRINTEAREA_WIDTH,
                                  curs_y,
                                  MARGIN + PRINTEAREA_WIDTH,
                                  curs_y + staffheight,
                                  width=2 * scale,
                                  capstyle='round',
                                  tag='grid',
                                  fill='black')

                # draw endbarline
                if len(msg) - 1 == idx_page and len(page) - 1 == idx_line:
                    pview.create_line(MARGIN + PRINTEAREA_WIDTH,
                                      curs_y,
                                      MARGIN + PRINTEAREA_WIDTH,
                                      curs_y + staffheight,
                                      width=4 * scale,
                                      capstyle='round',
                                      tag='grid',
                                      fill='black')

                # MSGS in lines
                for evt, idx_evt in zip(line, range(len(line))):

                    # barline and numbering
                    if evt['type'] == 'barline':
                        x = event_x_pos_engrave(evt['time'], new_line[l_counter], new_line[l_counter + 1])
                        pview.create_line(x,
                                          curs_y,
                                          x,
                                          curs_y + staffheight,
                                          width=2 * scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill='black')
                        pview.create_text(x,
                                          curs_y,
                                          text=b_counter,  # fix later TODO
                                          tag='grid',
                                          fill='black',
                                          font=('courier', round(12 * scale), "normal"),
                                          anchor='sw')
                        b_counter += 1

                    # grid
                    if evt['type'] == 'grid-line':
                        x = event_x_pos_engrave(evt['time'], new_line[l_counter], new_line[l_counter + 1])
                        pview.create_line(x,
                                          curs_y,
                                          x,
                                          curs_y + staffheight,
                                          width=1 * scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill='black',
                                          dash=(6, 6))

                    # staff
                    draw_staff_lines(curs_y, minnote, maxnote, scale)

                    # note start
                    if evt['type'] == 'note':

                        # define dimensions
                        x0 = event_x_pos_engrave(evt['time'], new_line[l_counter], new_line[l_counter + 1])
                        x1 = event_x_pos_engrave(evt['time'] + evt['duration'], new_line[l_counter],
                                                 new_line[l_counter + 1])
                        y = note_y_pos(evt['note'], minnote, maxnote, curs_y, scale)
                        y0 = y - (5 * scale)
                        y1 = y + (5 * scale)

                        # midinote
                        pview.create_polygon(x0,
                                             y,
                                             x0 + (5 * scale),
                                             y - (5 * scale),
                                             x1 - (5 * scale),
                                             y - (5 * scale),
                                             x1,
                                             y,
                                             x1 - (5 * scale),
                                             y + (5 * scale),
                                             x0 + (5 * scale),
                                             y + (5 * scale),
                                             fill=MIDINOTECOLOR,
                                             tag='midi_note',
                                             width=20 * x_scale)
                        pview.create_line(x1,
                                          y - (5 * scale),
                                          x1, y + (5 * scale),
                                          width=2 * scale,
                                          fill='black',
                                          tag=('midi_note','notestop'))

                        # left hand
                        if evt['hand'] == 'l':

                            # left stem and white space if on barline
                            pview.create_line(x0,
                                              y,
                                              x0,
                                              y + (25 * scale),
                                              width=2 * scale,
                                              tag='stem',
                                              fill='black')
                            for bl in b_ticks:

                                if diff(evt['time'], bl) < 1:
                                    pview.create_line(x0,
                                                      y - (10 * scale),
                                                      x0,
                                                      y + (30 * scale),
                                                      width=2 * scale,
                                                      tag='white_space',
                                                      fill='white')
                            # notehead
                            if evt['note'] in BLACK:

                                pview.create_oval(x0,
                                                  y0,
                                                  x0 + (5 * scale),
                                                  y1,
                                                  tag='black_notestart',
                                                  fill='black',
                                                  outline='black',
                                                  width=2 * scale)
                                # left dot black
                                pview.create_oval(x0 + (1.5 * scale),
                                                  y + (1 * scale),
                                                  x0 + (3.5 * scale),
                                                  y - (1 * scale),
                                                  tag='left_dot',
                                                  fill='white',
                                                  outline='')
                            else:
                                pview.create_oval(x0,
                                                  y0,
                                                  x0 + (10 * scale),
                                                  y1,
                                                  tag='white_notestart',
                                                  fill='white',
                                                  outline='black',
                                                  width=2 * scale)
                                # left dot white
                                pview.create_oval(x0 + (((10 / 2) - 1) * scale),
                                                  y + (1 * scale),
                                                  x0 + (((10 / 2) + 1) * scale),
                                                  y - (1 * scale),
                                                  tag='left_dot',
                                                  fill='black',
                                                  outline='')

                        # right hand
                        else:
                            # right stem and white space if on barline
                            pview.create_line(x0,
                                              y,
                                              x0,
                                              y - (25 * scale),
                                              width=2 * scale,
                                              tag='stem',
                                              fill='black')
                            for bl in b_ticks:

                                if diff(evt['time'], bl) < 1:
                                    pview.create_line(x0,
                                                      y - (30 * scale),
                                                      x0,
                                                      y + (10 * scale),
                                                      width=2 * scale,
                                                      tag='white_space',
                                                      fill='white')
                            # notehead
                            if evt['note'] in BLACK:

                                pview.create_oval(x0,
                                                  y0,
                                                  x0 + (5 * scale),
                                                  y1,
                                                  tag='black_notestart',
                                                  fill='black',
                                                  outline='black',
                                                  width=2 * scale)
                            else:
                                pview.create_oval(x0,
                                                  y0,
                                                  x0 + (10 * scale),
                                                  y1,
                                                  tag='white_notestart',
                                                  fill='white',
                                                  outline='black',
                                                  width=2 * scale)

                        # connect stems

                        for stem in line:

                            if stem['time'] == evt['time'] and stem['type'] == 'note' and stem['note'] != evt['note']:
                                if stem['time'] == evt['time'] and stem['hand'] == evt['hand']:
                                    stem_y = note_y_pos(stem['note'], minnote, maxnote, curs_y, scale)
                                    pview.create_line(x0,
                                                      stem_y,
                                                      x0,
                                                      y,
                                                      width=2 * scale,
                                                      capstyle='round',
                                                      tag='connect_stem',
                                                      fill='black')

                        # experimental note-attachements
                        if evt['beam'] == 1:
                            pview.create_line(x0,
                                              y + (25 * scale),
                                              x0 + (5 * scale),
                                              y + (27.5 * scale))

                    # note active
                    if evt['type'] in ['note', 'split']:
                        x0 = event_x_pos_engrave(evt['time'], new_line[l_counter], new_line[l_counter + 1])
                        x1 = event_x_pos_engrave(evt['time'] + evt['duration'], new_line[l_counter],
                                                 new_line[l_counter + 1])
                        y = note_y_pos(evt['note'], minnote, maxnote, curs_y, scale)
                        pview.create_polygon(x0,
                                             y,
                                             x0 + (5 * scale),
                                             y - (5 * scale),
                                             x1 - (5 * scale),
                                             y - (5 * scale),
                                             x1,
                                             y,
                                             x1 - (5 * scale),
                                             y + (5 * scale),
                                             x0 + (5 * scale),
                                             y + (5 * scale),
                                             fill=MIDINOTECOLOR,
                                             tag='midi_note',
                                             width=20 * x_scale)
                        pview.create_line(x1,
                                          y - (5 * scale),
                                          x1, y + (5 * scale),
                                          width=2 * scale,
                                          fill='black',
                                          tag='midi_note')
                    # if evt['type'] == 'split':
                    #     x0 = event_x_pos_engrave(evt['time'], new_line[l_counter], new_line[l_counter + 1])
                    #     x1 = event_x_pos_engrave(evt['time'] + evt['duration'], new_line[l_counter],
                    #                              new_line[l_counter + 1])
                    #     y = note_y_pos(evt['note'], minnote, maxnote, curs_y, scale)
                    #     pview.create_oval(x0 + (5 * scale),
                    #                       y - (2.5 * scale),
                    #                       x0 + (10 * scale),
                    #                       y + (2.5 * scale),
                    #                       fill='black',
                    #                       outline='',
                    #                       tag='tie_dot')

                    # time-signature-text
                    if evt['type'] == 'time_signature_text':
                        x = event_x_pos_engrave(evt['time'], new_line[l_counter], new_line[l_counter + 1])
                        pview.create_text(x + (2.5 * scale),
                                          curs_y + staffheight + (20 * scale),
                                          text=evt['text'],
                                          tag='tsigtext',
                                          anchor='w',
                                          font=('courier', round(12 * scale), 'underline'),
                                          fill='black')

                    # text
                    if evt['type'] == 'text':
                        x = event_x_pos_engrave(evt['time'], new_line[l_counter], new_line[l_counter + 1])
                        y = note_y_pos(evt['note'], minnote, maxnote, curs_y, scale)
                        t = pview.create_text(x,
                                              y,
                                              text=evt['text'],
                                              tag='text',
                                              anchor='w',
                                              font=('', round(12 * scale), 'normal'),
                                              fill='black')
                        round_rectangle(pview, pview.bbox(t)[0],
                                        pview.bbox(t)[1],  # +(3*scale),
                                        pview.bbox(t)[2],
                                        pview.bbox(t)[3],
                                        fill='white',
                                        outline='',
                                        width=.5,
                                        tag='textbg')

                    # count_line
                    if evt['type'] == 'count_line':
                        x = event_x_pos_engrave(evt['time'], new_line[l_counter], new_line[l_counter + 1])
                        y1 = note_y_pos(evt['note1'], minnote, maxnote, curs_y, scale)
                        y2 = note_y_pos(evt['note2'], minnote, maxnote, curs_y, scale)

                        pview.create_line(x,
                                          y1,
                                          x,
                                          y2,
                                          dash=(2, 2),
                                          tag='countline',
                                          fill='black')

                    # pedal


                # update curs_y
                try:
                    sys_space = system_space[l_counter]
                except IndexError:
                    sys_space = system_space[-1]
                if len(msg) - 1 == idx_page:
                    curs_y += staffheight + (eval(sys_space) / 2)
                else:
                    curs_y += (staffheight + (eval(sys_space) / 2) + (page_space[idx_page] / (len(msg[idx_page]))) / 2)

                l_counter += 1

            # update curs_y
            curs_y = PAPER_HEIGHT * (idx_page + 1)

        if not render_type == 'export':
            root.update()
            s = pview.winfo_width()
            s = s / PAPER_WIDTH
            pview.scale("all", 0, 0, s, s)

        # drawing order
        pview.tag_raise('paper')
        pview.tag_raise('midi_note')
        pview.tag_raise('staff')
        pview.tag_raise('grid')
        pview.tag_raise('white_space')
        pview.tag_raise('stem')
        pview.tag_raise('notestop')
        pview.tag_raise('white_notestart')
        pview.tag_raise('black_notestart')
        pview.tag_raise('connect_stem')
        pview.tag_raise('titles')
        pview.tag_raise('cursor')
        pview.tag_raise('endpaper')
        pview.tag_raise('left_dot')
        pview.tag_raise('tie_dot')
        pview.tag_raise('textbg')
        pview.tag_raise('text')
        pview.tag_raise('countline')
        

        # make the new render update fluently
        pview.move('all', 10000, 0)
        pview.delete('old')
        pview.configure(scrollregion=pview.bbox("all"))
        pview.addtag_all('old')

    draw()

    return len(msg)

















def do_engrave(event):
    with thread_auto_render.condition:
        thread_auto_render.needs_to_render = True
        thread_auto_render.condition.notify()


class QuitThread(Exception):
    pass


class ThreadAutoRender(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.needs_to_render = False
        self.condition = threading.Condition()

    def run(self):
        try:
            while True:
                self.wait_and_render()
        except QuitThread:
            pass

    def wait_and_render(self):
        with self.condition:
            if not program_is_running:
                raise QuitThread
            while not self.needs_to_render:
                self.condition.wait()
                if not program_is_running:
                    raise QuitThread
            self.needs_to_render = False
        try:
            engrave()
        except Exception:  # as e:
            traceback.print_exc()


thread_auto_render = ThreadAutoRender()
thread_auto_render.start()
















def set_titles(t):
    for i in FILE[0]:
        if isinstance(i, dict):
            if i['type'] == t:
                i['text'] = simpledialog.askstring('Set %s' % t, '')

    do_engrave('')


def set_global_scale():
    for i in FILE[0]:
        if isinstance(i, dict):
            if i['type'] == 'scale':
                i['value'] = simpledialog.askfloat('Set global scale',
                                                   'The global scale scales the drawing.\n 1=default, 2=twice as big.')

    do_engrave('')


def set_page_margins():
    for i in FILE[0]:
        if isinstance(i, dict):
            if i['type'] == 'margin':
                i['value'] = simpledialog.askfloat('Set page margins',
                                                   'Set the surrounding page margins; all four sides in one value.')

    do_engrave('')


















# --------------------------------------------------------
# MENU
# --------------------------------------------------------
menubar = Menu(root, relief='flat', bg=color1, fg='white', font=('courier', 12))
root.config(menu=menubar)

fileMenu = Menu(menubar, tearoff=0, bg=color1, fg='white')

fileMenu.add_command(label='new', command=new_file)
fileMenu.add_command(label='open', command=open_file)
fileMenu.add_command(label='import MIDI', command=midi_import)
fileMenu.add_command(label='save', command=None)
fileMenu.add_command(label='save as', command=save_as)

fileMenu.add_separator()

submenu = Menu(fileMenu, tearoff=0, bg=color1, fg='white')
submenu.add_command(label="postscript", command=exportPostscript)
submenu.add_command(label="pdf", command=exportPDF, underline=None)
fileMenu.add_cascade(label='export', menu=submenu, underline=None)

fileMenu.add_separator()

fileMenu.add_command(label="horizontal/vertical", underline=None, command=None)
fileMenu.add_command(label="fullscreen/windowed (F11)", underline=None, command=None)

fileMenu.add_separator()

fileMenu.add_command(label="exit", underline=None, command=None)
menubar.add_cascade(label="Menu", underline=None, menu=fileMenu)

setMenu = Menu(menubar, tearoff=1, bg=color1, fg='white')
setMenu.add_command(label='title', command=lambda: set_titles('title'))
setMenu.add_command(label='composer', command=lambda: set_titles('composer'))
setMenu.add_command(label='copyright', command=lambda: set_titles('copyright'))
setMenu.add_separator()
setMenu.add_command(label='global scale', command=set_global_scale)
setMenu.add_command(label='page margins', command=set_page_margins)
menubar.add_cascade(label="Set", underline=None, menu=setMenu)

modeMenu = Menu(menubar, tearoff=1, bg=color1, fg='white')
modeMenu.add_radiobutton(label="note", variable=input_mode, value='note')
modeMenu.add_radiobutton(label="left/right", variable=input_mode, value='l/r')
modeMenu.add_radiobutton(label="text", variable=input_mode, value='text')
modeMenu.add_radiobutton(label="count-line", variable=input_mode, value='countline')
modeMenu.add_radiobutton(label="pedal", variable=input_mode, value='pedal')
modeMenu.add_separator()
modeMenu.add_radiobutton(label="repeat", variable=input_mode, value='repeat')
modeMenu.add_radiobutton(label="section", variable=input_mode, value='section')
input_mode.set('note')
menubar.add_cascade(label="Elements", underline=None, menu=modeMenu)















# --------------------------------------------------------
# BIND (shortcuts)
# --------------------------------------------------------
root.bind('<Escape>', quit_editor)
editor.bind('<Motion>', lambda event: mouse_handling(event, 'motion'))
if platform.system() == 'Linux' or platform.system() == 'Windows':    
    editor.bind('<Button-1>', lambda event: mouse_handling(event, 'btn1click'))
    editor.bind('<ButtonRelease-1>', lambda event: mouse_handling(event, 'btn1release'))
    editor.bind('<Double-Button-1>', lambda event: mouse_handling(event, 'double-btn1'))
    editor.bind('<Button-2>', lambda event: mouse_handling(event, 'btn2click'))
    editor.bind('<ButtonRelease-2>', lambda event: mouse_handling(event, 'btn2release'))
    editor.bind('<Button-3>', lambda event: mouse_handling(event, 'btn3click'))
    editor.bind('<ButtonRelease-3>', lambda event: mouse_handling(event, 'btn3release'))
if platform.system() == 'Darwin':
    editor.bind('<Button-1>', lambda event: mouse_handling(event, 'btn1click'))
    editor.bind('<ButtonRelease-1>', lambda event: mouse_handling(event, 'btn1release'))
    editor.bind('<Double-Button-1>', lambda event: mouse_handling(event, 'double-btn1'))
    editor.bind('<Button-3>', lambda event: mouse_handling(event, 'btn2click'))
    editor.bind('<ButtonRelease-3>', lambda event: mouse_handling(event, 'btn2release'))
    editor.bind('<Button-2>', lambda event: mouse_handling(event, 'btn3click'))
    editor.bind('<ButtonRelease-2>', lambda event: mouse_handling(event, 'btn3release'))

# SCROLL
# linux scroll
if platform.system() == 'Linux':
    editor.bind("<5>", lambda event: editor.xview('scroll', 1, 'units'))
    editor.bind("<4>", lambda event: editor.xview('scroll', -1, 'units'))
    pview.bind("<5>", lambda event: pview.yview('scroll', 1, 'units'))
    pview.bind("<4>", lambda event: pview.yview('scroll', -1, 'units'))
# windows scroll
if platform.system() == 'Windows':
    editor.bind("<MouseWheel>", lambda event: editor.xview('scroll', -round(event.delta / 120), 'units'))
    pview.bind("<MouseWheel>", lambda event: pview.yview('scroll', -round(event.delta / 120), 'units'))
# mac scroll
if platform.system() == 'Darwin':
    print('!')
    editor.bind("<MouseWheel>", lambda event: editor.xview_scroll(-1 * event.delta, 'units'))

list_dur.bind('<ButtonRelease-1>', grid_selector)
divide_spin.configure(command=lambda: grid_selector())
times_spin.configure(command=lambda: grid_selector())
times_spin.bind('<Return>', lambda event: grid_selector(event))
midpanel.bind('<ButtonRelease-1>', lambda event: threading.Thread(target=run_pianroll()).start())
midpanel.bind('<ButtonRelease-1>', lambda event: do_engrave(event))
root.bind('<Key>', keyboard_handling)
applygrid_button.configure(command=process_grid_editor)
help_button1.configure(command=lambda: messagebox.showinfo('Grid map editor help', HELP1))
help_button2.configure(command=lambda: messagebox.showinfo('Grid map editor help', HELP2))
applyspace_button.configure(command=process_margin_editor)
applymeasures_button.configure(command=process_division_editor)     











if __name__ == '__main__':
    new_file()

# --------------------------------------------------------
# MAINLOOP
# --------------------------------------------------------
root.mainloop()

# --------------------------------------------------------
# TODO
# --------------------------------------------------------
'''
* ...
'''
