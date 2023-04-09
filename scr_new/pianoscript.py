# ----------------------
# welcome text on start
# ----------------------
print('**************************************************')
print('* Welcome to PianoScript music notation! Look on *')
print('* http://www.pianoscript.org/manual/ to read the *')
print('* manual on how to use PianoScript software.     *')
print('*                                                *')
print('* All terminal output can be sent to             *')
print('* philipbergwerf@gmail.com if you discovered a   *')
print('* bug or crash in the program.                   *')
print('* Have fun!                                      *')
print('**************************************************')


# --------------------
# IMPORTS
# --------------------
from tkinter import Tk, Canvas, Menu, Scrollbar, messagebox, PanedWindow, Listbox, Text
from tkinter import filedialog, Frame, Entry, Label, Spinbox, StringVar, PhotoImage
from tkinter import simpledialog, colorchooser
import time, ast, platform, subprocess, os, sys, errno, math, threading, random, json, traceback, datetime
from mido import MidiFile
from shutil import which
import tkinter.ttk as ttk
if platform.system() == 'Darwin':
    from tkmacosx import Button
else:
    from tkinter import Button

# --------------------
# GUI
# --------------------
# colors
def inverted_color(color):
    r = str(color[1]+color[2])
    g = str(color[3]+color[4])
    b = str(color[5]+color[6])
    R = 255 - int(r,16);
    G = 255 - int(g,16);
    B = 255 - int(b,16);
    R = format(R, 'x')
    G = format(G, 'x')
    B = format(B, 'x')
    if R == '0':
        R = '00'
    if G == '0':
        G = '00'
    if B == '0':
        B = '00'
    return '#' + R + G + B

color_basic_gui = '#002B36'#002B36
color_right_midinote = '#999999'
color_left_midinote = color_right_midinote 
color_editor_canvas = inverted_color(color_basic_gui)#eee8d5
color_highlight = '#268bd2'
color_notation_editor = color_basic_gui
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
panedmaster = PanedWindow(root, orient='h', sashwidth=0, relief='flat', bg=color_basic_gui)
panedmaster.place(relwidth=1, relheight=1)
leftpanel = PanedWindow(panedmaster, relief='flat', bg=color_basic_gui, width=50)
panedmaster.add(leftpanel)
midpanel = PanedWindow(panedmaster, relief='flat', bg=color_basic_gui, orient='h', sashwidth=10, width=scrwidth * 0.8)
panedmaster.add(midpanel)
rightpanel = PanedWindow(midpanel, relief='flat', bg=color_basic_gui)
midpanel.add(rightpanel)
# editor panel
root.update()
editorpanel = PanedWindow(midpanel, relief='groove', orient='h', bg=color_basic_gui, width=(scrwidth - 50) / 3 * 1.8)
midpanel.add(editorpanel)

# print panel
printpanel = PanedWindow(midpanel, relief='groove', orient='h', bg=color_basic_gui)
midpanel.add(printpanel)
# editor --> editorpanel
editor = Canvas(editorpanel, bg=color_editor_canvas, relief='flat', cursor='cross')
editor.place(relwidth=1, relheight=1)
hbar = Scrollbar(editor, orient='horizontal', width=20, relief='flat', bg=color_basic_gui)
hbar.pack(side='bottom', fill='x')
hbar.config(command=editor.xview)
editor.configure(xscrollcommand=hbar.set)   
# printview --> printpanel
pview = Canvas(printpanel, bg=color_editor_canvas, relief='flat')
pview.place(relwidth=1, relheight=1)

noteinput_label = Label(leftpanel, text='GRID:', bg=color_basic_gui, fg='white', anchor='w', font=("courier"))
noteinput_label.pack(fill='x')
list_dur = Listbox(leftpanel, height=8, bg='grey', selectbackground=color_highlight, fg='black')
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
divide_label = Label(leftpanel, text='÷', font=("courier", 20, "bold"), bg=color_basic_gui, fg='white', anchor='w')
divide_label.pack(fill='x')
divide_spin = Spinbox(leftpanel, from_=1, to=100, bg=color_highlight, font=('', 15, 'normal'))
divide_spin.pack(fill='x')
times_label = Label(leftpanel, text='×', font=("courier", 20, "bold"), bg=color_basic_gui, fg='white', anchor='w')
times_label.pack(fill='x')
times_spin = Spinbox(leftpanel, from_=1, to=100, bg=color_highlight, font=('', 15, 'normal'))
times_spin.pack(fill='x')
fill_label1 = Label(leftpanel, text='', bg=color_basic_gui, fg='white', anchor='w', font=("courier"))
fill_label1.pack(fill='x')
mode_label = Label(leftpanel, text='MODE:', bg=color_basic_gui, fg='white', anchor='w', font=("courier"))
mode_label.pack(fill='x')
input_right_img = PhotoImage(file='icons/noteinput_R.png')
input_right_button = Button(leftpanel, image=input_right_img, activebackground='#f0f0f0', bg=color_highlight)
input_right_button.pack(fill='x')
input_left_img = PhotoImage(file='icons/noteinput_L.png')
input_left_button = Button(leftpanel, image=input_left_img, bg='#f0f0f0', activebackground='#f0f0f0')
input_left_button.pack(fill='x')
txt_button_img = PhotoImage(file='icons/textinput.png')
txt_button = Button(leftpanel, image=txt_button_img, bg='#f0f0f0', activebackground='#f0f0f0')
txt_button.pack(fill='x')
countline_button_img = PhotoImage(file='icons/countline.png')
countline_button = Button(leftpanel, image=countline_button_img, bg='#f0f0f0', activebackground='#f0f0f0')
countline_button.pack(fill='x')

# rightpanel --> grid, devision, divide
fill_label5 = Label(rightpanel, text='GRID MAP EDITOR', bg=color_basic_gui, fg='white', anchor='w', font=("courier"))
fill_label5.pack(fill='x')
help_button1 = Button(rightpanel, text='?', font=("courier", 12, 'bold'))
help_button1.pack(fill='x')
gridedit_text = Text(rightpanel, bg='grey', height=6)
gridedit_text.pack(fill='x')
applygrid_button = Button(rightpanel, text='Apply', anchor='w')
applygrid_button.pack(fill='x')
fill_label9 = Label(rightpanel, text='', bg=color_basic_gui, fg='white', anchor='w', font=("courier"))
fill_label9.pack(fill='x')
fill_label7 = Label(rightpanel, text='SYSTEM MARGIN EDITOR (mm)', bg=color_basic_gui, fg='white', anchor='w', font=("courier"))
fill_label7.pack(fill='x')
help_button2 = Button(rightpanel, text='?', font=("courier", 12, 'bold'))
help_button2.pack(fill='x')
system_margin_text = Text(rightpanel, bg='grey', height=6)
system_margin_text.pack(fill='x')
applyspace_button = Button(rightpanel, text='Apply', anchor='w')
applyspace_button.pack(fill='x')
fill_label10 = Label(rightpanel, text='', bg=color_basic_gui, fg='white', anchor='w', font=("courier"))
fill_label10.pack(fill='x')
fill_label11 = Label(rightpanel, text='MEASURE DIVISION EDITOR', bg=color_basic_gui, fg='white', anchor='w', font=("courier"))
fill_label11.pack(fill='x')
help_button3 = Button(rightpanel, text='?', font=("courier", 12, 'bold'))
help_button3.pack(fill='x')
measureseachline_text = Text(rightpanel, bg='grey', height=6)
measureseachline_text.pack(fill='x')
applymeasures_button = Button(rightpanel, text='Apply', anchor='w')
applymeasures_button.pack(fill='x')

# changes in ui for windows:
if platform.system() == 'Windows':
    noteinput_label.configure(font=("courier", 12))
    mode_label.configure(font=("courier", 12))















# ------------------
# constants
# ------------------
QUARTER = 256
MM = root.winfo_fpixels('1m')
BLACK = [2, 5, 7, 10, 12, 14, 17, 19, 22, 24, 26, 29, 31, 34, 36, 38, 41, 43, 46,
         48, 50, 53, 55, 58, 60, 62, 65, 67, 70, 72, 74, 77, 79, 82, 84, 86]
HELP1 = '''Grid map editor is used to define the grid of the music.
You can enter the grid by passing a row of values 
seperated by space on each line. The values are:
time-signature|amount-of-measures|grid-division|t-sig-visible-on-paper(1, 0, True or False)

"4/4 16 4 1" creates 16 measures of 4/4 time-signature with a grid-division of 
4 and the time-signature change is visible on the sheet.

You can create as many messages (one each line) as you want to form the grid.'''

HELP2 = '''System margin editor is used to be able to set
the margin for each individual line of music in the score.

You can enter a list of numbers(in mm) how much space you want around the lines
of music. For example "10" will apply 10 mm of space on both top and bottom sides
of the staff. 

If you enter one value it will apply to the current and all following lines. This means
you can enter multiple numbers for each line separately.'''

HELP3 = '''Measure division editor is used to define how many measures will be printed
in one system/line of music.

"4 3 5 4" will engrave 4 measures in the first system/line, 3 on the second system/line 
and so on...

If you enter one value it will apply to the current and all following lines. This means
you can enter multiple numbers for each line separately. The last integer in the list will
be applied until the end of the document.'''

