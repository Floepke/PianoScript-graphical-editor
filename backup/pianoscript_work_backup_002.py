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
editor = Canvas(rightpanel, bg='grey', relief='flat',cursor='dot')
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
    editor.yview('scroll', int(event.y/200), 'units')
    #editor.configure(scrollregion=bbox_offset(editor.bbox("all")))
def scrollU(event):
    editor.yview('scroll', -abs(int(event.y/200)), 'units')
# linux scroll
if platform.system() == 'Linux':
    root.bind("<5>", scrollD)
    root.bind("<4>", scrollU)
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
XYPAPER = 30
MARGIN = 30
PRINTEAREA_WIDTH = PAPER_WIDTH - (MARGIN*2)
PRINTEAREA_HEIGHT = PAPER_HEIGHT - (MARGIN*2)
MIDINOTECOLOR = '#b4b4b4'
BLACK = [2, 5, 7, 10, 12, 14, 17, 19, 22, 24, 26, 29, 31, 34, 36, 38, 41, 43, 46, 
            48, 50, 53, 55, 58, 60, 62, 65, 67, 70, 72, 74, 77, 79, 82, 84, 86]











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
    {'type':'note', 'time':2048, 'duration':2048, 'note':52, 'hand':0, 'beam':0, 'slur':0},
    {'type':'note', 'time':128, 'duration':256, 'note':28, 'hand':1, 'beam':0, 'slur':0},
    {'type':'note', 'time':0, 'duration':512, 'note':40, 'hand':0, 'beam':0, 'slur':0}

    # text
    # {'type':'text', 'time':0, 'text':'play', 'bold':0, 'italic':1, 'underline':0}
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
    # score setup part:
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

        # page margins
        {'type':'margin', 'value':50},

        # space under systems / in between
        {'type':'system_space', 'value':60},

        # cursor
        {'type':'cursor', 'time':0, 'duration':128, 'note':40}
    ],

    # musical data part:
    [
        
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
        render('normal', 0)
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
t_sig_map = []
mp_line = []
msg = []
page_space = []
new_line = []
staff_rectangle_lst = []
title = ''
composer = ''
copyright = ''
system_space = []
header_space = 50
scale = 1
paper_color = 0
view_page = 0
ui_scale = 1.25

cursor = (0,40)
grid_step = 64
note_write = 0
click_y = None

# vars for editing notes
selected_note = None

def render(event, render_type, pageno=0, evt_type='nothing'):
    # check if there is a time_signature in the file.
    if not file[0][0]:
        print('ERROR: There is no time signature in the file!')
        return

    # remove all objects from the canvas.
    editor.delete('all')

    global paper_color, view_page
    if render_type == 'normal':
        paper_color = 'white'#ffe4de
    elif render_type == 'export':
        paper_color = 'white'


    def read_score_setup():
        '''
        Reads and writes the score setup
        settings to the score setup entry's
        from the file.
        '''
        # insert from file
        for i in file[0]:
            if isinstance(i,dict):
                if i['type'] == 'mp_line':
                    mpline_entry.delete(0,'end')
                    mpline_entry.insert(0,i['string'])
                if i['type'] == 'scale':
                    scale_entry.delete(0,'end')
                    scale_entry.insert(0,i['value'])
                if i['type'] == 'title':
                    title_entry.delete(0,'end')
                    title_entry.insert(0,i['text'])
                if i['type'] == 'composer':
                    composer_entry.delete(0,'end')
                    composer_entry.insert(0,i['text'])
                if i['type'] == 'copyright':
                    copyright_entry.delete(0,'end')
                    copyright_entry.insert(0,i['text'])
                if i['type'] == 'margin':
                    margin_entry.delete(0,'end')
                    margin_entry.insert(0,i['value'])
                if i['type'] == 'system_space':
                    system_entry.delete(0,'end')
                    system_entry.insert(0,i['value'])



    read_score_setup()

    
    def read():
        '''
        This function reads the file and translates it
        to a msg list; list containing nested lists:
        [pages[lines[notes]lines]pages]
        and it writes all settings to the right variables.
        '''
        # init utils lists and variables.
        global t_sig_map,mp_line,msg,MARGIN,title,composer,copyright
        global system_space,new_line,page_space,cursor,scale
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
        for i in file[0][0]:
            if i['type'] == 'time_signature':
                t_sig_map.append(i)
                # barline and grid messages
                meas_len = measure_length((i['numerator'], i['denominator']))
                grid_len = meas_len / i['grid']
                for meas in range(i['amount']):
                    msg.append(['barline', bln_time])
                    for grid in range(0,i['grid']):
                        msg.append(['gridline', grd_time])
                        grd_time += grid_len
                    bln_time += meas_len
                msg.append(['time_signature_text',t_sig_start_tick(t_sig_map,count),
                    meas_len,str(i['numerator'])+'/'+str(i['denominator'])])
                count += 1

            # mp_line
        for i in file[0]:
            if isinstance(i,dict):
                if i['type'] == 'mp_line':
                    try:
                        mpline = i['string'].split()
                        for mp in mpline:
                            mp_line.append(eval(mp))
                    except:
                        print('ERROR: mp_line string is not valid! mp_line is set to default value 5.')
                        mp_line.append(5)

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
                    try:
                        sys_space = i['value'].split()
                        for ss in sys_space:
                            system_space.append(eval(ss))
                    except:
                        print('ERROR: system_space string is not valid! system_space is set to default value 60.')
                        system_space.append(60)

            # cursor
                if i['type'] == 'cursor':
                    msg.append(['cursor',i['time'],i['duration'],i['note']])

        # musical data part:
        for i in file[1]:
            # note
            if i['type'] == 'note':
                for note in note_split_processor(i, t_sig_map):
                    msg.append([note['type'], note['time'], note['duration'], note['note'], note['hand']])

            # invisible note
            if i['type'] == 'invis':
                msg.append([note['type'], note['time'], note['duration'], note['note']])

            # text
            if i['type'] == 'text':
                msg.append([i['type'], i['time'], i['text'], i['bold'], i['italic'], i['underline']])

            # endline
            msg.append(['endline', end_bar_tick(t_sig_map)])


        # sort on starttime of event.
        msg.sort(key=lambda x: x[1])

        # placing the events in lists of lines.
        new_line = new_line_pos(t_sig_map, mp_line)
        msgs = msg
        msg = []
        count = 0
        for ln in new_line[:-1]:
            hlplst = []
            for evt in msgs:
                if evt[1] >= new_line[count] and evt[1] < new_line[count+1]:
                    hlplst.append(evt)
            msg.append(hlplst)
            count += 1


        # placing the lines in lists of pages.
        lineheight = []
        for line in msg:

            notelst = []
            for note in line:
                if note[0] == 'note' or note[0] == 'split' or note[0] == 'invis' or note[0] == 'cursor':
                    notelst.append(note[3])
                else:
                    pass
            try: 
                lineheight.append(staff_height(min(notelst), max(notelst), scale))
            except ValueError:
                lineheight.append(10*scale)

        msgs = msg
        msg = []
        curs_y = header_space
        pagelist = []
        icount = 0
        resspace = 0
        header = header_space
        for line, height in zip(msgs, lineheight):
            try:
                sys_space = system_space[icount]
            except IndexError:
                sys_space = system_space[-1]
            icount += 1
            curs_y += height + sys_space
            if icount == len(lineheight):#if this is the last iteration
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
                if curs_y <= PRINTEAREA_HEIGHT - header:#does fit on paper
                    pagelist.append(line)
                    resspace = PRINTEAREA_HEIGHT - curs_y
                elif curs_y > PRINTEAREA_HEIGHT - header:#does not fit on paper
                    msg.append(pagelist)
                    pagelist = []
                    pagelist.append(line)
                    curs_y = 0
                    curs_y += height + sys_space
                    page_space.append(resspace)
                    header = 0
                else:
                    pass

    if pageno > len(msg)-1:
        pageno = 0
        view_page = 0
    elif pageno < 0:
        pageno = len(msg)-1
        view_page = len(msg)-1


        # for page in msg:
        #     print('newpage:')
        #     for line in page:
        #         print('newline:')
        #         for note in line:
        #             if note[0] == 'note' or note[0] == 'split' or note[0] == 'endline':
        #                 print(note)
        # print(page_space)
















    # in this place i define a list that contains all info for
    # calculating the note position on the paper to be detected by
    # the note edit and add function.
    # [lines]



















    read()

    def draw():
        global selected_note, click_y

        # draw paper
        editor.create_rectangle(XYPAPER,
            XYPAPER,
            XYPAPER+PAPER_WIDTH,
            XYPAPER+PAPER_HEIGHT, 
            outline='', fill=paper_color)

        curs_y = XYPAPER + MARGIN

        l_counter = 0
        b_counter = 1

        # PAGE in message list
        for page, idx_page in zip(msg,range(len(msg))):
            
            # only draw the symbols of the selected page
            if idx_page != pageno:
                l_counter += len(page)
                continue

            # copyrights / footer
            editor.create_text(MARGIN+XYPAPER,
                curs_y + PAPER_HEIGHT - MARGIN - XYPAPER,
                text='page %s of %s | %s | %s' % (idx_page+1, len(msg), title, copyright),
                anchor='nw',
                font=('courier', round(18*scale), "normal"),
                tag='titles',
                fill='black')

            if pageno == 0: 
                curs_y = XYPAPER + MARGIN + header_space
            else:
                curs_y = XYPAPER + MARGIN

            # LINE of music
            for line, idx_line in zip(page,range(len(page))):

                staffheight, minnote, maxnote = get_staff_height(line, scale)

                # draw end-of-line barline
                editor.create_line(XYPAPER+MARGIN+PRINTEAREA_WIDTH,
                    curs_y,
                    XYPAPER+MARGIN+PRINTEAREA_WIDTH,
                    curs_y+staffheight,
                    width=2*scale,
                    capstyle='round',
                    tag='grid',
                    fill='black')
                
                # MSGS in lines
                for msgs, idx_msgs in zip(line,range(len(line))):
                    #print(msgs)

                    # barline and numbering
                    if msgs[0] == 'barline':
                        x = event_x_pos(msgs[1],new_line[l_counter],new_line[l_counter+1])
                        editor.create_line(x,
                            curs_y,
                            x,
                            curs_y+staffheight,
                            width=2*scale,
                            capstyle='round',
                            tag='grid',
                            fill='black')
                        editor.create_text(x,
                            curs_y,
                            text=b_counter,#fix later TODO
                            tag='grid',
                            fill='black',
                            font=('courier', round(12*scale), "bold"),
                            anchor='s')
                        b_counter += 1
                    
                    # grid
                    if msgs[0] == 'gridline':
                        x = event_x_pos(msgs[1],new_line[l_counter],new_line[l_counter+1])
                        editor.create_line(x,
                            curs_y,
                            x,
                            curs_y+staffheight,
                            width=1*scale,
                            capstyle='round',
                            tag='grid',
                            fill='black',
                            dash=(6,6))

                    # staff
                    draw_staff_lines(curs_y, minnote, maxnote, scale)

                    # note start
                    if msgs[0] == 'note':
                        x = event_x_pos(msgs[1],new_line[l_counter],new_line[l_counter+1])
                        y = note_y_pos(msgs[3], minnote, maxnote, curs_y, scale)
                        # right hand note design
                        if msgs[4] == 0: 
                            if msgs[3] in BLACK:
                                editor.create_oval(x,
                                    y-(5*scale),
                                    x+(5*scale),
                                    y+(5*scale),
                                    width=2*scale,
                                    fill='black',
                                    outline='black',
                                    tag='note_start')
                            else:
                                editor.create_oval(x,
                                    y-(5*scale),
                                    x+(10*scale),
                                    y+(5*scale),
                                    width=2*scale,
                                    fill='white',
                                    outline='black',
                                    tag='note_start')
                            editor.create_line(x,
                                y-(25*scale),
                                x,
                                y,
                                width=2*scale,
                                fill='black',
                                tag='note_start')
                        # left hand note design
                        if msgs[4] == 1: 
                            if msgs[3] in BLACK:
                                editor.create_oval(x,
                                    y-(5*scale),
                                    x+(5*scale),
                                    y+(5*scale),
                                    width=2*scale,
                                    fill='black',outline='black',tag='note_start')
                            else:
                                editor.create_oval(x,
                                    y-(5*scale),
                                    x+(10*scale),
                                    y+(5*scale),
                                    width=2*scale,
                                    fill='white',outline='black',tag='note_start')
                            editor.create_line(x,
                                y+(25*scale),
                                x,
                                y,
                                width=2*scale,
                                fill='black',
                                tag='note_start')

                    # note active
                    if msgs[0] == 'note':
                        x0 = event_x_pos(msgs[1],new_line[l_counter],new_line[l_counter+1])
                        x1 = event_x_pos(msgs[1]+msgs[2],new_line[l_counter],new_line[l_counter+1])
                        y = note_y_pos(msgs[3], minnote, maxnote, curs_y, scale)
                        editor.create_rectangle(x0,
                            y-(5*scale),
                            x1,
                            y+(5*scale),
                            fill=MIDINOTECOLOR,
                            outline='',
                            tag='midi_note')
                        editor.create_line(x1,
                            y-(5*scale),
                            x1,y+(5*scale),
                            width=2*scale,
                            fill='black',
                            tag='midi_note')
                    if msgs[0] == 'split':
                        x0 = event_x_pos(msgs[1],new_line[l_counter],new_line[l_counter+1])
                        x1 = event_x_pos(msgs[1]+msgs[2],new_line[l_counter],new_line[l_counter+1])
                        y = note_y_pos(msgs[3], minnote, maxnote, curs_y, scale)
                        editor.create_rectangle(x0,
                            y-(5*scale),
                            x1,
                            y+(5*scale),
                            fill=MIDINOTECOLOR,
                            outline='',
                            tag='midi_note')
                        editor.create_oval(x0+(5*scale),
                            y-(2.5*scale),
                            x0+(10*scale),
                            y+(2.5*scale),
                            fill='black',
                            outline='',
                            tag='midi_note')
                        editor.create_line(x1,
                            y-(5*scale),
                            x1,
                            y+(5*scale),
                            width=2*scale,
                            tag='midi_note')

                    













                    if not isinstance(event,str):
                        # the position of the mouse on the canvas in px
                        mx = editor.canvasx(event.x) / ui_scale
                        my = editor.canvasy(event.y) / ui_scale
                        if msgs[0] == 'note':

                            y = note_y_pos(msgs[3], minnote, maxnote, curs_y, scale)

                            # defining the detection rectangle for the mouse
                            x0 = event_x_pos(msgs[1],new_line[l_counter],new_line[l_counter+1])
                            x1 = event_x_pos(msgs[2]+msgs[1],new_line[l_counter],new_line[l_counter+1])
                            y0 = (y - (5 * scale))
                            y1 = y + (5 * scale)

                            if x1 == x0:
                                x1 = x0 + (10 * scale)
                            

                            if evt_type == 'btn1click':

                                click_y = my
                                
                                if mx >= x0 and mx < x1 and my >= y0 and my < y1:

                                    for sv,idx_sv in zip(file[1],range(len(file[1]))):
                                        if sv['type'] == 'note' and sv['time'] == msgs[1] and sv['note'] == msgs[3]:
                                            print('!',idx_sv)
                                            selected_note = idx_sv


                            if evt_type == 'btn1release':
                                selected_note = None


                            if evt_type == 'motion':
                                
                                # if we are editing a note.
                                if selected_note != None:

                                    # the note beiing edited
                                    edit_note = file[1][selected_note]

                                    if msgs[0] == 'note' and msgs[1] == edit_note['time'] and msgs[3] == edit_note['note']:

                                        # pitch up
                                        if my < y-(5*scale):
                                            
                                            # is_not_transposed = True
                                            # n = file[1][selected_note]['note']
                                            # while is_not_transposed:
                                                
                                            #     n += 1
                                            #     if n > 88:
                                            #         n -= 1
                                            #         break
                                            #     y = note_y_pos(n, minnote, maxnote, curs_y, scale)
                                            #     y0 = (y - (5 * scale))
                                            #     y1 = y + (5 * scale)
                                            #     if my > y0 and my < y1:
                                            #         is_not_transposed = False
                                            
                                            file[1][selected_note]['note'] += 1
                                            if file[1][selected_note]['note'] > 88:
                                                file[1][selected_note]['note'] = 88
                                        
                                        # pitch down
                                        if my > y+(5*scale):
                                            
                                            # is_not_transposed = True
                                            # n = file[1][selected_note]['note']
                                            # while is_not_transposed:
                                                
                                            #     n -= 1
                                            #     if n < 1:
                                            #         n += 1
                                            #         break
                                            #     y = note_y_pos(n, minnote, maxnote, curs_y, scale)
                                            #     y0 = (y - (5 * scale))
                                            #     y1 = y + (5 * scale)
                                            #     if my > y0 and my < y1:
                                            #         is_not_transposed = False
                                            
                                            file[1][selected_note]['note'] -= 1
                                            if file[1][selected_note]['note'] < 1:
                                                file[1][selected_note]['note'] = 1
                                # if adding note
                                else:
                                    ...
    
                # update curs_y
                try:
                    sys_space = system_space[l_counter]
                except IndexError:
                    sys_space = system_space[-1]
                
                if len(msg)-1 == pageno:
                    curs_y += staffheight + (sys_space)
                else:
                    curs_y += staffheight + (sys_space) + (page_space[pageno] / (len(msg[pageno])-1))

                # update line counter
                l_counter += 1


        # drawing order
        editor.tag_raise('paper')
        editor.tag_raise('midi_note')
        editor.tag_raise('staff')
        editor.tag_raise('grid')
        editor.tag_raise('tsig_text')
        editor.tag_raise('other')
        editor.tag_raise('white_space')
        editor.tag_raise('note_start')
        editor.tag_raise('connect_stem')
        editor.tag_raise('titles')
        editor.tag_raise('cursor')

    draw()

















    
    def edit():
        global selected_note

        try:
            is_evt = event.x
        except:
            return

        edited_note = []

        # FIND NOTE
        l_counter = 0
        b_counter = 1
        loop = True

        # PAGE in message list
        for page, idx_page in zip(msg,range(len(msg))):

            if loop == False:
                break
            
            # only draw the symbols of the selected page
            if idx_page != pageno:
                l_counter += len(page)
                continue

            if pageno == 0: 
                curs_y = XYPAPER + MARGIN + header_space
            else:
                curs_y = XYPAPER + MARGIN

            # LINE of music
            for line, idx_line in zip(page,range(len(page))):

                if loop == False:
                    break

                staffheight, minnote, maxnote = get_staff_height(line, scale)
                
                # MSGS in lines
                for msgs, idx_msgs in zip(line,range(len(line))):

                    # the position of the mouse on the canvas in px
                    mx = editor.canvasx(event.x) / ui_scale
                    my = editor.canvasy(event.y) / ui_scale
                    if msgs[0] == 'note':

                        y = note_y_pos(msgs[3], minnote, maxnote, curs_y, scale)

                        # defining the detection rectangle for the mouse
                        x0 = event_x_pos(msgs[1],new_line[l_counter],new_line[l_counter+1])
                        x1 = event_x_pos(msgs[2]+msgs[1],new_line[l_counter],new_line[l_counter+1])
                        y0 = (y - (5 * scale))
                        y1 = y + (5 * scale)

                        if x1 == x0:
                            x1 = x0 + (10 * scale)
                        

                        if evt_type == 'btn1click':
                            
                            if mx >= x0 and mx < x1 and my >= y0 and my < y1:

                                for sv,idx_sv in zip(file[1],range(len(file[1]))):
                                    if sv['type'] == 'note' and sv['time'] == msgs[1] and sv['note'] == msgs[3]:
                                        print('!',idx_sv)
                                        selected_note = idx_sv
                                        break


                        if evt_type == 'btn1release':
                            selected_note = None


                        if evt_type == 'motion':
                            
                            # if we are editing a note.
                            if selected_note != None:

                                # the note beiing edited
                                edit_note = file[1][selected_note]

                                if msgs[0] == 'note' and msgs[1] == edit_note['time'] and msgs[3] == edit_note['note']:
            
                                    # pitch up
                                    if my < y0:
                                        
                                        is_not_transposed = True
                                        n = file[1][selected_note]['note']
                                        while is_not_transposed:
                                            
                                            n += 1
                                            if n > 88:
                                                n -= 1
                                                break
                                            y = note_y_pos(n, minnote, maxnote, curs_y, scale)
                                            y0 = (y - (5 * scale))
                                            y1 = y + (5 * scale)
                                            if my > y0 and my < y1:
                                                is_not_transposed = False
                                        
                                        file[1][selected_note]['note'] = n

                                        break
                                    
                                    # pitch down
                                    if my > y1:
                                        
                                        is_not_transposed = True
                                        n = file[1][selected_note]['note']
                                        while is_not_transposed:
                                            
                                            n -= 1
                                            if n < 1:
                                                n += 1
                                                break
                                            y = note_y_pos(n, minnote, maxnote, curs_y, scale)
                                            y0 = (y - (5 * scale))
                                            y1 = y + (5 * scale)
                                            if my > y0 and my < y1:
                                                is_not_transposed = False
                                        
                                        file[1][selected_note]['note'] = n 

                                        break
                            # if adding note
                            else:
                                ...

                            
    
                # update curs_y
                try:
                    sys_space = system_space[l_counter]
                except IndexError:
                    sys_space = system_space[-1]
                
                if len(msg)-1 == pageno:
                    curs_y += staffheight + (sys_space)
                else:
                    curs_y += staffheight + (sys_space) + (page_space[pageno] / (len(msg[pageno])-1))

                # update line counter
                l_counter += 1

        # edit note with keyboard
        if edited_note:
            print('edited_note ', edited_note)

        # add note
        if evt_type == 'btn2click':
            file[1].append({'type':'note', 'time':256, 'duration':512, 'note':88, 'hand':0, 'beam':0, 'slur':0})

    #edit()

    













    if not render_type == 'export':
        editor.scale("all", 0, 0, ui_scale, ui_scale)
    editor.configure(scrollregion=bbox_offset(editor.bbox("all"), XYPAPER))
    return len(msg)

































#------------------
# editor functions
#------------------
def score_setup():
    pass


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

    # insert cursor
    file[0].append({'type':'cursor', 'time':0, 'duration':256, 'note':40})

    render('event', 'normal', view_page, 'nothing')












def move_cursor(event):
    global file
    if event.keysym == 'Up':
        for i in file[0]:
            if isinstance(i,dict):
                if i['type'] == 'cursor':
                    i['note'] += 1
                    if i['note'] > 88:
                        i['note'] = 88
    elif event.keysym == 'Down':
        for i in file[0]:
            if isinstance(i,dict):
                if i['type'] == 'cursor':
                    i['note'] -= 1
                    if i['note'] < 1:
                        i['note'] = 1
    elif event.keysym == 'Left':
        for i in file[0]:
            if isinstance(i,dict):
                if i['type'] == 'cursor':
                    i['time'] -= i['duration']
                    if i['time'] < 0:
                        i['time'] = 0
    elif event.keysym == 'Right':
        for i in file[0]:
            if isinstance(i,dict):
                if i['type'] == 'cursor':
                    i['time'] += i['duration']
    render('normal', view_page)












def change_grid(event):

    if event.keysym == 'F1':
        for i in file[0]:
            if isinstance(i,dict):
                if i['type'] == 'cursor':
                    i['duration'] = 1024
    if event.keysym == 'F2':
        for i in file[0]:
            if isinstance(i,dict):
                if i['type'] == 'cursor':
                    i['duration'] = 512
    if event.keysym == 'F3':
        for i in file[0]:
            if isinstance(i,dict):
                if i['type'] == 'cursor':
                    i['duration'] = 256
    if event.keysym == 'F4':
        for i in file[0]:
            if isinstance(i,dict):
                if i['type'] == 'cursor':
                    i['duration'] = 128
    if event.keysym == 'F5':
        for i in file[0]:
            if isinstance(i,dict):
                if i['type'] == 'cursor':
                    i['duration'] = 64
    if event.keysym == 'F6':
        for i in file[0]:
            if isinstance(i,dict):
                if i['type'] == 'cursor':
                    i['duration'] = 32
    if event.keysym == 'F7':
        for i in file[0]:
            if isinstance(i,dict):
                if i['type'] == 'cursor':
                    i['duration'] = 16
    if event.keysym == 'F8':
        for i in file[0]:
            if isinstance(i,dict):
                if i['type'] == 'cursor':
                    i['duration'] = 8
    if event.keysym == 'F9':
        for i in file[0]:
            if isinstance(i,dict):
                if i['type'] == 'cursor':
                    i['duration'] = simpledialog.askstring('Enter a duration in piano-ticks.',
                        'Pianoticks;\n256 piano-ticks == one quarter note.',
                        parent=root)












def apply_score_setup():

    for i in file[0]:
        if isinstance(i,dict):
            if i['type'] == 'mp_line':
                i['string'] = mpline_entry.get()
            if i['type'] == 'scale':
                i['value'] = eval(scale_entry.get())
            if i['type'] == 'title':
                i['text'] = title_entry.get()
            if i['type'] == 'composer':
                i['text'] = composer_entry.get()
            if i['type'] == 'copyright':
                i['text'] = copyright_entry.get()
            if i['type'] == 'margin':
                i['value'] = eval(margin_entry.get())
            if i['type'] == 'system_space':
                i['value'] = system_entry.get()

    render('normal', view_page)


apply_button.configure(command=apply_score_setup)


def next_page(event):
    global view_page
    view_page += 1
    render('normal', view_page)


def prev_page(event):
    global view_page
    view_page -= 1
    render('normal', view_page)



















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
# root.bind('<Up>',move_cursor)
# root.bind('<Down>',move_cursor)
# root.bind('<Left>',move_cursor)
# root.bind('<Right>',move_cursor)
#list_dur.bind("<<ListboxSelect>>", change_length)
root.bind('<Next>', next_page)
root.bind('<Prior>', prev_page)
editor.bind('<Motion>', lambda event: render(event, 'normal', view_page, 'motion'))
editor.bind('<Button-1>', lambda event: render(event, 'normal', view_page, 'btn1click'))
editor.bind('<ButtonRelease-1>', lambda event: render(event, 'normal', view_page, 'btn1release'))
root.bind('<F1>', change_grid)
root.bind('<F2>', change_grid)
root.bind('<F3>', change_grid)
root.bind('<F4>', change_grid)
root.bind('<F5>', change_grid)
root.bind('<F6>', change_grid)
root.bind('<F7>', change_grid)
root.bind('<F8>', change_grid)
root.bind('<F9>', change_grid)
root.bind('<Escape>', quit_editor)











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