#--------------------
# IMPORTS
#--------------------
from tkinter import Tk,Canvas,Menu,Scrollbar,messagebox,PanedWindow,Listbox
from tkinter import filedialog,Frame,Button,Entry,Label,Spinbox
from tkinter import simpledialog
import time,ast,platform,subprocess,os,sys,errno,math
from mido import MidiFile
from shutil import which
import tkinter.ttk as ttk

#--------------------
# GUI
#--------------------
_bg = '#333333' #d9d9d9
# root
root = Tk()
root.title('PianoScript')
ttk.Style(root).theme_use("alt")
scrwidth = root.winfo_screenwidth()
scrheight = root.winfo_screenheight()
root.geometry("%sx%s+%s+0" % (int(scrwidth/2), int(scrheight), int(scrwidth/2)))
# PanedWindow
orient = 'h'
# master
panedmaster = PanedWindow(root, orient='v', sashwidth=20, relief='flat', bg=_bg, sashcursor='arrow')
panedmaster.place(relwidth=1, relheight=1)
uppanel = PanedWindow(panedmaster, height=10000, relief='flat', bg=_bg)
panedmaster.add(uppanel)
downpanel = PanedWindow(panedmaster, relief='flat', bg=_bg)
panedmaster.add(downpanel)
# editor panel
paned = PanedWindow(uppanel, relief='flat', sashwidth=20, sashcursor='arrow', orient='h', bg=_bg)
uppanel.add(paned)
# left panel
leftpanel = PanedWindow(paned, relief='flat', bg=_bg)
paned.add(leftpanel)
# right panel
rightpanel = PanedWindow(paned, sashwidth=15, sashcursor='arrow', relief='flat', bg=_bg)
paned.add(rightpanel)
# editor --> leftpanel
editor = Canvas(rightpanel, bg='#4287f5', relief='flat',cursor='dot')
editor.place(relwidth=1, relheight=1)
vbar = Scrollbar(editor, orient='vertical', width=20, relief='flat', bg=_bg, jump=0)
vbar.pack(side='right', fill='y')
vbar.config(command=editor.yview)
editor.configure(yscrollcommand=vbar.set)
hbar = Scrollbar(editor, orient='horizontal', width=20, relief='flat', bg=_bg)
hbar.pack(side='bottom', fill='x')
hbar.config(command=editor.xview)
editor.configure(xscrollcommand=hbar.set)
editor.create_window(0,0, width=100,height=20, window=Button(editor, text='<').place())

# piano-keyboard-editor
# piano = Canvas(downpanel, bg='black', relief='flat')
# downpanel.add(piano)

def scrollD(event):
    editor.xview('scroll', 1, 'units')
    #editor.configure(scrollregion=bbox_offset(editor.bbox("all")))
def scrollU(event):
    editor.xview('scroll', -1, 'units')
# linux scroll
if platform.system() == 'Linux':
    editor.bind("<5>", scrollD)
    editor.bind("<4>", scrollU)
# mac scroll
if platform.system() == 'Darwin':
    def _on_mousewheel(event):
        editor.yview_scroll(-1*(event.delta), "units")
    editor.bind("<MouseWheel>", _on_mousewheel)
# windows scroll
if platform.system() == 'Windows':
    def _on_mousewheel(event):
        editor.yview_scroll(int(-1*(event.delta)/120), "units")
    editor.bind("<MouseWheel>", _on_mousewheel)

# score setup --> rightpanel
separator1 = ttk.Separator(leftpanel, orient='horizontal').pack(fill='x')
fill_label1 = Label(leftpanel, text='TITLES',bg=_bg,fg='white',anchor='w')
fill_label1.pack(fill='x')
title_label = Label(leftpanel, text='Title: ',bg=_bg,fg='white',anchor='w')
title_label.pack(fill='x')
title_entry = Entry(leftpanel)
title_entry.pack(fill='x')
composer_label = Label(leftpanel, text='Composer: ',bg=_bg,fg='white',anchor='w')
composer_label.pack(fill='x')
composer_entry = Entry(leftpanel)
composer_entry.pack(fill='x')
copyright_label = Label(leftpanel, text='Copyright: ',bg=_bg,fg='white',anchor='w')
copyright_label.pack(fill='x')
copyright_entry = Entry(leftpanel)
copyright_entry.pack(fill='x')

fill_label2 = Label(leftpanel, text='',bg=_bg,fg='white',anchor='w')
fill_label2.pack(fill='x')
separator2 = ttk.Separator(leftpanel, orient='horizontal').pack(fill='x')
fill_label3 = Label(leftpanel, text='LAYOUT',bg=_bg,fg='white',anchor='w')
fill_label3.pack(fill='x')
mpline_label = Label(leftpanel, text='Measures each line: ',bg=_bg,fg='white',anchor='w')
mpline_label.pack(fill='x')
mpline_entry = Entry(leftpanel)
mpline_entry.pack(fill='x')
scale_label = Label(leftpanel, text='Global scale: ',bg=_bg,fg='white',anchor='w')
scale_label.pack(fill='x')
scale_entry = Entry(leftpanel)
scale_entry.pack(fill='x')
margin_label = Label(leftpanel, text='Margin: ',bg=_bg,fg='white',anchor='w')
margin_label.pack(fill='x')
margin_entry = Entry(leftpanel)
margin_entry.pack(fill='x')
system_label = Label(leftpanel, text='Space under system: ',bg=_bg,fg='white',anchor='w')
system_label.pack(fill='x')
system_entry = Entry(leftpanel)
system_entry.pack(fill='x')
apply_label = Label(leftpanel, text='',bg=_bg,fg='white',anchor='w')
apply_label.pack(fill='x')
apply_button = Button(leftpanel, text='Apply to score')
apply_button.pack(fill='x')