HELP4 = '''Please enter three integers seperated by space:
measure-number-start, measure-number-end and transpose. 
example:3 5 12 will transpose all notes from the start of bar 3 to the 
end of bar 5, 12 semitones up. Use -12 to transpose one octave down.
Use 0 0 12 to select and transpose the whole file one octave up.
'''















# ---------------------
# save SaveFile structure
# ---------------------
'''
File structure: A *.pianoscript file 
is a json format file structure.
'''
SaveFile = {
  "header": {
    "title": {
      "text": "Untitled",
      "x-offset": 0,
      "y-offset": 0,
      "visible": True
    },
    "composer": {
      "text": "PianoScript",
      "x-offset": 0,
      "y-offset": 0,
      "visible": True
    },
    "copyright": {
      "text": "© PianoScript 2023",
      "x-offset": 0,
      "y-offset": 0,
      "visible": True
    },
    "app-name": "pianoscript",
    "app-version": 1.0
  },
  "properties": {
    "page-width": 210,
    "page-height": 297,
    "page-margin-left": 15,
    "page-margin-right": 15,
    "page-margin-up": 15,
    "page-margin-down": 15,
    "draw-scale": 0.75,
    "header-height":10,
    "footer-height":5,
    "measure-line-division": [
      4
    ],
    "line-margin": [
      10
    ],
    "grid": [
      {
        "amount": 8,
        "numerator": 4,
        "denominator": 4,
        "grid": 4,
        "visible": True
      }
    ]
  },
  "events": {
    "note": [],
    "text": [],
    "bpm": [],
    "slur": [],
    "pedal": []
  }
}
try:
    with open('template.pianoscript', 'r') as f:
        SaveFile = json.load(f)
except:
    with open('template.pianoscript', 'w') as f:
        f.write(json.dumps(SaveFile, separators=(',', ':'), indent=2))















#--------------------------------------
# Settings json load or create system |
#-------------------------------------

# the Settings variable is a json file the get's saves automatically to disk
# which contains all editor settings. (editor_settings.json)
# The TEMPLATE in the source code is used to create a template.pianoscript
# file in the same folder as editor_settings.json
Settings = {
"editor-x-zoom":35,
"editor-y-zoom":80,
"default-page-margin-left":10,
"default-page-margin-right":10,
"default-page-margin-up":10,
"default-page-margin-down":10,
"default-draw-scale":0.75
}
try:
    with open('editor_settings.json', 'r') as f:
        Settings = json.load(f)
except:
    with open('editor_settings.json', 'w') as f:
        f.write(json.dumps(Settings, separators=(',', ':'), indent=2))




















# --------------------------------------------------------
# TOOLS (notation design, help functions etc...)
# --------------------------------------------------------
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
    return round((x - (base / 2)) / base) * base


def x2tick_editor(mx):
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


def y2pitch_editor(y):
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


def time2x_editor(pianotick):
    '''
        This funtion converts pianotick
        to x position on the editor staff
    '''
    # calculate dimensions for staff (in px)
    editor_height = editor.winfo_height() - hbar.winfo_height()
    staff_y_margin = (editor_height - (y_scale_percent * editor_height)) / 2
    return staff_y_margin + (((x_scale_quarter_mm / 256) * MM) * pianotick)

def pitch2y_editor(pitch):
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

def barline_times(time_signatures):
    '''
        This function returns a list of
        times from every barline in the SaveFile.
    '''
    bl_times = []
    count = 0
    for grid in time_signatures:
        step = measure_length((grid['numerator'],grid['denominator']))
        for t in range(grid['amount']):
            bl_times.append(count)
            count += step
    return bl_times

def draw_note_pianoroll(note, cursor=False):
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
    x = time2x_editor(note['time'])
    x1 = time2x_editor(note['time'] + note['duration'])
    y = pitch2y_editor(note['pitch'])

    state = 'normal'
    note_color = color_notation_editor
    if cursor:
        state = 'disabled'
        note_color = 'black'# before it was blue

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
        bl_times = barline_times(SaveFile['properties']['grid'])
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
        bl_times = barline_times(SaveFile['properties']['grid'])
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
        update_connectstem(note,False,'r')
        update_connectstem(note,False,'l')
    
    update_drawing_order()


def update_connectstem(note, remove=False, hand='r'):
    # define x and y position on the editor canvas:
    # calculate dimensions for staff (in px)
    editor_height = editor.winfo_height() - hbar.winfo_height()
    staff_xy_margin = (editor_height - (y_scale_percent * editor_height)) / 2
    staff_height = editor_height - staff_xy_margin - staff_xy_margin
    y_factor = staff_height / 490
    x = time2x_editor(note['time'])
    
    # connect stems if two notes are starting at the same time
    buffer = []
    for evt in SaveFile['events']['note']:
        if evt['time'] == note['time'] and evt['pitch'] != note['pitch'] and evt['hand'] == hand:
            buffer.append(evt)
    if not remove and note['hand'] == hand:  buffer.append(note)
    buffer = sorted(buffer, key=lambda x: x['pitch'])
    tags = ['connectstem']
    for pos in buffer:
        tags.append(pos['id'])
    if len(buffer) > 1:
        editor.create_line(x,
            pitch2y_editor(buffer[0]['pitch']),
            x,
            pitch2y_editor(buffer[-1]['pitch']),
            width=2,
            fill=color_notation_editor,
            tag=tags)


def update_drawing_order():
    editor.tag_raise('midinote')
    editor.tag_raise('staffline')
    editor.tag_raise('notestop')
    editor.tag_raise('whitespace')
    editor.tag_raise('notehead')
    editor.tag_raise('whitedot')
    editor.tag_raise('blacknote')
    editor.tag_raise('blackdot')
    editor.tag_raise('stem')   
    editor.tag_raise('new')
    editor.tag_raise('connectstem')
    editor.tag_raise('cursor')
    


def note_split_processor(note):
    '''
    Returns a list of notes and if the note 
    crosses a barline it creates a note split.
    '''
    out = []

    # creating a list of barline positions.
    b_lines = barline_times(SaveFile['properties']['grid'])

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
                            'pitch': note['pitch'],
                            'time': start,
                            'duration': split_points[0] - start,
                            'hand': note['hand']})
            elif i == len(split_points):  # if last iteration
                out.append({'type': 'split',
                            'pitch': note['pitch'],
                            'time': split_points[i - 1],
                            'duration': end - split_points[i - 1],
                            'hand': note['hand'],})
                return out
            else:  # if not first and not last iteration
                out.append({'type': 'split', 'pitch': note['pitch'], 'time': split_points[i - 1],
                            'duration': split_points[i] - split_points[i - 1]})


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

def diff(x, y):
    if x >= y:
        return x - y
    else:
        return y - x























# ------------
# SMALL TOOLS
# ------------
def space_shift(event):
    '''
        This is a switch for mode 1 & 2
    '''
    if input_mode == 'right':
        mode_select(2)
    elif input_mode == 'left':
        mode_select(1)



def hover_switch(value):
    global mouse_hover_on_editor
    mouse_hover_on_editor = value



'''
    This part is taking care of updating the editor
    when resizing the window
'''
window_width, window_height = 0, 0
def resize(event):
    global window_width, window_height
    if event.widget == ".!panedwindow.!panedwindow":
        if (window_width != event.width) and (window_height != event.height):
            window_width, window_height = event.width,event.height
            print(f"The width of Toplevel is {window_width} and the height of Toplevel "
                  f"is {window_height}")



















# ------------------
# SaveFile management
# ------------------
file_changed = False
file_path = 'New'


def test_file():
    print('loading test file...')
    with open('template.pianoscript', 'r') as f:
        global SaveFile
        SaveFile = json.load(f)
        # run the piano-roll and print-view
        threading.Thread(target=draw_pianoroll).start()
        do_engrave('')
        root.title('PianoScript - %s' % f.name)

def new_file():
    global SaveFile, file_changed, file_path
    print('new_file')

    # check if user wants to save or cancel the task.
    if file_changed == True or file_path == 'New':
        ask = messagebox.askyesnocancel('Wish to save?', 'Do you wish to save the current SaveFile?', default='yes')
        if ask == True:# yes
            save()
        elif ask == False:# no
            ...
        elif ask == None:# cancel
            return

    file_changed = False

    # create new SaveFile
    print('creating new file...')
    with open('template.pianoscript', 'r') as f:
        SaveFile = json.load(f)

    # set window title
    root.title('PianoScript - New')
    file_path = 'New'

    # render pianoroll and printview
    threading.Thread(target=draw_pianoroll).start()
    do_engrave('')
    print('!!')


def load_file():
    print('load_file...')

    global SaveFile, file_changed, file_path

    # check if user wants to save or cancel the task.
    if file_changed == True:
        ask = messagebox.askyesnocancel('Wish to save?', 'Do you wish to save the current SaveFile?')
        if ask == True:
            save()
        elif ask == False:
            ...
        elif ask == None:
            return
    else:
        ...

    #global file_changed
    file_changed = False

    # open SaveFile
    f = filedialog.askopenfile(parent=root, 
        mode='Ur', 
        title='Open', 
        filetypes=[("PianoScript files", "*.pianoscript")])
    if f:
        with open(f.name, 'r') as f:
            fjson = json.load(f)
            try:
                if fjson['header']['app-name'] == 'pianoscript':
                    SaveFile = fjson
                else:
                    print('ERROR: file is not a pianoscript file.')
            except:
                print('ERROR: file is not a pianoscript file or is damaged.')

        # update file_path
        file_path = f.name

        # run the piano-roll and print-view
        threading.Thread(target=draw_pianoroll).start()
        do_engrave('')
        root.title('PianoScript - %s' % f.name)
    
    return


