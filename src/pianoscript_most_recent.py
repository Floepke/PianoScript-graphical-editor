
# --------------------
# IMPORTS
# --------------------
from tkinter import Tk, Canvas, Menu, Scrollbar, messagebox, PanedWindow, Listbox, Text
from tkinter import filedialog, Frame, Entry, Label, Spinbox, StringVar, PhotoImage
from tkinter import simpledialog
import time, ast, platform, subprocess, os, sys, errno, math, threading, random, json
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
color_basic_gui = '#444444'
color_right_midinote = 'grey'
color_left_midinote = color_right_midinote
color_editor_canvas = 'white'#d9d9d9#fdffd1
color_highlight = '#03a1fc'#a6a832
color_notation_editor = 'black'
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
editorpanel = PanedWindow(midpanel, relief='groove', orient='h', bg=color_basic_gui, width=scrwidth)
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
pview = Canvas(printpanel, bg='white', relief='flat')
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
fill_label7 = Label(rightpanel, text='SYSTEM MARGIN EDITOR', bg=color_basic_gui, fg='white', anchor='w', font=("courier"))
fill_label7.pack(fill='x')
help_button2 = Button(rightpanel, text='?', font=("courier", 12, 'bold'))
help_button2.pack(fill='x')
systemspace_text = Text(rightpanel, bg='grey', height=6)
systemspace_text.pack(fill='x')
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
    returns true if z is in between x and y.
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
        times from every barline in the FILE.
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
    editor.delete('cursor')

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
        note_color = 'blue'

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
        bl_times = barline_times(FILE['properties']['grid'])
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
        bl_times = barline_times(FILE['properties']['grid'])
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
    for evt in FILE['events']['note']:
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
    editor.tag_raise('whitespace')
    editor.tag_raise('notestop')
    editor.tag_raise('notehead')
    editor.tag_raise('whitedot')
    editor.tag_raise('blacknote')
    editor.tag_raise('blackdot')
    editor.tag_raise('stem')   
    editor.tag_raise('new')
    editor.tag_raise('connectstem')
    editor.tag_raise('cursor')






















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
    #print(event.widget)
    if event.widget == ".!panedwindow.!panedwindow":
        if (window_width != event.width) and (window_height != event.height):
            window_width, window_height = event.width,event.height
            print(f"The width of Toplevel is {window_width} and the height of Toplevel "
                  f"is {window_height}")

    




















# ---------------------
# save FILE structure
# ---------------------
'''
File structure:
A *.pianoscript file is a json format file structure. Below
a the json structure with descriptive names.
'''