fill_label4 = Label(leftpanel, text='',bg=_bg,fg='white',anchor='w')
fill_label4.pack(fill='x')
separator2 = ttk.Separator(leftpanel, orient='horizontal').pack(fill='x')
noteinput_label = Label(leftpanel, text='NOTE INPUT',bg=_bg,fg='white',anchor='w')
noteinput_label.pack(fill='x')
length_label = Label(leftpanel, text='Note length:', anchor='w', bg=_bg, fg='white')
length_label.pack(fill='x')
list_dur = Listbox(leftpanel, height=8)
list_dur.pack(fill='x')
list_dur.insert(0, "1 whole")
list_dur.insert(1, "2 half")
list_dur.insert(2, "4 quarter")
list_dur.insert(3, "8 eight")
list_dur.insert(4, "16 sixteenth")
list_dur.insert(5, "32 ...")
list_dur.insert(6, "64 ...")
list_dur.insert(7, "128 ...")
divide_label = Label(leftpanel, text='÷', font=("courier", 20, "bold"), bg=_bg, fg='white')
divide_label.pack(fill='x')
divide_spin = Spinbox(leftpanel, from_=1, to=20)
divide_spin.pack(fill='x')



















#------------------
# constants
#------------------
QUARTER = 256
MM = root.winfo_fpixels('1m')
PAPER_HEIGHT = MM * 297  # a4 210x297 mm
PAPER_WIDTH = MM * 210
XYPAPER = 60
MARGIN = 30
PRINTEAREA_WIDTH = PAPER_WIDTH - (MARGIN*2)
PRINTEAREA_HEIGHT = PAPER_HEIGHT - (MARGIN*2)
MIDINOTECOLOR = '#b4b4b4'
BLACK = [2, 5, 7, 10, 12, 14, 17, 19, 22, 24, 26, 29, 31, 34, 36, 38, 41, 43, 46, 
            48, 50, 53, 55, 58, 60, 62, 65, 67, 70, 72, 74, 77, 79, 82, 84, 86]
FULLSTAFFHEIGHT = 490











#--------------------------------------------------------
# TOOLS (notation design, help functions etc...)
#--------------------------------------------------------
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
    if x < z and y > z:
        return True
    else:
        return False


def barline_pos(t_sig_map):
    '''
    This functions returns a list of all barline
    positions in the score based on the time signatures.
    '''
    b_lines = []
    bln_time = 0
    for i in t_sig_map:
        meas_len = measure_length((i['numerator'], i['denominator']))
        for meas in range(0,i['amount']):
            b_lines.append(bln_time)
            bln_time += meas_len
    return b_lines


def note_split_processor(note, t_sig_map):
    '''
    Returns a list of notes and if nessesary note split
    '''
    out = []

    # creating a list of barline positions.
    b_lines = barline_pos(t_sig_map)

    # detecting barline overlapping note.
    is_split = False
    split_points = []
    for i in b_lines:
        if is_in_range(note['time'], note['time']+note['duration'], i):
            split_points.append(i)
            is_split = True
    if is_split == False:
        out.append(note)
        return out
    elif is_split == True:
        start = note['time']
        end = note['time']+note['duration']
        for i in range(0,len(split_points)+1):
            if i == 0:# if first iteration
                out.append({'type':'note', 'note':note['note'], 'time':start, 'duration':split_points[0]-start, 'hand':0, 'beam':0, 'slur':0})
            elif i == len(split_points):# if last iteration
                out.append({'type':'split', 'note':note['note'], 'time':split_points[i-1], 'duration':end-split_points[i-1], 'hand':0, 'beam':0, 'slur':0})
                return out
            else:# if not first and not last iteration
                out.append({'type':'split', 'note':note['note'], 'time':split_points[i-1], 'duration':split_points[i]-split_points[i-1], 'hand':0, 'beam':0, 'slur':0})


def bbox_offset(bbox, offset):
    x1, y1, x2, y2 = bbox
    return (x1-offset, y1-offset, x2+offset, y2+offset)


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


def insert_x_pos(mouse_x):
    '''
        translates the mouse position on 
        the paper to a time in pianoticks.
    '''

    print(mouse_x)

    return 0