def save():
    print('save...')

    if file_path != 'New':
        f = open(file_path, 'w')
        f.write(json.dumps(SaveFile, separators=(',', ':'), indent=2))
        f.close()
    else:
        save_as() 


def save_as():
    print('save_as...')
    global file_path

    # save SaveFile
    f = filedialog.asksaveasfile(parent=root, 
        mode='w', 
        filetypes=[("PianoScript files", "*.pianoscript")],
        title='Save as...',
        initialdir='~/Desktop/')
    if f:
        root.title('PianoScript - %s' % f.name)
        f = open(f.name, 'w')
        f.write(json.dumps(SaveFile, separators=(',', ':'), indent=2))
        f.close()

        # update file_path
        file_path = f.name


def quit_editor(event='dummy'):
    print('quit_editor...')

    # check if user wants to save or cancel the task.
    if file_changed == True:
        ask = messagebox.askyesnocancel('Wish to save?', 'Do you wish to save the current file?')
        if ask == True:
            save()
        elif ask == False:
            ...
        elif ask == None:
            return
    else:
        ...
    # close thread
    print('**********************************')
    print('* http://www.pianoscript.org/ :) *')
    print('* Much Love From Philip Bergwerf *')
    print('**********************************')
    global program_is_running
    with thread_auto_render.condition:
        program_is_running = False
        thread_auto_render.condition.notify()
    thread_auto_render.join()

    # close program
    root.destroy()
















# -----------------
# variable storage
# -----------------

# render mechanics
needs_to_render = True
program_is_running = True

# piano-roll editor
x_scale_quarter_mm = 35 # 256 pianoticks == (...)mm on the screen
y_scale_percent = .75 # (...)% of canvas/screen height. (1 == 100%, 0.8 == 80% etc...)
total_pianoticks = 0
new_id = 0
edit_grid = 128
note_start_times = []
input_mode = 'right'
edit_cursor = (0,40)
hand = 'l'
mouse_hover_on_editor = False


# mouse edit
btn1_click = False
btn2_click = False
btn3_click = False
shift_key = False
ctl_key = False
alt_key = False
hold_id = ''





























def draw_pianoroll(event='event'):
    '''
        This function draws the pianoroll-view
        based on the SaveFile
    '''
    editor.delete('all')
    update_textboxes()

    global total_pianoticks, new_id, x_scale_quarter_mm, y_scale_percent

    x_scale_quarter_mm = Settings['editor-x-zoom']
    y_scale_percent = Settings['editor-y-zoom'] / 100
    
    # calculate total_pianoticks (staff length)
    total_pianoticks = 0
    for grid in SaveFile['properties']['grid']:
        ...
        total_pianoticks += (grid['amount'] * measure_length((grid['numerator'], grid['denominator'])))

    # calculate dimensions for staff (in px)
    root.update()
    editor_height = editor.winfo_height() - hbar.winfo_height()
    staff_y_margin = (editor_height - (y_scale_percent * editor_height)) / 2
    editor_x_margin = staff_y_margin # not sure
    staff_height = editor_height - staff_y_margin - staff_y_margin
    
    staff_x0 = editor_x_margin
    staff_x1 = editor_x_margin + (((x_scale_quarter_mm / 256) * MM) * total_pianoticks)
    staff_y0 = staff_y_margin
    staff_y1 = staff_y_margin + staff_height

    y_factor = staff_height / 490

    # DOC STAFF #
    x_curs = staff_x0
    measnum = 1
    for grid_msg in SaveFile['properties']['grid']:

        # draw time signature change
        if grid_msg['visible']:
            editor.create_text(x_curs,
                staff_y1+20,
                text=str(grid_msg['numerator'])+'/'+str(grid_msg['denominator']),
                font=('courier', 30, 'bold'),
                anchor='nw',
                fill='black')

        for meas in range(grid_msg['amount']):

            # draw barlines
            grid_size = ((x_scale_quarter_mm / 256) * MM) * measure_length(
                (grid_msg['numerator'], grid_msg['denominator']))
            editor.create_line(x_curs,
                staff_y0,
                x_curs,
                staff_y1,
                width=2,
                tag='staffline',
                fill=color_notation_editor,
                state='disabled')
            editor.create_text(x_curs,
                staff_y0,
                text=measnum,
                anchor='sw',
                fill=color_notation_editor,
                font=('courier', 30, 'bold'))

            # draw grid
            for grid in range(grid_msg['grid']):

                editor.create_line(x_curs,
                    staff_y0,
                    x_curs,
                    staff_y1,
                    width=1,
                    dash=(6,6),
                    tag='staffline',
                    fill=color_notation_editor,
                    state='disabled')

                x_curs += grid_size / grid_msg['grid']

            measnum += 1

    # draw endline
    editor.create_line(staff_x1,
        staff_y0,
        staff_x1,
        staff_y1,
        width=4,
        tag='staffline',
        fill=color_notation_editor,
        state='disabled')

    # draw staff-lines
    y_curs = staff_y0

    for staff in range(7):

        for line in range(3):
            editor.create_line(staff_x0,
                y_curs,
                staff_x1,
                y_curs,
                width=2,
                tag='staffline',
                fill=color_notation_editor,
                state='disabled')
            y_curs += 10 * y_factor

        y_curs += 10 * y_factor

        for line in range(2):
            if staff == 3:
                editor.create_line(staff_x0,
                    y_curs,
                    staff_x1,
                    y_curs,
                    width=1,
                    tag='staffline',
                    dash=(6,6),
                    fill=color_notation_editor,
                    state='disabled')
            else:
                editor.create_line(staff_x0,
                    y_curs,
                    staff_x1,
                    y_curs,
                    width=1,
                    tag='staffline',
                    fill=color_notation_editor,
                    state='disabled')
            y_curs += 10 * y_factor

        y_curs += 10 * y_factor

    editor.create_line(staff_x0,
        y_curs,
        staff_x1,
        y_curs,
        width=2,
        tag='staffline',
        fill=color_notation_editor,
        state='disabled')

    # DOC EVENTS

    # draw note events
    new_id = 0
    for note in SaveFile['events']['note']:
        note['id'] = 'note%i'%new_id
        draw_note_pianoroll(note)
        new_id += 1

    update_drawing_order()

    # update bbox
    _, _, bbox3, bbox4 = editor.bbox('all')
    editor.configure(scrollregion=(0, 0, bbox3 + editor_x_margin, bbox4 + staff_y_margin))




            



