FILE = {
  "header": {
    "app-name": "pianoscript",
    "app-version": 1.0
  },
  "properties": {
    "title": {
      "text": "Tutorial",
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
      "text": "Copyrights reserved by Philip Bergwerf 2023",
      "x-offset": 0,
      "y-offset": 0,
      "visible": True
    },
    "page-width": 210,
    "page-height": 297,
    "page-margin-left": 50,
    "page-margin-right": 50,
    "page-margin-up": 50,
    "page-margin-down": 50,
    "draw-scale": 0.85,
    "measure-line-division": [
      4,
      3,
      5,
      4
    ],
    "line-margin": [
      40,
      50,
      75,
      60
    ],
    "grid": [
      {
        "amount": 1,
        "numerator": 1,
        "denominator": 4,
        "grid": 1,
        "visible": False
      },
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
    "note": [
      {
        "id": 0,
        "time": 0.0,
        "duration": 256.0,
        "pitch": 33,
        "hand": "r",
        "x-offset": 0,
        "y-offset": 0,
        "visible": True
      }
    ],
    "text": [
      {
        "id": 1,
        "text": "soft like a baby...",
        "anchor": "w",
        "bold": False,
        "italic": False,
        "underline": False,
        "time": 0,
        "note": 40,
        "x-offset": 0,
        "y-offset": 0,
        "visible": True
      }
    ],
    "bpm": [
      {
        "id": 2,
        "time": 0,
        "bpm": 120,
        "division": 4,
        "x-offset": 0,
        "y-offset": 0,
        "visible": True
      }
    ],
    "slur": [
      {
        "id": 3,
        "time": 0,
        "duration": 256,
        "note-a": 0,
        "note-b": 20,
        "note-c": 0,
        "visible": True
      }
    ],
    "pedal": [
      {
        "pressed": True,
        "id": 4,
        "time": 0,
        "x-offset": 0,
        "y-offset": 0,
        "visible": True
      }
    ]
  }
}



















# ------------------
# FILE management
# ------------------
file_changed = False
file_path = ''


def test_file():
    print('loading test file...')
    with open('pianoscript_files/pianoscript_newfile.pianoscript', 'r') as f:
        global FILE
        FILE = json.load(f)

        # run the piano-roll and print-view
        threading.Thread(target=draw_pianoroll).start()
        do_engrave('')
        root.title('PianoScript - %s' % f.name)

def new_file():
    print('new_file')
    
    # Check if user wants to save or cancel the task.
    if file_changed == True:
        ask = messagebox.askyesnocancel('Wish to save?', 'Do you wish to save the current FILE?')
        if ask == True:
            save_as()
        elif ask == False:
            ...
        else:
            return
    else:
        ...

    # Create new FILE
    print('creating new file...')
    global FILE
    FILE = {"header":{"title":{"text":"Untitled","x-offset":0,"y-offset":0,"visible":True},"composer":{"text":"PianoScript","x-offset":0,"y-offset":0,"visible":True},"copyright":{"text":"\u00a9 PianoScript 2023","x-offset":0,"y-offset":0,"visible":True},"app-name":"pianoscript","app-version":1.0},"properties":{"page-width":210,"page-height":297,"page-margin-left":50,"page-margin-right":50,"page-margin-up":50,"page-margin-down":50,"draw-scale":0.85,"measure-line-division":[4],"line-margin":[50],"grid":[{"amount":8,"numerator":4,"denominator":4,"grid":4,"visible":True}]},"events":{"note":[],"text":[],"bpm":[],"slur":[],"pedal":[]}}

    # Set window title
    root.title('PianoScript - New')
    file_path = 'New'


def load_file():
    print('load_file')

    # Check if user wants to save or cancel the task.
    if file_changed == True:
        ask = messagebox.askyesnocancel('Wish to save?', 'Do you wish to save the current FILE?')
        if ask == True:
            save_file()
        elif ask == False:
            ...
        else:
            return
    else:
        ...

    # open FILE
    f = filedialog.askopenfile(parent=root, 
        mode='Ur', 
        title='Open', 
        filetypes=[("PianoScript files", "*.pianoscript")])
    if f:
        with open(f.name, 'r') as f:
            fjson = json.load(f)
            try:
                if fjson['header']['app-name'] == 'pianoscript':
                    global FILE
                    FILE = fjson
                else:
                    print('ERROR: file is not a pianoscript file.')
            except:
                print('ERROR: file is not a pianoscript file or is damaged.')

        # update file_path
        global file_path
        file_path = f.name

        # run the piano-roll and print-view
        threading.Thread(target=draw_pianoroll).start()
        do_engrave('')
        root.title('PianoScript - %s' % f.name)
    
    return


def save():
    print('save')

    if file_changed == True or file_path == 'New':
        save_as()
        return
    else:
        f = open(file_path, 'w')
        f.write(json.dumps(FILE, separators=(',', ':')))
        f.close()


def save_as():
    print('save_as')

    # save FILE
    f = filedialog.asksaveasfile(parent=root, 
        mode='w', 
        filetypes=[("PianoScript files", "*.pianoscript")],
        title='Save as...',
        initialdir='~/Desktop/')
    if f:
        root.title('PianoScript - %s' % f.name)
        f = open(f.name, 'w')
        f.write(json.dumps(FILE, separators=(',', ':'), indent=2))
        f.close()

        # update file_path
        global file_path
        file_path = f.name


def quit_editor(event='dummy'):
    # close thread
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
        based on the FILE
    '''
    editor.delete('all')

    # calculate total_pianoticks (staff length)
    global total_pianoticks, new_id
    total_pianoticks = 0
    for grid in FILE['properties']['grid']:
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

    # DRAW STAFF #
    x_curs = staff_x0
    measnum = 1
    for grid_msg in FILE['properties']['grid']:

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




    # DRAW EVENTS

    # draw note events
    new_id = 0

    for note in FILE['events']['note']:

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
    global new_id, cursor_note, cursor_time, edit_cursor

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

            # Detecting if we are clicking a note
            tags = editor.gettags(editor.find_withtag('current'))
            editing = False
            if tags:    
                if 'note' in tags[0]:
                    editing = True
                    hold_id = tags[0]

            # if we are not editing we create a new note in FILE
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
                # write new_note to FILE
                FILE['events']['note'].append(new_note)
                # sort the events on the time key
                FILE['events']['note'] = sorted(FILE['events']['note'], key=lambda time: time['time'])
                hold_id = new_note['id']
                new_id += 1
            else:
                # update hand to current selected mode
                for evt in FILE['events']['note']:
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
            edit_cursor = (ex,ey)



        # if we press the right mouse button we remove the selected note
        if event_type == 'btn3click':

            # Detecting if we are clicking a note
            note = editor.find_withtag('current')
            tags = editor.gettags(note)
            if tags:    
                if 'note' in tags[0]:
                    # in this case we are removing the selected note from editor and FILE
                    editor.delete(tags[0])
                    #editor.delete('stem'+tags[0][-1])
                    for evt,idx in zip(FILE['events']['note'],range(len(FILE['events']['note']))):
                        if evt['id'] == tags[0]:
                            #remove_note_editor(tags[0])
                            FILE['events']['note'].pop(idx)
                            update_connectstem(evt,True,'r')
                            update_connectstem(evt,True,'l')
                            break




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
                    # write change to FILE
                    for evt in FILE['events']['note']:
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
    
    ...

















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
                                    message='''Be sure you have selected a valid path in the default.pnoscript FILE. 
                                    You have to set the path+gswin64c.exe. 
                                    example: ~windowsgsexe{C:/Program Files/gs/gs9.54.0/bin/gswin64c.exe}''')

















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
## variables ##


def engrave(auto_scaling=True, renderer='pianoscript'):
    ...

















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
            engrave()
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
    root.after(500,check_resize)
check_resize()

















def set_titles(t):
    ...

    do_engrave('')


def set_global_scale():
    ...

    do_engrave('')


def set_page_margins():
    ...

    do_engrave('')


def grid_selector(event='event'):
    global edit_grid
    value = ''

    for i in list_dur.curselection():
        value = list_dur.get(i)

    lengthdict = {1: 1024, 2: 512, 4: 256, 8: 128, 16: 64, 32: 32, 64: 16, 128: 8}
    edit_grid = ((lengthdict[eval(value)] / eval(divide_spin.get())) * eval(times_spin.get()))

    root.focus()
    print('new grid: ', edit_grid)


















# --------------------------------------------------------
# MENU
# --------------------------------------------------------
menubar = Menu(root, relief='flat', bg=color_basic_gui, fg='white', font=('courier', 14))
root.config(menu=menubar)

fileMenu = Menu(menubar, tearoff=0, bg=color_basic_gui, fg='white', font=('courier', 14))

fileMenu.add_command(label='new', command=new_file)
fileMenu.add_command(label='load', command=load_file)
fileMenu.add_command(label='save', command=None)
fileMenu.add_command(label='save as...', command=save_as)

fileMenu.add_separator()

fileMenu.add_command(label='import midi', command=midi_import)

fileMenu.add_separator()

fileMenu.add_command(label="export ps", command=exportPostscript)
fileMenu.add_command(label="export pdf", command=exportPDF, underline=None)
fileMenu.add_command(label="export midi", command=exportPDF, underline=None)

fileMenu.add_separator()

fileMenu.add_command(label="exit", underline=None, command=quit_editor)
menubar.add_cascade(label="File", underline=None, menu=fileMenu)

setMenu = Menu(menubar, tearoff=1, bg=color_basic_gui, fg='white', font=('courier', 14))
setMenu.add_command(label='title', command=lambda: set_titles('title'))
setMenu.add_command(label='composer', command=lambda: set_titles('composer'))
setMenu.add_command(label='copyright', command=lambda: set_titles('copyright'))
setMenu.add_separator()
setMenu.add_command(label='global scale', command=set_global_scale)
setMenu.add_command(label='page margins', command=set_page_margins)
menubar.add_cascade(label="Set", underline=None, menu=setMenu)

optionsMenu = Menu(menubar, tearoff=1, bg=color_basic_gui, fg='white', font=('courier', 14))
optionsMenu.add_command(label='redraw editor', command=lambda: draw_pianoroll())
menubar.add_cascade(label="Options", underline=None, menu=optionsMenu)














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
        editor.configure(cursor='none')
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
        editor.configure(cursor='none')
    elif mode == 3:
        input_mode = 'text'
        input_right_button.configure(bg='#f0f0f0')
        input_left_button.configure(bg='#f0f0f0')
        txt_button.configure(bg=color_highlight)
        countline_button.configure(bg='#f0f0f0')
        editor.configure(cursor='cross')
    elif mode == 4:
        input_mode = 'countline'
        input_right_button.configure(bg='#f0f0f0')
        input_left_button.configure(bg='#f0f0f0')
        txt_button.configure(bg='#f0f0f0')
        countline_button.configure(bg=color_highlight)
        editor.configure(cursor='cross')
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
    editor.bind("<MouseWheel>", lambda event: editor.xview_scroll(-1 * event.delta, 'units'))

list_dur.bind('<<ListboxSelect>>', grid_selector)
divide_spin.configure(command=lambda: grid_selector())
divide_spin.bind('<Return>', lambda event: grid_selector())
times_spin.configure(command=lambda: grid_selector())
times_spin.bind('<Return>', lambda event: grid_selector())

midpanel.bind('<ButtonRelease-1>', lambda event: do_engrave(event))

root.bind('<Key-1>', lambda e: mode_select(1))
root.bind('<Key-2>', lambda e: mode_select(2))
root.bind('<Key-3>', lambda e: mode_select(3))
root.bind('<Key-4>', lambda e: mode_select(4))

root.bind('<KeyPress-space>', space_shift)
root.bind('<KeyRelease-space>', space_shift)

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