def new_line_pos(t_sig_map, mp_line):
    '''
    returns a list of the position of every new line of music.
    '''
    b_pos = barline_pos(t_sig_map)
    new_lines = []
    count = 0
    for bl in range(len(b_pos)):
        try:
            new_lines.append(b_pos[count])
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
        x = XYPAPER + MARGIN
        editor.create_line(x, y, x+PRINTEAREA_WIDTH, y, width=2, capstyle='round',fill='black',tag='staff')
        editor.create_line(x, y+(10*scale), x+PRINTEAREA_WIDTH, y+(10*scale), width=2, capstyle='round',fill='black',tag='staff')
        editor.create_line(x, y+(20*scale), x+PRINTEAREA_WIDTH, y+(20*scale), width=2, capstyle='round',fill='black',tag='staff')


    def draw2line(y):
        x = XYPAPER + MARGIN
        editor.create_line(x, y, x+PRINTEAREA_WIDTH, y, width=0.5, capstyle='round',fill='black',tag='staff')
        editor.create_line(x, y+(10*scale), x+PRINTEAREA_WIDTH, y+(10*scale), width=0.5, capstyle='round',fill='black',tag='staff')


    def draw_dash2line(y):
        x = XYPAPER + MARGIN
        if platform.system() == 'Linux' or platform.system() == 'Darwin':
            editor.create_line(x, y, x+PRINTEAREA_WIDTH, y, width=1, dash=(6,6), capstyle='round',fill='black',tag='staff')
            editor.create_line(x, y+(10*scale), x+PRINTEAREA_WIDTH, y+(10*scale), width=1, dash=(6,6), capstyle='round',fill='black',tag='staff')
        elif platform.system() == 'Windows':
            editor.create_line(x, y, x+PRINTEAREA_WIDTH, y, width=1, dash=4, capstyle='round',fill='black',tag='staff')
            editor.create_line(x, y+(10*scale), x+PRINTEAREA_WIDTH, y+(10*scale), width=1, dash=4, capstyle='round',fill='black',tag='staff')
        

    keyline = 0

    if mx >= 81:
        draw3line(0+y)
        draw2line((40*scale)+y)
        draw3line((70*scale)+y)
        draw2line((110*scale)+y)
        draw3line((140*scale)+y)
        draw2line((180*scale)+y)
        draw3line((210*scale)+y)
        keyline = (250*scale)
    if mx >= 76 and mx <= 80:
        draw2line(0+y)
        draw3line((30*scale)+y)
        draw2line((70*scale)+y)
        draw3line((100*scale)+y)
        draw2line((140*scale)+y)
        draw3line((170*scale)+y)
        keyline = (210*scale)
    if mx >= 69 and mx <= 75:
        draw3line(0+y)
        draw2line((40*scale)+y)
        draw3line((70*scale)+y)
        draw2line((110*scale)+y)
        draw3line((140*scale)+y)
        keyline = 180*scale
    if mx >= 64 and mx <= 68:
        draw2line(0+y)
        draw3line((30*scale)+y)
        draw2line((70*scale)+y)
        draw3line((100*scale)+y)
        keyline = 140*scale
    if mx >= 57 and mx <= 63:
        draw3line(0+y)
        draw2line((40*scale)+y)
        draw3line((70*scale)+y)
        keyline = 110*scale
    if mx >= 52 and mx <= 56:
        draw2line(0+y)
        draw3line((30*scale)+y)
        keyline = 70*scale
    if mx >= 45 and mx <= 51:
        draw3line(0+y)
        keyline = 40*scale

    draw_dash2line(keyline+y)

    if mn >= 33 and mn <= 39:
        draw3line(keyline+(30*scale)+y)
    if mn >= 28 and mn <= 32:
        draw3line(keyline+(30*scale)+y)
        draw2line(keyline+(70*scale)+y)
    if mn >= 21 and mn <= 27:
        draw3line(keyline+(30*scale)+y)
        draw2line(keyline+(70*scale)+y)
        draw3line(keyline+(100*scale)+y)
    if mn >= 16 and mn <= 20:
        draw3line(keyline+(30*scale)+y)
        draw2line(keyline+(70*scale)+y)
        draw3line(keyline+(100*scale)+y)
        draw2line(keyline+(140*scale)+y)
    if mn >= 9 and mn <= 15:
        draw3line(keyline+(30*scale)+y)
        draw2line(keyline+(70*scale)+y)
        draw3line(keyline+(100*scale)+y)
        draw2line(keyline+(140*scale)+y)
        draw3line(keyline+(170*scale)+y)
    if mn >= 4 and mn <= 8:
        draw3line(keyline+(30*scale)+y)
        draw2line(keyline+(70*scale)+y)
        draw3line(keyline+(100*scale)+y)
        draw2line(keyline+(140*scale)+y)
        draw3line(keyline+(170*scale)+y)
        draw2line(keyline+(210*scale)+y)
    if mn >= 1 and mn <= 3:
        draw3line(keyline+(30*scale)+y)
        draw2line(keyline+(70*scale)+y)
        draw3line(keyline+(100*scale)+y)
        draw2line(keyline+(140*scale)+y)
        draw3line(keyline+(170*scale)+y)
        draw2line(keyline+(210*scale)+y)
        editor.create_line(XYPAPER + MARGIN, (keyline+(240*scale)+y), XYPAPER + MARGIN + PRINTEAREA_WIDTH, (keyline+(240*scale)+y), width=2)


def get_staff_height(line, scale):
    #create linenotelist
    linenotelist = []
    for note in line:
        if note[0] == 'note' or note[0] == 'split' or note[0] == 'invis' or note[0] == 'cursor':
            linenotelist.append(note[3])
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
        for meas in range(0,i['amount']):
            bln_time += meas_len
    return bln_time


def event_x_pos(pos, start_line_tick, end_line_tick):
    '''
    returns the x position on the paper.
    '''
    factor = interpolation(start_line_tick,end_line_tick,pos)
    return XYPAPER + MARGIN + (PRINTEAREA_WIDTH * factor)


def t_sig_start_tick(t_sig_map,n):
    out = []
    tick = 0
    for i in t_sig_map:
        out.append(tick)
        tick += measure_length((i['numerator'], i['denominator'])) * i['amount']
    return out[n]


def process_margin(value):
    global QUARTER,MM,PAPER_HEIGHT,PAPER_WIDTH,XYPAPER
    global MARGIN,PRINTEAREA_WIDTH,PRINTEAREA_HEIGHT
    QUARTER = 256
    MM = root.winfo_fpixels('1m')
    PAPER_HEIGHT = MM * 297  # a4 210x297 mm
    PAPER_WIDTH = MM * 210
    XYPAPER = 30
    MARGIN = value
    PRINTEAREA_WIDTH = PAPER_WIDTH - (MARGIN*2)
    PRINTEAREA_HEIGHT = PAPER_HEIGHT - (MARGIN*2)


def note_active_grey(x0, x1, y, linenr, new_line):
    '''draws a midi note with a stop sign(vertical line at the end of the midi-note).'''
    x0 = event_x_pos(x0, linenr, new_line)
    x1 = event_x_pos(x1, linenr, new_line)
    editor.create_rectangle(x0, y-5, x1, y+5, fill='#e3e3e3', outline='')#e3e3e3
    editor.create_line(x1, y-5, x1, y+5, width=2)
    editor.create_line(x0, y-5, x0, y+5, width=2, fill='#e3e3e3')


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

    return cursy + (ylist[note-1]*scale) - (sub*scale)


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
    (r1,g1,b1) = root.winfo_rgb('white')
    (r2,g2,b2) = root.winfo_rgb(MIDINOTECOLOR)
    r_ratio = float(r2-r1) / width
    g_ratio = float(g2-g1) / width
    b_ratio = float(b2-b1) / width
    for i in range(math.ceil(width)):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
        editor.create_line(x0+i,y-(5*scale),x0+i,y+(5*scale), fill=color)
    editor.create_line(x1, y-(5*scale), x1, y+(5*scale), width=2)
    editor.create_line(x0, y-(5*scale), x0, y+(5*scale), width=2, fill='white')


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
    return base * round(x/base)