def mouse_handling(event, event_type):
    '''
        In general this function covers all mouse_handling for
        the editor.

        The function is called on every mouse movement,
        button-click or button-release.
        event == event(containing x and y position)
        event_type == 'btn1click', 'btn1release', 'btn2click', 
        'btn2release', 'btn3click', 'btn3release' or 'motion'.
    '''
    global btn1_click, btn2_click, btn3_click, hold_id, hand
    global new_id, cursor_note, cursor_time, edit_cursor, file_changed

    editor.tag_lower('cursor')

    # first we keep track of the mouse buttons.
    if event_type == 'btn1click': btn1_click = True
    if event_type == 'btn2click': btn2_click = True
    if event_type == 'btn3click': btn3_click = True
    if event_type == 'btn1release': btn1_click = False
    if event_type == 'btn2release': btn2_click = False
    if event_type == 'btn3release': btn3_click = False

    # define mouse_x and mouse_y.
    m_x = editor.canvasx(event.x)
    m_y = editor.canvasy(event.y)

    if input_mode == 'right' or input_mode == 'left':

        '''
            This part defines what to do if we are
            in 'right-note-adding/editing-mode'.
        '''

        # we add a note when not clicking on an existing note with left-mouse-button:
        if event_type == 'btn1click':

            file_changed = True

            # delete cursor
            editor.delete('cursor')

            # Detecting if we are clicking a note
            tags = editor.gettags(editor.find_withtag('current'))
            editing = False
            if tags:    
                if 'note' in tags[0]:
                    editing = True
                    hold_id = tags[0]

            # if we are not editing we create a new note in SaveFile
            if not editing:
                ex = x2tick_editor(m_x)
                ey = y2pitch_editor(m_y)
                new_note = {
                    "id": 'note%i'%new_id,
                    "time": ex,
                    "duration": edit_grid,
                    "pitch": ey,
                    "hand": hand,
                    "x-offset": 0,
                    "y-offset": 0,
                    "stem-visible": True
                }
                draw_note_pianoroll(new_note)
                # write new_note to SaveFile
                SaveFile['events']['note'].append(new_note)
                # sort the events on the time key
                SaveFile['events']['note'] = sorted(SaveFile['events']['note'], key=lambda time: time['time'])
                hold_id = new_note['id']
                new_id += 1
            else:
                # update hand to current selected mode
                for evt in SaveFile['events']['note']:
                    if evt['id'] == hold_id:
                        evt['hand'] = hand
                        editor.delete(hold_id)
                        draw_note_pianoroll(evt)




        # if we release the left mouse button
        if event_type == 'btn1release':

            hold_id = ''

            '''RENDER CURSOR'''
            ex = x2tick_editor(m_x)
            ey = y2pitch_editor(m_y)
            cursor = {
                "id": 'cursor',
                "time": ex,
                "duration": edit_grid,
                "pitch": ey,
                "hand": hand,
                "x-offset": 0,
                "y-offset": 0,
                "stem-visible": True
            }
            draw_note_pianoroll(cursor,True)
            do_engrave('')
            edit_cursor = (ex,ey)



        # if we press the right mouse button we remove the selected note
        if event_type == 'btn3click':

            file_changed = True

            # Detecting if we are clicking a note
            note = editor.find_withtag('current')
            tags = editor.gettags(note)
            if tags:    
                if 'note' in tags[0]:
                    # in this case we are removing the selected note from editor and SaveFile
                    editor.delete(tags[0])
                    #editor.delete('stem'+tags[0][-1])
                    for evt,idx in zip(SaveFile['events']['note'],range(len(SaveFile['events']['note']))):
                        if evt['id'] == tags[0]:
                            #remove_note_editor(tags[0])
                            SaveFile['events']['note'].pop(idx)
                            update_connectstem(evt,True,'r')
                            update_connectstem(evt,True,'l')
                            break

            do_engrave('')




        # in motion mode we process the mouse movement
        if event_type == 'motion':

            if input_mode == 'right':
                hand = 'r'
            else:
                hand = 'l'

            if hold_id:
                '''EDITING NOTE'''
                # get event
                event = editor.find_withtag(hold_id)
                if event:
                    # write change to SaveFile
                    for evt in SaveFile['events']['note']:
                        if evt['id'] == hold_id:
                            mouse_time = x2tick_editor(m_x)
                            if mouse_time > evt['time']:
                                evt['duration'] = mouse_time - evt['time']
                            if mouse_time < evt['time']:
                                evt['pitch'] = y2pitch_editor(m_y)
                            draw_note_pianoroll(evt)
            
            else:
                '''RENDER CURSOR'''
                ex = x2tick_editor(m_x)
                ey = y2pitch_editor(m_y)
                cursor = {
                    "id": 'cursor',
                    "time": ex,
                    "duration": edit_grid,
                    "pitch": ey,
                    "hand": hand,
                    "x-offset": 0,
                    "y-offset": 0,
                    "stem-visible": True
                }
                draw_note_pianoroll(cursor,True)
                edit_cursor = (ex,ey)

    if input_mode == 'text':
        '''
            This part defines what to do if we are
            in 'text-adding-mode'.
        '''

        ...

    if input_mode == 'countline':
        '''
            This part defines what to do if we are
            in 'countline-adding-mode'.
        '''

        ...

    editor.tag_raise('cursor')














def keyboard_handling(event):

    ...














def midi_import():
    
    global SaveFile, new_id, file_changed
    with open('template.pianoscript', 'r') as f:
        SaveFile = json.load(f)
    SaveFile['properties']['grid'] = []
    SaveFile['events']['note'] = []
    SaveFile['events']['text'] = []
    SaveFile['events']['bpm'] = []
    SaveFile['events']['slur'] = []
    SaveFile['events']['pedal'] = []
    new_id = 0
    file_changed = False

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
            SaveFile['properties']['grid'].append(
                {'amount': amount, 'numerator': i['numerator'], 'denominator': i['denominator'],
                 'grid': gridno, 'visible': 1})
            count += 1

    # write notes
    for i in mesgs:
        if i['type'] == 'note_on' and i['channel'] == 0:
            SaveFile['events']['note'].append({'time': round(i['time']), 
                                            'duration': i['duration'], 
                                            'pitch': i['note'] - 20, 
                                            'hand': 'r', 
                                            'id':new_id})
            new_id += 1
        if i['type'] == 'note_on' and i['channel'] >= 1:
            SaveFile['events']['note'].append({'time': round(i['time']), 
                                            'duration': i['duration'], 
                                            'pitch': i['note'] - 20, 
                                            'hand': 'l', 
                                            'id':new_id})
            new_id += 1

    threading.Thread(target=draw_pianoroll).start()
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
                    y=rend * (SaveFile['properties']['page-height'] * MM), 
                    width=SaveFile['properties']['page-width'] * MM,
                    height=SaveFile['properties']['page-height'] * MM, 
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

    elif platform.system() == 'Windows':
        f = filedialog.asksaveasfile(mode='w', parent=root, filetypes=[("pdf SaveFile", "*.pdf")], initialfile=title,
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
                draw_pianoroll = subprocess.Popen(
                    f'''"{windowsgsexe}" -dQUIET -dBATCH -dNOPAUSE -dFIXEDMEDIA -sPAPERSIZE=a4 -dEPSFitPage -sDEVICE=pdfwrite -sOutputFile="{f.name}.pdf" {' '.join(pslist)}''',
                    shell=True)
                draw_pianoroll.wait()
                draw_pianoroll.terminate()
                for i in pslist:
                    os.remove(i.strip('"'))
                f.close()
                os.remove(f.name)
            except:
                messagebox.showinfo(title="Can't export PDF!",
                                    message='''Be sure you have selected a valid path in the default.pnoscript SaveFile. 
                                    You have to set the path+gswin64c.exe. 
                                    example: ~windowsgsexe{C:/Program Files/gs/gs9.54.0/bin/gswin64c.exe}''')

    do_engrave('')

















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
split_times = []
title = ''
composer = ''
copyright = ''
system_space = []
header_space = 50
paper_color = 0
view_page = 0

def draw_staff(y_cursor, mn, mx, page_margin_left,page_width,page_margin_right,color_black,draw_scale):
    def two(y):
        pview.create_line(page_margin_left,
            y,
            page_width - page_margin_right,
            y,
            fill=color_black,
            width=1*draw_scale)
        pview.create_line(page_margin_left,
            y+(10*draw_scale),
            page_width - page_margin_right,
            y+(10*draw_scale),
            fill=color_black,
            width=1*draw_scale)
    def three(y):
        pview.create_line(page_margin_left,
            y,
            page_width - page_margin_right,
            y,
            fill=color_black,
            width=2*draw_scale)
        pview.create_line(page_margin_left,
            y+(10*draw_scale),
            page_width - page_margin_right,
            y+(10*draw_scale),
            fill=color_black,
            width=2*draw_scale)
        pview.create_line(page_margin_left,
            y+(20*draw_scale),
            page_width - page_margin_right,
            y+(20*draw_scale),
            fill=color_black,
            width=2*draw_scale)
        
    def clef(y):
        pview.create_line(page_margin_left,
            y,
            page_width - page_margin_right,
            y,
            fill=color_black,
            width=1*draw_scale,
            dash=(6,6))
        pview.create_line(page_margin_left,
            y+(10*draw_scale),
            page_width - page_margin_right,
            y+(10*draw_scale),
            fill=color_black,
            width=1*draw_scale,
            dash=(6,6))

    # control flow for engraving the right composition of staff-lines
    keyline = 0
    if mx >= 81:
        three(0 + y_cursor)
        two((40 * draw_scale) + y_cursor)
        three((70 * draw_scale) + y_cursor)
        two((110 * draw_scale) + y_cursor)
        three((140 * draw_scale) + y_cursor)
        two((180 * draw_scale) + y_cursor)
        three((210 * draw_scale) + y_cursor)
        keyline = (250 * draw_scale)
    if mx >= 76 and mx <= 80:
        two(0 + y_cursor)
        three((30 * draw_scale) + y_cursor)
        two((70 * draw_scale) + y_cursor)
        three((100 * draw_scale) + y_cursor)
        two((140 * draw_scale) + y_cursor)
        three((170 * draw_scale) + y_cursor)
        keyline = (210 * draw_scale)
    if mx >= 69 and mx <= 75:
        three(0 + y_cursor)
        two((40 * draw_scale) + y_cursor)
        three((70 * draw_scale) + y_cursor)
        two((110 * draw_scale) + y_cursor)
        three((140 * draw_scale) + y_cursor)
        keyline = 180 * draw_scale
    if mx >= 64 and mx <= 68:
        two(0 + y_cursor)
        three((30 * draw_scale) + y_cursor)
        two((70 * draw_scale) + y_cursor)
        three((100 * draw_scale) + y_cursor)
        keyline = 140 * draw_scale
    if mx >= 57 and mx <= 63:
        three(0 + y_cursor)
        two((40 * draw_scale) + y_cursor)
        three((70 * draw_scale) + y_cursor)
        keyline = 110 * draw_scale
    if mx >= 52 and mx <= 56:
        two(0 + y_cursor)
        three((30 * draw_scale) + y_cursor)
        keyline = 70 * draw_scale
    if mx >= 45 and mx <= 51:
        three(0 + y_cursor)
        keyline = 40 * draw_scale

    clef(keyline + y_cursor)

    if mn >= 33 and mn <= 39:
        three(keyline + (30 * draw_scale) + y_cursor)
    if mn >= 28 and mn <= 32:
        three(keyline + (30 * draw_scale) + y_cursor)
        two(keyline + (70 * draw_scale) + y_cursor)
    if mn >= 21 and mn <= 27:
        three(keyline + (30 * draw_scale) + y_cursor)
        two(keyline + (70 * draw_scale) + y_cursor)
        three(keyline + (100 * draw_scale) + y_cursor)
    if mn >= 16 and mn <= 20:
        three(keyline + (30 * draw_scale) + y_cursor)
        two(keyline + (70 * draw_scale) + y_cursor)
        three(keyline + (100 * draw_scale) + y_cursor)
        two(keyline + (140 * draw_scale) + y_cursor)
    if mn >= 9 and mn <= 15:
        three(keyline + (30 * draw_scale) + y_cursor)
        two(keyline + (70 * draw_scale) + y_cursor)
        three(keyline + (100 * draw_scale) + y_cursor)
        two(keyline + (140 * draw_scale) + y_cursor)
        three(keyline + (170 * draw_scale) + y_cursor)
    if mn >= 4 and mn <= 8:
        three(keyline + (30 * draw_scale) + y_cursor)
        two(keyline + (70 * draw_scale) + y_cursor)
        three(keyline + (100 * draw_scale) + y_cursor)
        two(keyline + (140 * draw_scale) + y_cursor)
        three(keyline + (170 * draw_scale) + y_cursor)
        two(keyline + (210 * draw_scale) + y_cursor)
    if mn >= 1 and mn <= 3:
        three(keyline + (30 * draw_scale) + y_cursor)
        two(keyline + (70 * draw_scale) + y_cursor)
        three(keyline + (100 * draw_scale) + y_cursor)
        two(keyline + (140 * draw_scale) + y_cursor)
        three(keyline + (170 * draw_scale) + y_cursor)
        two(keyline + (210 * draw_scale) + y_cursor)
        pview.create_line(XYMARGIN + MARGIN, 
            (keyline + (240 * draw_scale) + y_cursor), 
            XYMARGIN + MARGIN + PRINTEAREA_WIDTH,
            (keyline + (240 * draw_scale) + y_cursor), 
            width=2)


def engrave(render_type, auto_scaling=True, renderer='pianoscript'):
    '''
        auto_scaling == the drawing gets scaled to the width of the printview.
        renderer == 'pianoscript' or 'klavarskribo'.
    '''

    # check if there is a time_signature in the SaveFile
    if not SaveFile['properties']['grid']:
        print('ERROR: There is no time signature in the SaveFile!')
        return

    # place all data in variables from SaveFile for cleaner code
    page_width = SaveFile['properties']['page-width'] * MM
    page_height = SaveFile['properties']['page-height'] * MM
    page_margin_left = SaveFile['properties']['page-margin-left'] * MM
    page_margin_right = SaveFile['properties']['page-margin-right'] * MM
    page_margin_up = SaveFile['properties']['page-margin-up'] * MM
    page_margin_down = SaveFile['properties']['page-margin-down'] * MM
    draw_scale = SaveFile['properties']['draw-scale']
    measure_line_division = SaveFile['properties']['measure-line-division']
    line_margin = SaveFile['properties']['line-margin']
    header_height = SaveFile['properties']['header-height'] * MM
    footer_height = SaveFile['properties']['footer-height'] * MM
    grid = SaveFile['properties']['grid']
    note = SaveFile['events']['note']
    text = SaveFile['events']['text']
    bpm = SaveFile['events']['bpm']
    slur = SaveFile['events']['slur']
    pedal = SaveFile['events']['pedal']
    title = SaveFile['header']['title']
    composer = SaveFile['header']['composer']
    copyright = SaveFile['header']['copyright']

    

    def read():
        '''
            read the music from SaveFile an place in the DOC list.
            DOC is an structured list with all events in it.
            structure: [pages[line[events]lines]pages]
            In the draw function we can easily loop over it
            to engrave the document.
        '''
        # data to collect:
        DOC = []
        page_spacing = []
        staff_heights = []

        # we add all events from SaveFile to the DOC list
        for note_evt in note:
            e = note_evt
            e['type'] = 'note'
            e = note_split_processor(e)
            for ev in e:
                DOC.append(ev)
        for text_evt in text:
            e = text_evt
            e['type'] = 'text'
            DOC.append(e)
        for bpm_evt in bpm:
            e = bpm_evt
            e['type'] = 'bpm'
            DOC.append(e)
        for slur_evt in slur:
            e = slur_evt
            e['type'] = 'slur'
            DOC.append(e)
        for pedal_evt in pedal:
            e = pedal_evt
            e['type'] = 'pedal'
            DOC.append(e)

        # now we sort the events on time-key
        DOC = sorted(DOC, key=lambda x: x['time'])

        # Now we organize the DOC object into a list of lines
        # We use the measure_line_division list to do that
        
        # we first need to get the split times from SaveFile
        bl_times = barline_times(grid)
        def split_bl_times(gridlst, measures_each_system):
            '''returns a list of the position of every new line/system of music.'''
            #gridlst = barline_pos_list(gridlst)
            linelist = [0]
            cntr = 0
            for barline in range(len(gridlst)):
                try: cntr += measures_each_system[barline]
                except IndexError:
                    cntr += measures_each_system[-1]
                try: linelist.append(gridlst[cntr])
                except IndexError:
                    linelist.append(gridlst[-1])
                    break
            if linelist[-1] == linelist[-2]:
                linelist.remove(linelist[-1])

            return linelist
        split_times = split_bl_times(barline_times(grid), measure_line_division)
        
        # now we split the DOC list into parts of lines
        DRAW2 = DOC
        DOC = []
        for _,spl in enumerate(split_times):
            buffer = []
            try: nxt = split_times[_+1]
            except IndexError: nxt = split_times[-1]
            for e in DRAW2:
                if e['time'] >= spl and e['time'] < nxt:
                    buffer.append(e)
            DOC.append(buffer)

        # now we have to calculate the amount of lines
        # that will fit on every page. We need to know 
        # the height of the staffs, and from layout settings
        # the margin around the staff.

        # we make a list that contains all staff heights
        for l in DOC:
            pitches = []
            for e in l:
                if e['type'] in ['note', 'split', 'invis']:
                    pitches.append(e['pitch'])
            try:
                staff_heights.append(staff_height(min(pitches),max(pitches),draw_scale))
            except ValueError:
                staff_heights.append(10*draw_scale)

        DOC.pop(-1)
        staff_heights.pop(-1)

        #print('staff_heights: ',staff_heights)

        # in this part we calculate how many systems fit on each page
        # also we gather the free space in the printarea in a list
        # called 'page_spacing'.
        DRAW2 = DOC
        DOC = []
        y_cursor = header_height
        printarea_height = (page_height - page_margin_up - page_margin_down)
        remaining_space = 0
        page = []
        for line, sh, c in zip(DRAW2,staff_heights, range(len(DRAW2))):
            try:
                lm = line_margin[c] * MM
            except IndexError:
                lm = line_margin[-1] * MM
            '''
                line = line of music
                sh = staff-height
                c = counter
                lm = line-margin
            '''
            y_cursor += (lm + sh + lm)
            # if the line fits on paper:
            if y_cursor <= printarea_height - header_height - footer_height:
                page.append(line)
                remaining_space = printarea_height - header_height - footer_height - y_cursor
            # if the line does NOT fit on paper:
            else:
                DOC.append(page)
                page = []
                page.append(line)
                page_spacing.append(remaining_space)
                y_cursor = lm + sh + lm 
                header = 0
            # if this is the last line:
            if c+1 == len(DRAW2):
                DOC.append(page)
                page_spacing.append(remaining_space)
                break
                    
        return DOC, page_spacing, staff_heights, split_times, bl_times

    DOC, page_spacing, staff_heights, split_times, bl_times = read()

    #------------------
    # debugging prints
    # print('page_spacing: ', page_spacing, '\nstaff_heights: ', len(staff_heights))
    
    # idxl = 0
    # for idxp, p in enumerate(DOC):
    #     print('new page:', idxp+1)
    #     for l in p:
    #         print('new line:', idxl+1)
    #         for e in l:
    #             print(e)
    #             ...
    #         idxl += 1
    #------------------
    
    def event_x_pos_engrave(pos, start_line_tick, end_line_tick):
        '''
        returns the x position on the paper.
        '''
        factor = interpolation(start_line_tick, end_line_tick, pos)
        return page_margin_left + ((page_width - page_margin_left - page_margin_right) * factor)

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

    def draw():
        '''
            I try to draw everything as efficient as possible from
            the ordered DOC list using many nested if/else flow.
            I found it the best way to draw.

            things we need to know/keep track on:
                - y_cursor
                - page_spacings
                - staff_heights
        '''
        # variables
        if render_type == 'export':
            color_black = 'black'
            color_white = 'white'
        else:
            color_black = color_basic_gui
            color_white = color_editor_canvas#inverted_color('#eee8d5')

        y_cursor = 0
        idx_l = 0
        for idx_p, page in enumerate(DOC):
            
            # draw paper
            if not render_type:
                pview.create_line(0,
                    y_cursor,
                    page_width,
                    y_cursor,
                    fill=color_black,
                    width=2,
                    dash=(6,4,5,2,3))

            # draw footer (page numbering, title and copyright notice
            pview.create_text(page_margin_left,
                y_cursor + page_height - page_margin_down,
                text='page ' + str(idx_p+1) + ' of ' + str(len(DOC)) + ' | ' + title['text'] + ' | ' + copyright['text'],
                anchor='sw',
                fill=color_black,
                font=('courier', round(12 * draw_scale), "normal"))

            y_cursor += page_margin_up

            if not idx_p: # if on the first page
                # draw header (title & composer text)
                pview.create_text(page_margin_left,
                    page_margin_up,
                    text=SaveFile['header']['title']['text'],
                    anchor='nw',
                    font=('courier', round(18 * draw_scale), "normal"),
                    fill=color_black)
                pview.create_text(page_width - page_margin_right,
                    page_margin_up,
                    text=SaveFile['header']['composer']['text'],
                    anchor='ne',
                    font=('courier', round(12 * draw_scale), "normal"),
                    fill=color_black)

                y_cursor += header_height
            
            for line in page:

                sh = staff_heights[idx_l]
                try: lm = line_margin[idx_l] * MM
                except: lm = line_margin[-1] * MM
                
                y_cursor += lm + (page_spacing[idx_p] / (len(DOC[idx_p])) / 2)

                # getting lowest and highest note in line
                mn, mx = 40, 44
                for obj in line:
                    
                    if obj['type'] in ['note', 'split', 'invis']:
                        
                        # calculating the highest and lowest note in the line
                        if mn >= obj['pitch']:
                            mn = obj['pitch']
                        if mx <= obj['pitch']:
                            mx = obj['pitch']

                for idx_o, obj in enumerate(line):
                    # barline and numbering
                    if obj['type'] == 'barline':
                        x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        pview.create_line(x,
                                          y_cursor,
                                          x,
                                          y_cursor + staffheight,
                                          width=2 * draw_scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill=color_black)
                        pview.create_text(x,
                                          y_cursor,
                                          text=b_counter,  # fix later TODO
                                          tag='grid',
                                          fill=color_black,
                                          font=('courier', round(12 * draw_scale), "normal"),
                                          anchor='sw')
                        b_counter += 1

                    # grid
                    if obj['type'] == 'grid-line':
                        x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        pview.create_line(x,
                                          y_cursor,
                                          x,
                                          y_cursor + staffheight,
                                          width=.5 * draw_scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill=color_black,
                                          dash=(6, 6))

                    # note start
                    if obj['type'] == 'note':

                        # define dimensions
                        x0 = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        x1 = event_x_pos_engrave(obj['time'] + obj['duration'], split_times[idx_l],
                                                 split_times[idx_l + 1])
                        y = note_y_pos(obj['pitch'], mn, mx, y_cursor, draw_scale)
                        y0 = y - (5 * draw_scale)
                        y1 = y + (5 * draw_scale)

                        # midinote
                        pview.create_polygon(x0,
                                             y,
                                             x0 + (5 * draw_scale),
                                             y - (5 * draw_scale),
                                             x1 - (5 * draw_scale),
                                             y - (5 * draw_scale),
                                             x1,
                                             y,
                                             x1 - (5 * draw_scale),
                                             y + (5 * draw_scale),
                                             x0 + (5 * draw_scale),
                                             y + (5 * draw_scale),
                                             fill=color_right_midinote,
                                             tag='midi_note',
                                             width=20 * draw_scale)
                        pview.create_line(x1,
                                          y - (5 * draw_scale),
                                          x1, y + (5 * draw_scale),
                                          width=2 * draw_scale,
                                          fill=color_black,
                                          tag=('midi_note','notestop'))

                        # left hand
                        if obj['hand'] == 'l':

                            # left stem and white space if on barline
                            pview.create_line(x0,
                                              y,
                                              x0,
                                              y + (25 * draw_scale),
                                              width=3 * draw_scale,
                                              tag='stem',
                                              fill=color_black)
                            for bl in bl_times:

                                if diff(obj['time'], bl) < 1:
                                    pview.create_line(x0,
                                                      y - (10 * draw_scale),
                                                      x0,
                                                      y + (30 * draw_scale),
                                                      width=2 * draw_scale,
                                                      tag='white_space',
                                                      fill=color_white)
                            # notehead
                            if obj['pitch'] in BLACK:

                                pview.create_oval(x0,
                                                  y0,
                                                  x0 + (5 * draw_scale),
                                                  y1,
                                                  tag='black_notestart',
                                                  fill=color_black,
                                                  outline=color_black,
                                                  width=2 * draw_scale)
                                # left dot black
                                pview.create_oval(x0 + (1.5 * draw_scale),
                                                  y + (1 * draw_scale),
                                                  x0 + (3.5 * draw_scale),
                                                  y - (1 * draw_scale),
                                                  tag='left_dot',
                                                  fill=color_white,
                                                  outline='')
                            else:
                                pview.create_oval(x0,
                                                  y0,
                                                  x0 + (10 * draw_scale),
                                                  y1,
                                                  tag='white_notestart',
                                                  fill=color_white,
                                                  outline=color_black,
                                                  width=2 * draw_scale)
                                # left dot white
                                pview.create_oval(x0 + (((10 / 2) - 1) * draw_scale),
                                                  y + (1 * draw_scale),
                                                  x0 + (((10 / 2) + 1) * draw_scale),
                                                  y - (1 * draw_scale),
                                                  tag='left_dot',
                                                  fill=color_black,
                                                  outline='')

                        # right hand
                        else:
                            # right stem and white space if on barline
                            pview.create_line(x0,
                                              y,
                                              x0,
                                              y - (25 * draw_scale),
                                              width=3 * draw_scale,
                                              tag='stem',
                                              fill=color_black)
                            for bl in bl_times:

                                if diff(obj['time'], bl) < 1:
                                    pview.create_line(x0,
                                                      y - (30 * draw_scale),
                                                      x0,
                                                      y + (10 * draw_scale),
                                                      width=2 * draw_scale,
                                                      tag='white_space',
                                                      fill=color_white)
                            # notehead
                            if obj['pitch'] in BLACK:

                                pview.create_oval(x0,
                                                  y0,
                                                  x0 + (5 * draw_scale),
                                                  y1,
                                                  tag='black_notestart',
                                                  fill=color_black,
                                                  outline=color_black,
                                                  width=2 * draw_scale)
                            else:
                                pview.create_oval(x0,
                                                  y0,
                                                  x0 + (10 * draw_scale),
                                                  y1,
                                                  tag='white_notestart',
                                                  fill=color_white,
                                                  outline=color_black,
                                                  width=2 * draw_scale)

                        # connect stems

                        for stem in line:

                            if stem['time'] == obj['time'] and stem['type'] == 'note' and stem['pitch'] != obj['pitch']:
                                if stem['time'] == obj['time'] and stem['hand'] == obj['hand']:
                                    stem_y = note_y_pos(stem['pitch'], mn, mx, y_cursor, draw_scale)
                                    pview.create_line(x0,
                                                      stem_y,
                                                      x0,
                                                      y,
                                                      width=3 * draw_scale,
                                                      capstyle='round',
                                                      tag='connect_stem',
                                                      fill=color_black)

                    # note active
                    if obj['type'] in ['note', 'split']:
                        x0 = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        x1 = event_x_pos_engrave(obj['time'] + obj['duration'], split_times[idx_l],
                                                 split_times[idx_l + 1])
                        y = note_y_pos(obj['pitch'], mn, mx, y_cursor, draw_scale)
                        pview.create_polygon(x0,
                                             y,
                                             x0 + (5 * draw_scale),
                                             y - (5 * draw_scale),
                                             x1 - (5 * draw_scale),
                                             y - (5 * draw_scale),
                                             x1,
                                             y,
                                             x1 - (5 * draw_scale),
                                             y + (5 * draw_scale),
                                             x0 + (5 * draw_scale),
                                             y + (5 * draw_scale),
                                             fill=color_right_midinote,
                                             tag='midi_note',
                                             width=20 * draw_scale)
                        pview.create_line(x1,
                                          y - (5 * draw_scale),
                                          x1, y + (5 * draw_scale),
                                          width=2 * draw_scale,
                                          fill=color_black,
                                          tag='midi_note')

                    # time signature text
                    if obj['type'] == 'time_signature_text':
                        x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        pview.create_text(x + (2.5 * draw_scale),
                                          y_cursor + staffheight + (20 * draw_scale),
                                          text=obj['text'],
                                          tag='tsigtext',
                                          anchor='w',
                                          font=('courier', round(12 * draw_scale), 'underline'),
                                          fill=color_black)

                    # text
                    if obj['type'] == 'text':
                        x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        y = note_y_pos(obj['pitch'], mn, mx, y_cursor, draw_scale)
                        t = pview.create_text(x,
                                              y,
                                              text=obj['text'],
                                              tag='text',
                                              anchor='w',
                                              font=('', round(12 * draw_scale), 'normal'),
                                              fill='black')
                        round_rectangle(pview, pview.bbox(t)[0],
                                        pview.bbox(t)[1],
                                        pview.bbox(t)[2],
                                        pview.bbox(t)[3],
                                        fill='white',
                                        outline='',
                                        width=.5,
                                        tag='textbg')

                    # count_line
                    if obj['type'] == 'count_line':
                        x = event_x_pos_engrave(obj['time'], 
                            split_times[idx_l], 
                            split_times[idx_l + 1])
                        y1 = note_y_pos(obj['note1'], mn, mx, y_cursor, draw_scale)
                        y2 = note_y_pos(obj['note2'], mn, mx, y_cursor, draw_scale)

                        pview.create_line(x,
                                          y1,
                                          x,
                                          y2,
                                          dash=(2, 2),
                                          tag='countline',
                                          fill=color_black,
                                          width=1*draw_scale)

                    # pedal
                #----------------------------------------

                # draw_staff is positioned up in the file because it's such a big function.
                # it needs a lot of variables to draw the staff properly.
                draw_staff(y_cursor,
                    mn,
                    mx,
                    page_margin_left,
                    page_width,
                    page_margin_right,
                    color_black,
                    draw_scale)

                # update y_cursor and divide the systems equal:
                y_cursor += sh + lm + (page_spacing[idx_p] / (len(DOC[idx_p])) / 2)

                idx_l += 1

            y_cursor = page_height * (idx_p + 1)


        # draw bottom line last page
        if not render_type:
            pview.create_line(0,
                y_cursor,
                page_width,
                y_cursor,
                fill=color_black,
                width=2,
                dash=(6,4,5,2,3,1))

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
        
        # make the new render update fluently and scale
        if not render_type == 'export':    
            root.update()
            s = pview.winfo_width() / page_width
            pview.scale("all", 0, 0, s, s)
        pview.move('all', 10000, 0)
        pview.delete('old')
        if not render_type == 'export':
            pview.configure(scrollregion=pview.bbox("all"))
        pview.addtag_all('old')

    draw()

    return len(DOC)


    

















def do_engrave(event='dummy'):
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
            engrave('')
        except Exception:  # as e:
            traceback.print_exc()


thread_auto_render = ThreadAutoRender()
thread_auto_render.start()















root.update()
window_width, window_height = root.winfo_width(), root.winfo_height()
def check_resize():
    global window_width, window_height
    if (window_width != root.winfo_width()) or (window_height != root.winfo_height()):
        window_width, window_height = root.winfo_width(),root.winfo_height()
        threading.Thread(target=draw_pianoroll()).start()
        do_engrave('')
    root.after(500,check_resize)
check_resize()
















# --------------
# editor tools |
# --------------

def set_base_color():
    
    def combine_hex_values(d):
        d_items = sorted(d.items())
        tot_weight = sum(d.values())
        red = int(sum([int(k[:2], 16)*v for k, v in d_items])/tot_weight)
        green = int(sum([int(k[2:4], 16)*v for k, v in d_items])/tot_weight)
        blue = int(sum([int(k[4:6], 16)*v for k, v in d_items])/tot_weight)
        zpad = lambda x: x if len(x)==2 else '0' + x
        return '#' + zpad(hex(red)[2:]) + zpad(hex(green)[2:]) + zpad(hex(blue)[2:])

    global color_basic_gui, color_editor_canvas
    color_basic_gui = colorchooser.askcolor(title ="Choose color")[1]
    #color_basic_gui = '#aaa000'
    color_editor_canvas = inverted_color(color_basic_gui)
    color1 = color_basic_gui
    color2 = color_editor_canvas
    color3 = combine_hex_values({color1[1:]: .5, color2[1:]: .5})
    print(color3)
    
    pview.configure(bg=color2)
    editor.configure(bg=color2)
    leftpanel.configure(bg=color3)

#set_base_color()

def set_value(t):
    global SaveFile, Settings

    # SaveFile settings
    if t == 'title':
        user_input = simpledialog.askstring(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=SaveFile['header']['title']['text'])
        if user_input: SaveFile['header'][t] = user_input
    elif t == 'composer':
        user_input = simpledialog.askstring(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=SaveFile['header']['composer']['text'])
        if user_input: SaveFile['header'][t] = user_input
    elif t == 'copyright':
        user_input = simpledialog.askstring(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=SaveFile['header']['copyright']['text'])
        if user_input: SaveFile['header'][t] = user_input
    elif t == 'page-width':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=SaveFile['properties']['page-width'])
        if user_input: SaveFile['properties'][t] = user_input
        else: SaveFile['properties'][t] = 210
    elif t == 'page-height':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=SaveFile['properties']['page-height'])
        if user_input: SaveFile['properties'][t] = user_input
        else: SaveFile['properties'][t] = 297
    elif t == 'page-margin-left':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=SaveFile['properties']['page-margin-left'])
        if user_input: SaveFile['properties'][t] = user_input
        else: SaveFile['properties'][t] = 10
    elif t == 'page-margin-right':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=SaveFile['properties']['page-margin-right'])
        if user_input: SaveFile['properties'][t] = user_input
        else: SaveFile['properties'][t] = 10
    elif t == 'page-margin-up':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=SaveFile['properties']['page-margin-up'])
        if user_input: SaveFile['properties'][t] = user_input
        else: SaveFile['properties'][t] = 10
    elif t == 'page-margin-down':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=SaveFile['properties']['page-margin-down'])
        if user_input: SaveFile['properties'][t] = user_input
        else: SaveFile['properties'][t] = 10
    elif t == 'draw-scale':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t}(1=default, 2=twice as big so from .5 to 1.5 is reasonable) for the document:', initialvalue=SaveFile['properties']['draw-scale'])
        if user_input: SaveFile['properties'][t] = user_input
        else: SaveFile['properties'][t] = 1
    elif t == 'header-height':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} in mm for the document:', initialvalue=SaveFile['properties']['header-height'])
        if user_input: SaveFile['properties'][t] = user_input
        else: SaveFile['properties'][t] = 15
    
    # editor Settings
    elif t == 'editor-x-zoom':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} from 0 to 100(or more) for the editor:', 
            initialvalue=Settings[t])
        if user_input: Settings[t] = user_input
        else: Settings[t] = 35
        with open('editor_settings.json', 'w') as f:
            f.write(json.dumps(Settings, separators=(',', ':'), indent=2))
    elif t == 'editor-y-zoom':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} (0.5 will make the staff height 50% of the editor view) for the editor:', initialvalue=Settings[t])
        if user_input: Settings[t] = user_input
        else: Settings[t] = 80
        with open('editor_settings.json', 'w') as f:
            f.write(json.dumps(Settings, separators=(',', ':'), indent=2))
    
    draw_pianoroll()
    do_engrave('')