def mx2tick(mx,edit_grid,length_of_music,x_scale):
    '''
        This function converts the mouse position to
        (start) time in pianoticks.
    '''
    # defining the tick
    start = XYPAPER
    end = XYPAPER + (length_of_music * x_scale)
    tick = baseround(interpolation(start,end,mx) * length_of_music,edit_grid)

    return tick


def my2pitch(my,y_scale):
    '''
        This function converts the mouse position to
        pitch in pianokeynumber 1..88.
    '''
    staffheight = XYPAPER + FULLSTAFFHEIGHT * y_scale + (10 * y_scale)
    mouse_y_on_staff = my - XYPAPER + (20 * y_scale)
    percent = (interpolation(0,staffheight,mouse_y_on_staff))
    print(percent)

    return -round(percent * 88) % 88


def mx2duration(mx,time,edit_grid,length_of_music,x_scale):
    '''
        This function converts the mouse position to
        duration in pianoticks.
    '''
    t = mx2tick(mx,edit_grid,length_of_music,x_scale)

    

    return t

















#---------------------
# save file structure
#---------------------
'''
File structure:
A *.pnoscript file consists of a python list which contains
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

file = [
# score setup part:
[
    # t_sig_map; inside list because the order of the t_sig messages defines the time changes/score.
    [
    {'type':'time_signature','amount':16, 'numerator':4, 'denominator':4, 'grid':4, 'visible':1},
    #{'type':'time_signature','amount':4, 'numerator':6, 'denominator':8, 'grid':2, 'visible':1},
    ],

    # mp_line
    {'type':'mp_line', 'string':'5'},

    # titles
    {'type':'title', 'text':'Test_Version'},
    {'type':'composer', 'text':'PianoScript'},
    {'type':'copyright', 'text':'copyrights reserved 2022'},
    
    # scale; global scale
    {'type':'scale', 'value':1},

    # page margins
    {'type':'margin', 'value':50},

    # space under systems / in between
    {'type':'system_space', 'value':'60'}
],

# musical data part:
[
    # notes
    {'type': 'note', 'time': 0.0, 'duration': 64.0, 'note': 56, 'hand': 0, 'beam': 0, 'slur': 0},
    {'type': 'note', 'time': 64.0, 'duration': 64.0, 'note': 55, 'hand': 0, 'beam': 0, 'slur': 0},
    {'type': 'note', 'time': 128.0, 'duration': 64.0, 'note': 56, 'hand': 0, 'beam': 0, 'slur': 0},
    {'type': 'note', 'time': 192.0, 'duration': 64.0, 'note': 55, 'hand': 0, 'beam': 0, 'slur': 0},
    {'type': 'note', 'time': 256.0, 'duration': 64.0, 'note': 56, 'hand': 0, 'beam': 0, 'slur': 0},
    {'type': 'note', 'time': 320.0, 'duration': 64.0, 'note': 51, 'hand': 0, 'beam': 0, 'slur': 0},
    {'type': 'note', 'time': 384.0, 'duration': 64.0, 'note': 54, 'hand': 0, 'beam': 0, 'slur': 0},
    {'type': 'note', 'time': 448.0, 'duration': 64.0, 'note': 52, 'hand': 0, 'beam': 0, 'slur': 0},
    {'type': 'note', 'time': 512.0, 'duration': 128.0, 'note': 49, 'hand': 0, 'beam': 0, 'slur': 0}

    # text
    # {'type':'text', 'time':0, 'text':'play', 'bold':0, 'italic':1, 'underline':0},

    # slur
    # {'type':'slur', 'time':0, 'duration':2048, 'interpolx':.5, 'y':20, 'hand':0}
]
]











#------------------
# file management
#------------------
file_changed = 0
def new_file():
    if file_changed == 1:
        save_quest()

    mpline_entry.delete(0,'end')
    title_entry.delete(0,'end')
    composer_entry.delete(0,'end')
    copyright_entry.delete(0,'end')

    global file
    file = [
    # score setup part/settings:
    [
        # t_sig_map; inside list because the order of the t_sig messages defines the time changes/score.
        [
        {'type':'time_signature','amount':8, 'numerator':4, 'denominator':4, 'grid':4, 'visible':1},
        ],

        # mp_line
        {'type':'mp_line', 'string':'4'},

        # titles
        {'type':'title', 'text':'Untitled'},
        {'type':'composer', 'text':'PianoScript'},
        {'type':'copyright', 'text':'copyrights reserved 2022'},
        
        # scale; global scale
        {'type':'scale', 'value':1},

        # page margins; bottom,top,left,right together
        {'type':'margin', 'value':50},

        # space under systems / in between
        {'type':'system_space', 'value':60},

        # cursor
        {'type':'cursor', 'time':0, 'duration':128, 'note':40}
    ],

    # musical data part:
    [
        # time and duration are in piano-ticks; note 1..88 == pianokey; hand 0=left, 1=right
        {'type':'note', 'time':0, 'duration':2048, 'note':52, 'hand':0},
    ]
    ]
    render('normal', 0)



def open_file():
    print('open_file')
    f = filedialog.askopenfile(parent=root, mode='Ur', title='Open', filetypes=[("PianoScript files","*.pnoscript")], initialdir='~/Desktop/')
    if f:
        mpline_entry.delete(0,'end')
        title_entry.delete(0,'end')
        composer_entry.delete(0,'end')
        copyright_entry.delete(0,'end')
        filepath = f.name
        root.title('PnoScript - %s' % f.name)
        f = open(f.name, 'r', newline=None)
        global file
        file = ast.literal_eval(f.read())
        f.close()
        draw('event')
    return


def save_file():
    save_as()


def save_as():
    f = filedialog.asksaveasfile(parent=root, mode='w', filetypes=[("PianoScript files","*.pnoscript")], initialdir='~/Desktop/')
    if f:
        root.title('PnoScript - %s' % f.name)
        f = open(f.name, 'w')
        f.write(str(file))
        f.close()
        return


def save_quest():
    if messagebox.askyesno('Wish to save?', 'Do you wish to save the current file?'):
        save_file()
    else:
        return


def quit_editor(event='dummy'):

    root.destroy()












    
    


#--------------
# draw engine
#--------------
'''
    Test engine; I will test how big midi files perform if 
    I simply draw the whole file to the canvas from left to right.