def grid_selector(event='event'):
    global edit_grid
    value = ''

    for i in list_dur.curselection():
        value = list_dur.get(i)

    lengthdict = {1: 1024, 2: 512, 4: 256, 8: 128, 16: 64, 32: 32, 64: 16, 128: 8}
    edit_grid = ((lengthdict[float(value)] / eval(divide_spin.get())) * eval(times_spin.get()))

    root.focus()
    print('new grid: ', edit_grid)

def process_grid_map_editor():
    '''
        This function processes the grid map editor
        syntax and places it in the SaveFile.
    '''
    global SaveFile

    t = gridedit_text.get('1.0', 'end').split('\n')
    ignore = False

    SaveFile['properties']['grid'] = []

    for ts in t:

        numerator = None
        denominator = None
        amount = None
        grid = None
        visible = None

        if ts:
            try:
                numerator = eval(ts.split()[0].split('/')[0])
                denominator = eval(ts.split()[0].split('/')[1])
                amount = eval(ts.split()[1])
                grid = eval(ts.split()[2])
                visible = eval(ts.split()[3])
            except:
                print(
                    'Please read the documentation about how to provide the grid mapping correctly.\na correct gridmap:\n4/4 16 4 1')
                ignore = True
                break
        else:
            continue

        if ignore == True:
            return

        # gridmap add to SaveFile
        SaveFile['properties']['grid'].append(
            {'amount': amount, 'numerator': numerator, 'denominator': denominator,
             'grid': grid, 'visible': visible})

    draw_pianoroll()
    do_engrave('')
    update_textboxes()