'''

# variable storage
x_scale = .7
y_scale = 2

length_of_music = 0
noteid = 0

def draw(event):
    global length_of_music, file

    # remove all objects from the canvas.
    editor.delete('all')
    
    # DRAW GRID AND BARLINES
    length_staff = 0
    gx = 0
    bl_count = 1
    for ts,idx_ts in zip(file[0][0],range(len(file[0][0]))):
        numerator = ts['numerator']
        denominator = ts['denominator']
        amount = ts['amount']
        grid = ts['grid']

        l = measure_length((numerator,denominator)) * x_scale
        length_of_music += measure_length((numerator,denominator)) * amount

        # draw grid
        grid_dist = l / grid
        for grid1 in range(amount):

            length_staff += l

            # draw barline and barnumbering
            editor.create_line(XYPAPER+gx,
                XYPAPER,
                XYPAPER+gx,
                XYPAPER+FULLSTAFFHEIGHT*y_scale,
                width=2,
                fill='black',
                tag='staff')
            editor.create_text(XYPAPER+gx,
                XYPAPER,
                text=bl_count,
                anchor='s',
                font=('courier', round(12*y_scale), "bold"),
                tag='barnumbering')

            for grid2 in range(grid):

                # draw gridline
                editor.create_line(XYPAPER+gx+(grid_dist*grid2),
                    XYPAPER,
                    XYPAPER+gx+(grid_dist*grid2),
                    XYPAPER+FULLSTAFFHEIGHT*y_scale,
                    dash=(6,6),
                    fill='black',
                    tag='staff')

            gx += l
            bl_count += 1

        # draw endline
        if idx_ts+1 == len(file[0][0]):
            editor.create_line(XYPAPER+length_staff,
                XYPAPER,
                XYPAPER+length_staff,
                XYPAPER+FULLSTAFFHEIGHT*y_scale,
                fill='black',
                width=4,
                tag='staff')

    # DRAW STAFF
    y_axis = 0
    for staff in range(7):
        editor.create_line(XYPAPER,
            XYPAPER+y_axis,
            XYPAPER+length_staff,
            XYPAPER+y_axis,
            fill='black',
            width=2,
            tag='staff')
        editor.create_line(XYPAPER,
            XYPAPER+y_axis+(10*y_scale),
            XYPAPER+length_staff,
            XYPAPER+y_axis+(10*y_scale),
            fill='black',
            width=2,
            tag='staff')
        editor.create_line(XYPAPER,
            XYPAPER+y_axis+(20*y_scale),
            XYPAPER+length_staff,
            XYPAPER+y_axis+(20*y_scale),
            fill='black',
            width=2,
            tag='staff')
        if staff == 3:
            editor.create_line(XYPAPER,
                XYPAPER+y_axis+(40*y_scale),
                XYPAPER+length_staff,
                XYPAPER+y_axis+(40*y_scale),
                fill='black',
                width=1,
                tag='staff',
                dash=(6,6))
            editor.create_line(XYPAPER,
                XYPAPER+y_axis+(50*y_scale),
                XYPAPER+length_staff,
                XYPAPER+y_axis+(50*y_scale),
                fill='black',
                width=1,
                tag='staff',
                dash=(6,6))
        else:
            editor.create_line(XYPAPER,
                XYPAPER+y_axis+(40*y_scale),
                XYPAPER+length_staff,
                XYPAPER+y_axis+(40*y_scale),
                fill='black',
                width=1,
                tag='staff')
            editor.create_line(XYPAPER,
                XYPAPER+y_axis+(50*y_scale),
                XYPAPER+length_staff,
                XYPAPER+y_axis+(50*y_scale),
                fill='black',
                width=1,
                tag='staff')
        y_axis += 70 * y_scale
    editor.create_line(XYPAPER,
        XYPAPER+y_axis,
        XYPAPER+length_staff,
        XYPAPER+y_axis,
        fill='black',
        width=2,
        tag='staff')

    # DRAW PAPER
    editor.create_rectangle(XYPAPER-(30*y_scale),
        XYPAPER-(30*y_scale),
        XYPAPER+length_staff+(30*y_scale),
        XYPAPER+y_axis+(30*y_scale),
        fill='white',
        outline='black')


    # DRAW NOTES
    sh = staff_height(1,88,1)
    global noteid
    noteid = 0
    for note in file[1]:
        
        if note['type'] == 'note':

            # apply id to the note in file to find it back later
            note['id'] = 'note%i' % noteid
            
            # coordanates for midinote rectangle and notestart
            x0 = XYPAPER + (note['time'] * x_scale)
            x1 = XYPAPER + (((note['time'] + note['duration']) * x_scale))
            y = (note_y_pos(note['note'], 1, 88, XYPAPER, y_scale))
            y0 = y - (5 * y_scale)
            y1 = y + (5 * y_scale)

            # draw midi-note
            editor.create_rectangle(x0,
                y0,
                x1,
                y1,
                fill=MIDINOTECOLOR,
                outline='',
                tag=('note%i' % noteid, 'midinote'))
            editor.create_line(x1,
                y0,
                x1,
                y1,
                fill='black',
                width=2,
                tag=('note%i' % noteid, 'midinote'))

            # draw note start
            if note['hand'] == 0:
                editor.create_line(x0,
                    y,
                    x0,
                    y - (20 * y_scale),
                    width=2,
                    tag=('note%i' % noteid, 'notestart'))
            else:
                editor.create_line(x0,
                    y,
                    x0,
                    y + (20 * y_scale),
                    width=2,
                    tag=('note%i' % noteid, 'notestart'))
            if note['note'] in BLACK:
                editor.create_oval(x0,
                    y0,
                    x0 + (10 * y_scale),
                    y1,
                    outline='black',
                    fill='black',
                    width=2,
                    tag=('note%i' % noteid, 'notestart'))
            else:
                editor.create_oval(x0,
                    y0,
                    x0 + (10 * y_scale),
                    y1,
                    outline='black',
                    fill='white',
                    width=2,
                    tag=('note%i' % noteid, 'notestart'))

            noteid += 1

    
    editor.tag_raise('midinote')
    editor.tag_raise('staff')
    editor.tag_raise('notestart')
    editor.tag_raise('barnumbering')


    # update bbox
    editor.configure(scrollregion=bbox_offset(editor.bbox("all"), XYPAPER))













btn1_click = False
btn3_click = False
holdid = None
click_x = None
click_y = None
old_x = None
old_y = None

edit_grid = 128


def edit_note(event, event_type):
    '''
        event = event
        event_type = 'btn1click', 'btn1release' or 'motion'
    '''
    global btn1_click, holdid, old_x, old_y, click_x, click_y, btn3_click, noteid

    mx = editor.canvasx(event.x)
    my = editor.canvasy(event.y)

    if event_type == 'btn1click':

        btn1_click = True
        old_x = mx
        old_y = my
        click_x = mx
        click_y = my
        taglst = editor.gettags(editor.find_withtag('current'))
        print(taglst)
        
        # if we are not clicking on a note we are adding a note.
        if taglst == () or taglst[0] == 'staff' or taglst[0] == 'current':
            
            noteid += 1

            note = {'type': 'note', 'time': mx2tick(mx,edit_grid,length_of_music,x_scale), 'duration': edit_grid, 'note': my2pitch(my,y_scale), 'hand': 0, 'beam': 0, 'slur': 0, 'id':'note%i'%noteid}
            file[1].append(note)

            holdid = 'note%i'%noteid

            # coordanates for midinote rectangle and notestart
            x0 = XYPAPER + (note['time'] * x_scale)
            x1 = XYPAPER + (((note['time'] + note['duration']) * x_scale))
            y = (note_y_pos(note['note'], 1, 88, XYPAPER, y_scale))
            y0 = y - (5 * y_scale)
            y1 = y + (5 * y_scale)

            # draw midi-note
            editor.create_rectangle(x0,
                y0,
                x1,
                y1,
                fill=MIDINOTECOLOR,
                outline='',
                tag=(holdid, 'midinote'))
            editor.create_line(x1,
                y0,
                x1,
                y1,
                fill='black',
                width=2,
                tag=(holdid, 'midinote'))

            # draw note start
            if note['hand'] == 0:
                editor.create_line(x0,
                    y,
                    x0,
                    y - (20 * y_scale),
                    width=2,
                    tag=(holdid, 'notestart'))
            else:
                editor.create_line(x0,
                    y,
                    x0,
                    y + (20 * y_scale),
                    width=2,
                    tag=(holdid, 'notestart'))
            if note['note'] in BLACK:
                editor.create_oval(x0,
                    y0,
                    x0 + (10 * y_scale),
                    y1,
                    outline='black',
                    fill='black',
                    width=2,
                    tag=(holdid, 'notestart'))
            else:
                editor.create_oval(x0,
                    y0,
                    x0 + (10 * y_scale),
                    y1,
                    outline='black',
                    fill='white',
                    width=2,
                    tag=(holdid, 'notestart'))

            # update drawing order:
            editor.tag_raise('midinote')
            editor.tag_raise('staff')
            editor.tag_raise('notestart')
            editor.tag_raise('barnumbering')
        else:
            try:
                holdid = taglst[0]
            except IndexError:
                ...

        #editor.configure(cursor='none')

    elif event_type == 'btn1release':

        old_x = None
        old_y = None
        click_x = None
        click_y = None
        btn1_click = False
        holdid = None
        
        #editor.configure(cursor='dot')

    elif event_type == 'btn2click':

        holdid = editor.gettags(editor.find_withtag('current'))[0]

        if 'note' in holdid:

            # delete the note drawing
            editor.delete(holdid)

            for note in file[1]:

                if note['type'] == 'note':

                    if note['id'] == holdid:

                        file[1].remove(note)
                        break

    elif event_type == 'btn3click':

        btn3_click = True
        old_x = mx
        old_y = my
        click_x = mx
        click_y = my
        taglst = editor.gettags(editor.find_withtag('current'))
        print(taglst)
        
        # if we are not clicking on a note we are not editing.
        if taglst == () or taglst[0] == 'staff':
            return
        
        try:
            holdid = taglst[0]
        except IndexError:
            ...

        #editor.configure(cursor='none')

    elif event_type == 'btn3release':

        old_x = None
        old_y = None
        click_x = None
        click_y = None
        btn3_click = False
        holdid = None
        
        #editor.configure(cursor='dot')

    elif event_type == 'motion':

        # render cursor
        editor.delete('cursor')

        

        if btn3_click == True and holdid:
            
            if 'note' in holdid:

                # delete the note drawing
                editor.delete(holdid)

                # update note in file[1]
                for note in file[1]:
                    if note['type'] == 'note':
                        if note['id'] == holdid:
                            note['time'] = mx2tick(mx,edit_grid,length_of_music,x_scale)
                            note['note'] = my2pitch(my,y_scale)

                            # redraw the note
                            # coordanates for midinote rectangle and notestart
                            x0 = XYPAPER + (note['time'] * x_scale)
                            x1 = XYPAPER + (((note['time'] + note['duration']) * x_scale))
                            y = (note_y_pos(note['note'], 1, 88, XYPAPER, y_scale))
                            y0 = y - (5 * y_scale)
                            y1 = y + (5 * y_scale)

                            # draw midi-note
                            editor.create_rectangle(x0,
                                y0,
                                x1,
                                y1,
                                fill=MIDINOTECOLOR,
                                outline='',
                                tag=(holdid, 'midinote'))
                            editor.create_line(x1,
                                y0,
                                x1,
                                y1,
                                fill='black',
                                width=2,
                                tag=(holdid, 'midinote'))

                            # draw note start
                            if note['hand'] == 0:
                                editor.create_line(x0,
                                    y,
                                    x0,
                                    y - (20 * y_scale),
                                    width=2,
                                    tag=(holdid, 'notestart'))
                            else:
                                editor.create_line(x0,
                                    y,
                                    x0,
                                    y + (20 * y_scale),
                                    width=2,
                                    tag=(holdid, 'notestart'))
                            if note['note'] in BLACK:
                                editor.create_oval(x0,
                                    y0,
                                    x0 + (10 * y_scale),
                                    y1,
                                    outline='black',
                                    fill='black',
                                    width=2,
                                    tag=(holdid, 'notestart'))
                            else:
                                editor.create_oval(x0,
                                    y0,
                                    x0 + (10 * y_scale),
                                    y1,
                                    outline='black',
                                    fill='white',
                                    width=2,
                                    tag=(holdid, 'notestart'))

                            # update drawing order:
                            editor.tag_raise('midinote')
                            editor.tag_raise('staff')
                            editor.tag_raise('notestart')
                            editor.tag_raise('barnumbering')

        if btn1_click == True and holdid:
            
            if 'note' in holdid:

                # delete the note drawing
                editor.delete(holdid)

                # edit note in file and redraw note
                for note in file[1]:

                    if note['type'] == 'note':

                        if note['id'] == holdid:

                            duration_time = mx2tick(mx,edit_grid,length_of_music,x_scale) - note['time']
                            if duration_time < edit_grid:
                                duration_time = edit_grid
                            note['duration'] = duration_time
                            note['note'] = my2pitch(my,y_scale)

                            # coordanates for midinote rectangle and notestart
                            x0 = XYPAPER + (note['time'] * x_scale)
                            x1 = XYPAPER + (((note['time'] + note['duration']) * x_scale))
                            y = (note_y_pos(note['note'], 1, 88, XYPAPER, y_scale))
                            y0 = y - (5 * y_scale)
                            y1 = y + (5 * y_scale)

                            # draw midi-note
                            editor.create_rectangle(x0,
                                y0,
                                x1,
                                y1,
                                fill=MIDINOTECOLOR,
                                outline='',
                                tag=(holdid, 'midinote'))
                            editor.create_line(x1,
                                y0,
                                x1,
                                y1,
                                fill='black',
                                width=2,
                                tag=(holdid, 'midinote'))

                            # draw note start
                            if note['hand'] == 0:
                                editor.create_line(x0,
                                    y,
                                    x0,
                                    y - (20 * y_scale),
                                    width=2,
                                    tag=(holdid, 'notestart'))
                            else:
                                editor.create_line(x0,
                                    y,
                                    x0,
                                    y + (20 * y_scale),
                                    width=2,
                                    tag=(holdid, 'notestart'))
                            if note['note'] in BLACK:
                                editor.create_oval(x0,
                                    y0,
                                    x0 + (10 * y_scale),
                                    y1,
                                    outline='black',
                                    fill='black',
                                    width=2,
                                    tag=(holdid, 'notestart'))
                            else:
                                editor.create_oval(x0,
                                    y0,
                                    x0 + (10 * y_scale),
                                    y1,
                                    outline='black',
                                    fill='white',
                                    width=2,
                                    tag=(holdid, 'notestart'))

                            # update drawing order:
                            editor.tag_raise('midinote')
                            editor.tag_raise('staff')
                            editor.tag_raise('notestart')
                            editor.tag_raise('barnumbering')


















def midi_import():
    global file
    file = [
    # score setup part:
    [
        # t_sig_map; inside list because the order of the t_sig messages defines the time changes/score.
        [
            
        ],

        # mp_line
        {'type':'mp_line', 'string':'5 4'},

        # titles
        {'type':'title', 'text':'Test_Version'},
        {'type':'composer', 'text':'PianoScript'},
        {'type':'copyright', 'text':'copyrights reserved 2022'},
        
        # scale; global scale
        {'type':'scale', 'value':1},

        # page margins
        {'type':'margin', 'value':40},

        # space under systems / in between
        {'type':'system_space', 'value':'40'}
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
        filetypes=[("MIDI files","*.mid")]).name
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
        i['time'] +=  memory
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
            for t in mesgs[index+1:]:
                if t['type'] == 'time_signature' or t['type'] == 'end_of_track':
                    i['duration'] = t['time'] - i['time']
                    break
        index += 1


    # round time to piano-tick
    for i in mesgs:
        if i['type'] == 'note_on' or i['type'] == 'time_signature':
            i['time'] = round(i['time'],0)
            i['duration'] = round(i['duration'],0)
    
    # for debugging purposes print every midi message.
    # for i in mesgs:
    #     print(i)

    # write time_signatures:
    count = 0
    for i in mesgs:
        if i['type'] == 'time_signature':
            tsig = (i['numerator'], i['denominator'])
            amount = int(round(i['duration'] / measure_length(tsig),0))
            gridno = i['numerator']
            if tsig == '6/8':
                gridno = 2
            if tsig == '12/8':
                gridno = 4
            file[0][0].append({'type':i['type'], 'amount':amount, 'numerator':i['numerator'], 'denominator':i['denominator'], 'grid':gridno, 'visible':1})
            count += 1

    # write notes
    for i in mesgs:  
        if i['type'] == 'note_on' and i['channel'] == 0:
            file[1].append({'type':'note', 'time':i['time'], 'duration':i['duration'], 'note':i['note']-20, 'hand':0, 'beam':0, 'slur':0})
        if i['type'] == 'note_on' and i['channel'] >= 1:
            file[1].append({'type':'note', 'time':i['time'], 'duration':i['duration'], 'note':i['note']-20, 'hand':1, 'beam':0, 'slur':0})

    draw(file)












#------------------
# export
#------------------
def exportPDF():
    def is_tool(name):
        """Check whether `name` is on PATH and marked as executable."""
        return which(name) is not None
        print('exportPDF')


    if platform.system() == 'Linux':
        if is_tool('ps2pdfwr') == 0:
            messagebox.showinfo(title="Can't export PDF!", 
                message='PianoScript cannot export the PDF because function "ps2pdfwr" is not installed on your computer.')
            return
        
        f = filedialog.asksaveasfile(mode='w', parent=root, filetypes=[("pdf file","*.pdf")], initialfile=title, initialdir='~/Desktop')
        if f:
            pslist = []
            for rend in range(render('export')):
                editor.postscript(file="/tmp/tmp%s.ps" % rend, x=XYPAPER, y=XYPAPER+(rend*(PAPER_HEIGHT+XYPAPER)), width=PAPER_WIDTH, height=PAPER_HEIGHT, rotate=False)
                process = subprocess.Popen(["ps2pdfwr", "-sPAPERSIZE=a4", "-dFIXEDMEDIA", "-dEPSFitPage", "/tmp/tmp%s.ps" % rend, "/tmp/tmp%s.pdf" % rend])
                process.wait()
                os.remove("/tmp/tmp%s.ps" % rend)
                pslist.append("/tmp/tmp%s.pdf" % rend)
            cmd = 'pdfunite '
            for i in range(len(pslist)):
                cmd += pslist[i] + ' '
            cmd += '"%s"' % f.name
            process = subprocess.Popen(cmd, shell=True)
            process.wait()
            render('normal')
            return
        else:
            return
                
    elif platform.system() == 'Windows':
        f = filedialog.asksaveasfile(mode='w', parent=root, filetypes=[("pdf file","*.pdf")], initialfile=title, initialdir='~/Desktop')
        if f:
            print(f.name)
            counter = 0
            pslist = []
            for export in range(render('export')):
                counter += 1
                print('printing page ', counter)
                editor.postscript(file=f"{f.name}{counter}.ps", colormode='gray', x=40, y=50+(export*(paperheigth+50)), width=paperwidth, height=paperheigth, rotate=False)
                pslist.append(str('"'+str(f.name)+str(counter)+'.ps'+'"'))
            try:
                process = subprocess.Popen(f'''"{windowsgsexe}" -dQUIET -dBATCH -dNOPAUSE -dFIXEDMEDIA -sPAPERSIZE=a4 -dEPSFitPage -sDEVICE=pdfwrite -sOutputFile="{f.name}.pdf" {' '.join(pslist)}''', shell=True)
                process.wait()
                process.terminate()
                for i in pslist:
                    os.remove(i.strip('"'))
                f.close()
                os.remove(f.name)
            except:
                messagebox.showinfo(title="Can't export PDF!", message='Be sure you have selected a valid path in the default.pnoscript file. You have to set the path+gswin64c.exe. example: ~windowsgsexe{C:/Program Files/gs/gs9.54.0/bin/gswin64c.exe}')

















#--------------------------------------------------------
# MENU
#--------------------------------------------------------
menubar = Menu(root, relief='flat', bg='#333333', fg='white')
root.config(menu=menubar)

fileMenu = Menu(menubar, tearoff=0, bg='#333333', fg='white')

fileMenu.add_command(label='new', command=new_file)
fileMenu.add_command(label='open', command=open_file)
fileMenu.add_command(label='import MIDI', command=midi_import)
fileMenu.add_command(label='save', command=None)
fileMenu.add_command(label='save as', command=save_as)

fileMenu.add_separator()

submenu = Menu(fileMenu, tearoff=0, bg='#333333', fg='white')
submenu.add_command(label="postscript", command=None)
submenu.add_command(label="pdf", command=exportPDF)
fileMenu.add_cascade(label='export', menu=submenu, underline=0)

fileMenu.add_separator()

fileMenu.add_command(label="horizontal/vertical", underline=0, command=None)
fileMenu.add_command(label="fullscreen/windowed (F11)", underline=0, command=None)

fileMenu.add_separator()

fileMenu.add_command(label="exit", underline=0, command=None)
menubar.add_cascade(label="menu", underline=0, menu=fileMenu)

editMenu = Menu(menubar, tearoff=0, bg='#333333', fg='white')
editMenu.add_command(label='score setup...', command=None)
menubar.add_cascade(label="edit", underline=0, menu=editMenu)











#--------------------------------------------------------
# BIND (shortcuts)
#--------------------------------------------------------
root.bind('<Escape>', quit_editor)
editor.bind('<Motion>', lambda event: edit_note(event, 'motion'))
editor.bind('<Button-1>', lambda event: edit_note(event, 'btn1click'))
editor.bind('<ButtonRelease-1>', lambda event: edit_note(event, 'btn1release'))
editor.bind('<Button-2>', lambda event: edit_note(event, 'btn3click'))
editor.bind('<ButtonRelease-2>', lambda event: edit_note(event, 'btn3release'))
editor.bind('<Button-3>', lambda event: edit_note(event, 'btn2click'))
editor.bind('<r>', draw)


draw(file)







#--------------------------------------------------------
# MAINLOOP
#--------------------------------------------------------
#render(0,'normal', 10)
root.mainloop()


#--------------------------------------------------------
# TODO
#--------------------------------------------------------
'''
* grid editor
* render per page
* divide function note length
* save file
* toolbar
'''