def process_system_margin_editor():
    
    '''
        This function processes the system margin editor
        syntax and places it in the SaveFile.
    '''
    global SaveFile
    t = system_margin_text.get('1.0', 'end').split()
    if not t:
        print('EMPTY system margin editor; Default value "15" is used.')
        SaveFile['properties']['line-margin'] = [15]
        update_textboxes()
        return
    try: t = [float(x) for x in t]
    except:
        print('ERROR in system margin editor; please provide one or more floats in mm seperated by space. Default value "15" is used.')
        SaveFile['properties']['line-margin'] = [15]
        update_textboxes()
        return
    SaveFile['properties']['line-margin'] = t
    update_textboxes()
    do_engrave('')

def process_measure_line_division():
    
    '''
        This function processes the measure line division
        syntax and places it in the SaveFile.
    '''
    global SaveFile
    t = measureseachline_text.get('1.0', 'end').split()
    if not t:
        print('EMPTY measure line editor; Default value "4" is used.')
        SaveFile['properties']['measure-line-division'] = [4]
        update_textboxes()
        return
    try: t = [int(x) for x in t]
    except:
        print('ERROR in system margin editor; please provide one or more integers seperated by space. Default value "4" is used.')
        SaveFile['properties']['measure-line-division'] = [4]
        update_textboxes()
        return
    SaveFile['properties']['measure-line-division'] = t
    update_textboxes()
    do_engrave('')

def update_textboxes():
    '''
        This function updates the gui textboxes from SaveFile
    '''

    # grid map editor
    txt = ''
    for ts,idx in zip(SaveFile['properties']['grid'],range(len(SaveFile['properties']['grid']))):

        numerator = ts['numerator']
        denominator = ts['denominator']
        amount = ts['amount']
        grid_div = ts['grid']
        visible = ts['visible']

        if not idx == len(SaveFile['properties']['grid'])-1:
            txt += str(numerator) + '/' + str(denominator) + ' ' + str(amount) + ' ' + str(grid_div) + ' ' + str(visible) + '\n'
        else:
            txt += str(numerator) + '/' + str(denominator) + ' ' + str(amount) + ' ' + str(grid_div) + ' ' + str(visible)
    gridedit_text.delete('1.0','end')
    gridedit_text.insert('1.0', txt)

    # margin editor
    txt = ''
    for idx, marg in enumerate(SaveFile['properties']['line-margin']):
        add = '%g'%(marg)
        if idx > 0: txt += str(add) + ' '
        else: txt += str(add)
    system_margin_text.delete('1.0','end')
    system_margin_text.insert('1.0', txt)

    # measure line division
    txt = ''
    for mld in SaveFile['properties']['measure-line-division']:
        txt += str(mld) + ' '    
    measureseachline_text.delete('1.0','end')
    measureseachline_text.insert('1.0', txt)

def transpose():
    '''
        the user selects the range(from bar x to bar y) and
        gives a integer to transpose all notes in the selection.
    '''
    user_input = simpledialog.askstring('Transpose', HELP4)
    start = 0
    end = 0
    tr = 0
    if user_input:
        try:
            # reading user input
            user_input = user_input.split()
            start = int(user_input[0])
            end = int(user_input[1])
            tr = int(user_input[2])
            note = SaveFile['events']['note']
            grid = SaveFile['properties']['grid']
            bl_times = barline_times(grid)
            # transposing the selection
            for e in note:
                if not start or not end:
                    e['pitch'] += tr
                else:
                    m = 1
                    for blt in bl_times:
                        try: nxt = bl_times[m]
                        except IndexError: nxt = bl_times[-1]
                        if e['time'] >= blt and e['time'] < nxt:
                            break
                        m += 1
                    if m >= start and m <= end:
                        e['pitch'] += tr
            draw_pianoroll()
            do_engrave()
        except:
            print('ERROR in transpose function; please provide three integers. Action is ignored.')

    
            
    
















# --------------------------------------------------------
# MENU
# --------------------------------------------------------
menubar = Menu(root, relief='flat', bg=color_basic_gui, fg=color_editor_canvas, font=('courier', 14))
root.config(menu=menubar)
fileMenu = Menu(menubar, tearoff=0, bg=color_basic_gui, fg=color_editor_canvas, font=('courier', 14))
fileMenu.add_command(label='|new        |', command=new_file)
fileMenu.add_command(label='|load       |', command=load_file)
fileMenu.add_command(label='|save       |', command=save)
fileMenu.add_command(label='|save as... |', command=save_as)
fileMenu.add_separator()
fileMenu.add_command(label='|import midi|', command=midi_import)
fileMenu.add_separator()
fileMenu.add_command(label="|export ps  |", command=exportPostscript)
fileMenu.add_command(label="|export pdf |", command=exportPDF, underline=None)
fileMenu.add_command(label="|export midi|", command=exportPDF, underline=None)
fileMenu.add_separator()
fileMenu.add_command(label="|exit       |", underline=None, command=quit_editor)
menubar.add_cascade(label="|Menu|", underline=None, menu=fileMenu)
setMenu = Menu(menubar, tearoff=1, bg=color_basic_gui, fg=color_editor_canvas, font=('courier', 14))
setMenu.add_command(label='|title (string)               |', command=lambda: set_value('title'))
setMenu.add_command(label='|composer (string)            |', command=lambda: set_value('composer'))
setMenu.add_command(label='|copyright (string)           |', command=lambda: set_value('copyright'))
setMenu.add_separator()
setMenu.add_command(label='|draw scale (0.3-2.5)         |', command=lambda: set_value('draw-scale'))
setMenu.add_command(label='|page width (mm)              |', command=lambda: set_value('page-width'))
setMenu.add_command(label='|page height (mm)             |', command=lambda: set_value('page-height'))
setMenu.add_command(label='|header height (mm)           |', command=lambda: set_value('header-height'))
setMenu.add_command(label='|page margin left (mm)        |', command=lambda: set_value('page-margin-left'))
setMenu.add_command(label='|page margin right (mm)       |', command=lambda: set_value('page-margin-right'))
setMenu.add_command(label='|page margin up (mm)          |', command=lambda: set_value('page-margin-up'))
setMenu.add_command(label='|page margin down (mm)        |', command=lambda: set_value('page-margin-down'))
setMenu.add_separator()
setMenu.add_command(label='|editor x zoom (0-100 or more)|', command=lambda: set_value('editor-x-zoom'))
setMenu.add_command(label='|editor y zoom (0-100)        |', command=lambda: set_value('editor-y-zoom'))
menubar.add_cascade(label="|Settings|", underline=None, menu=setMenu)
toolsMenu = Menu(menubar, tearoff=1, bg=color_basic_gui, fg=color_editor_canvas, font=('courier', 14))
toolsMenu.add_command(label='|redraw editor|', command=lambda: draw_pianoroll())
toolsMenu.add_command(label='|transpose    |', command=lambda: transpose())
menubar.add_cascade(label="|Tools|", underline=None, menu=toolsMenu)














# -------------
# MODE TOOLBAR
# -------------
def mode_select(mode):
    
    global input_mode


    if mode == 1:
        input_mode = 'right'
        input_right_button.configure(bg=color_highlight)
        input_left_button.configure(bg='#f0f0f0')
        txt_button.configure(bg='#f0f0f0')
        countline_button.configure(bg='#f0f0f0')
        cursor = {
            "id": 'cursor',
            "time": edit_cursor[0],
            "duration": edit_grid,
            "pitch": edit_cursor[1],
            "hand": 'r',
            "x-offset": 0,
            "y-offset": 0,
            "stem-visible": True
        }
        draw_note_pianoroll(cursor,True)
    elif mode == 2:
        input_mode = 'left'
        input_right_button.configure(bg='#f0f0f0')
        input_left_button.configure(bg=color_highlight)
        txt_button.configure(bg='#f0f0f0')
        countline_button.configure(bg='#f0f0f0')
        cursor = {
            "id": 'cursor',
            "time": edit_cursor[0],
            "duration": edit_grid,
            "pitch": edit_cursor[1],
            "hand": 'l',
            "x-offset": 0,
            "y-offset": 0,
            "stem-visible": True
        }
        draw_note_pianoroll(cursor,True)
    elif mode == 3:
        input_mode = 'text'
        input_right_button.configure(bg='#f0f0f0')
        input_left_button.configure(bg='#f0f0f0')
        txt_button.configure(bg=color_highlight)
        countline_button.configure(bg='#f0f0f0')
    elif mode == 4:
        input_mode = 'countline'
        input_right_button.configure(bg='#f0f0f0')
        input_left_button.configure(bg='#f0f0f0')
        txt_button.configure(bg='#f0f0f0')
        countline_button.configure(bg=color_highlight)
    else:
        ...

input_right_button.configure(command=lambda: [mode_select(1), mode_label.focus_force()])
input_left_button.configure(command=lambda: [mode_select(2), mode_label.focus_force()])
txt_button.configure(command=lambda: [mode_select(3), mode_label.focus_force()])
countline_button.configure(command=lambda: [mode_select(4), mode_label.focus_force()])























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
    # mac scroll
    editor.bind("<MouseWheel>", lambda event: editor.xview_scroll(-1 * event.delta, 'units'))
    pview.bind("<MouseWheel>", lambda event: pview.yview_scroll(-1 * event.delta, 'units'))
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
list_dur.bind('<<ListboxSelect>>', grid_selector)
divide_spin.configure(command=lambda: grid_selector())
#divide_spin.bind('<Return>', lambda event: grid_selector())
times_spin.configure(command=lambda: grid_selector())
#times_spin.bind('<Return>', lambda event: grid_selector())
applygrid_button.configure(command=process_grid_map_editor)
applyspace_button.configure(command=process_system_margin_editor)
applymeasures_button.configure(command=process_measure_line_division)
midpanel.bind('<ButtonRelease-1>', lambda event: do_engrave(event))
root.bind('<Key-1>', lambda e: mode_select(1))
root.bind('<Key-2>', lambda e: mode_select(2))
root.bind('<Key-3>', lambda e: mode_select(3))
root.bind('<Key-4>', lambda e: mode_select(4))
root.bind('<KeyPress-space>', space_shift)
root.bind('<KeyRelease-space>', space_shift)
root.option_add('*Dialog.msg.font', 'Courier 20')
help_button1.configure(command=lambda: messagebox.showinfo('Grid map editor help', HELP1))
help_button2.configure(command=lambda: messagebox.showinfo('System margin editor help', HELP2))
help_button3.configure(command=lambda: messagebox.showinfo('Measure division editor help', HELP3))
editor.bind('<Leave>', lambda e: editor.delete('cursor'))











if __name__ == '__main__':
    test_file()

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