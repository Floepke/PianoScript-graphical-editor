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
    PianoScript V1.0
    Futures:
        * midi import
        * 
'''

# -----
# TODO
# -----
'''
    * grouped notes
    * select cut copy paste
    * text
    * countline
    * midi export
'''

# ----------------------
# welcome text on start
# ----------------------
print('--------------------------------------------------')
print('| Welcome to PianoScript music notation! Look on |')
print('| http://www.pianoscript.org/manual.html to read |')
print('| the manual on how to use PianoScript software. |')
print('|                                                |')
print('| All terminal output can be sent to             |')
print('| philipbergwerf@gmail.com if you discovered a   |')
print('| bug or crash in the program.                   |')
print('|                                                |')
print('| Have fun! :)                                   |')
print('--------------------------------------------------')
print('')
print('--------------------------------------------------')
print('| PianoScript Version: 1.0                       |')
print('| Code by Philip Bergwerf                        |')
print('--------------------------------------------------')
print('')



# ------------------
# constants
# ------------------
QUARTER = 256
BLACK = [2, 5, 7, 10, 12, 14, 17, 19, 22, 24, 26, 29, 31, 34, 36, 38, 41, 43, 46,
         48, 50, 53, 55, 58, 60, 62, 65, 67, 70, 72, 74, 77, 79, 82, 84, 86]

# grid map editor
HELP1 = '''
Grid map editor is used to define the grid of the music.
You can enter the grid by passing a row of values 
seperated by <space> on each line. The values are:
time-signature, amount-of-measures, grid-division and 
timesignature-visible-on-paper (1, 0, True or False)

"4/4 16 4 1" creates 16 measures of 4/4 time-signature 
with a grid-division of 4 and the time-signature change 
is visible on the sheet.

You can create as many messages (one each line) as 
you want to form the grid.
'''

# transpose
HELP2 = '''Please enter three integers seperated by space:
measure-number-start, measure-number-end and transpose. 
example:3 5 12 will transpose all notes from the start of bar 3 to the 
end of bar 5, 12 semitones up. Use -12 to transpose one octave down.
Use 0 0 12 to select and transpose the whole file one octave up.'''

# insert measure
HELP3 = '''Please provide two integers: 'insert-at-start-measure-number' and 'amount-of-measures-to-insert'.
Use '0 12' to insert 12 measures to the end of the file.'''

HELP4 = '''Please provide two numbers seperated by <space>: 'line-margin-up-left' and 'line-margin-down-right':'''

# add quick line breaks
HELP5 = '''If you enter '4': It will place line-breaks in groups of 4 measures trough the entire file.
If you enter '4 3 5': It will place 4 measures on the first line, 3 at the second etc... and 
apply 5 for the rest of the document. Please provide one or more integers that describe the 
line-breaks in terms of measures:'''


# --------------------
# IMPORTS
# --------------------
from tkinter import Tk, Canvas, Menu, Scrollbar, messagebox, PanedWindow, PhotoImage
from tkinter import filedialog, Label, Spinbox, StringVar, Listbox, Text
from tkinter import simpledialog,colorchooser, font
import platform, subprocess, os, threading, json, traceback
from mido import MidiFile
from shutil import which
import tkinter.ttk as ttk
if platform.system() == 'Darwin':
    from tkmacosx import Button
else:
    from tkinter import Button

# imports from my own code :)
from imports.midiutils import *
from imports.savefilestructure import *
from imports.tools import *
from imports.pianorolleditor import *
from imports.tooltip import *
from imports.engraver_klavarskribo import *
from imports.engraver_pianoscript import *
from imports.grideditor import *
from imports.dialogs import *



# --------------------
# GUI
# --------------------
# colors
color_basic_gui = '#002B36'
color_right_midinote = Score['properties']['color-right-hand-midinote']
color_left_midinote = Score['properties']['color-left-hand-midinote']
color_editor_canvas = '#eee8d5'#d9d9d9#fdffd1
color_highlight = '#268bd2'#a6a832
color_notation_editor = '#002b66'
# root
root = Tk()
MM = root.winfo_fpixels('1m')
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
leftpanel = PanedWindow(panedmaster, relief='flat', bg=color_basic_gui, width=65)
panedmaster.add(leftpanel)
midpanel = PanedWindow(panedmaster, relief='flat', bg=color_basic_gui, orient='h', sashwidth=10)
panedmaster.add(midpanel)
toolbarpanel = PanedWindow(midpanel, relief='flat', bg=color_basic_gui)
midpanel.add(toolbarpanel)
# editor panel
root.update()
editorpanel = PanedWindow(midpanel, relief='groove', orient='h', bg=color_basic_gui, width=scrwidth / 3 * 1.75)
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
divide_spin = Spinbox(leftpanel, from_=1, to=99, bg=color_highlight, font=('', 15, 'normal'))
divide_spin.pack(fill='x')
div_spin = StringVar(value=1)
divide_spin.configure(textvariable=div_spin)
times_label = Label(leftpanel, text='×', font=("courier", 20, "bold"), bg=color_basic_gui, fg='white', anchor='w')
times_label.pack(fill='x')
times_spin = Spinbox(leftpanel, from_=1, to=99, bg=color_highlight, font=('', 15, 'normal'))
times_spin.pack(fill='x')
tim_spin = StringVar(value=1)
times_spin.configure(textvariable=tim_spin)
fill_label1 = Label(leftpanel, text='', bg=color_basic_gui, fg='white', anchor='w', font=("courier"))
fill_label1.pack(fill='x')

# mode knobs:
mode_label = Label(leftpanel, text='MODE:', bg=color_basic_gui, fg='white', anchor='w', font=("courier"))
mode_label.pack(fill='x')

input_right_button = Button(leftpanel, text='right', activebackground=color_highlight, bg=color_highlight)
input_right_button.pack(fill='x')
ir_photo = PhotoImage(file = r"icons/noteinput_R.png")
input_right_button.configure(image=ir_photo)
input_right_button_tooltip = Tooltip(input_right_button, text='Right hand note input/edit mode', wraplength=scrwidth)

input_left_button = Button(leftpanel, bg='#f0f0f0', activebackground=color_highlight)
input_left_button.pack(fill='x')
il_photo = PhotoImage(file = r"icons/noteinput_L.png")
input_left_button.configure(image=il_photo)
input_left_button_tooltip = Tooltip(input_left_button, text='Left hand note input/edit mode', wraplength=scrwidth)
fill_label9 = Label(leftpanel, text='', bg=color_basic_gui, fg='white', anchor='w', font=("courier"))
fill_label9.pack(fill='x')
linebreak_button = Button(leftpanel, text='linebreak', activebackground=color_highlight, bg='#f0f0f0')
linebreak_button.pack(fill='x')
lb_photo = PhotoImage(file = r"icons/linebreak.png")
linebreak_button.configure(image=lb_photo)
linebreak_button_tooltip = Tooltip(linebreak_button, text='Line-break input/edit mode', wraplength=scrwidth)

countline_button = Button(leftpanel, text='countline*', bg='#f0f0f0', activebackground=color_highlight)
countline_button.pack(fill='x')
cnt_photo = PhotoImage(file = r"icons/countline.png")
countline_button.configure(image=cnt_photo)
countline_button_tooltip = Tooltip(countline_button, text='Countline input/edit mode', wraplength=scrwidth)

txt_button = Button(leftpanel, text='text*', bg='#f0f0f0', activebackground=color_highlight)
txt_button.pack(fill='x')
txt_photo = PhotoImage(file = r"icons/text.png")
txt_button.configure(image=txt_photo)
txt_button_tooltip = Tooltip(txt_button, text='Text input/edit mode', wraplength=scrwidth)

slur_button = Button(leftpanel, text='slur*', bg='#f0f0f0', activebackground=color_highlight)
slur_button.pack(fill='x')
slr_photo = PhotoImage(file = "icons/slur.png")
slur_button.configure(image=slr_photo)
slur_button_tooltip = Tooltip(slur_button, text='Slur input/edit mode', wraplength=scrwidth)

# toolbarpanel --> grid
grid_map_editor_label = Label(toolbarpanel, text='GRID MAP EDITOR (?)', bg=color_basic_gui, fg='white', anchor='w', font=("courier"))
grid_map_editor_label.pack(fill='x')
grid_map_editor_tooltip = Tooltip(grid_map_editor_label, text=HELP1, wraplength=scrwidth)
gridedit_text = Text(toolbarpanel, bg='grey', height=6, font=("courier", 14))
gridedit_text.pack(fill='x')
applygrid_button = Button(toolbarpanel, text='Apply', anchor='w', font=("courier"))
applygrid_button.pack(fill='x')

# changes in ui for windows:
if platform.system() == 'Windows':
    mode_label.configure(font=("courier", 12))

def setting_screenwidth():
    
    return printpanel.winfo_width() / 3
root.update()
print(setting_screenwidth())



  





# ------------
# SMALL TOOLS
# ------------
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
# File management
# ------------------
file_changed = False
file_path = 'New'


def test_file():
    print('test_file...')
    with open('testfile.pianoscript', 'r') as f:
        global Score
        Score = json.load(f)
        # run the piano-roll and print-view
        do_pianoroll()
        do_engrave('')
        root.title('PianoScript - %s' % f.name)

def new_file(e=''):
    global Score, file_changed,file_path
    print('new_file')

    # check if user wants to save or cancel the task.
    if file_changed == True:
        ask = messagebox.askyesnocancel('Wish to save?', 'Do you wish to save the current Score?', default='yes')
        if ask == True:# yes
            save()
        elif ask == False:# no
            ...
        elif ask == None:# cancel
            return

    file_changed = False

    # create new Score
    print('creating new file...')
    with open('template.pianoscript', 'r') as f:
        Score = json.load(f)

    # set window title
    root.title('PianoScript - New')
    file_path = 'New'

    # render pianoroll and printview
    do_pianoroll()
    do_engrave()


def load_file(e=''):
    print('load_file...')

    global Score, file_changed, file_path

    # check if user wants to save or cancel the task.
    if file_changed == True:
        ask = AskYesNo(root, 'Wish to save?', 'Do you wish to save the current Score?').result
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

    # open Score
    f = filedialog.askopenfile(parent=root, 
        mode='Ur', 
        title='Open', 
        filetypes=[("PianoScript files", "*.pianoscript")])
    if f:
        with open(f.name, 'r') as f:
            fjson = json.load(f)
            try:
                if fjson['header']['app-name'] == 'pianoscript':
                    Score = fjson
                else:
                    print('ERROR: file is not a pianoscript file.')
            except:
                print('ERROR: file is not a pianoscript file or is damaged.')

        # update file_path
        file_path = f.name

        # run the piano-roll and print-view
        do_pianoroll()
        do_engrave()
        root.title('PianoScript - %s' % f.name)
    
    return


def save(e=''):
    print('save...')
    global file_changed

    if file_path != 'New':
        f = open(file_path, 'w')
        f.write(json.dumps(Score, separators=(',', ':')))#, indent=2))# publish
        f.close()
        file_changed = False
    else:
        save_as()


def save_as(e=''):
    print('save_as...')
    global file_path, file_changed

    # save Score
    f = filedialog.asksaveasfile(parent=root, 
        mode='w', 
        filetypes=[("PianoScript files", "*.pianoscript")],
        title='Save as...',
        initialdir='~/Desktop/')
    if f:
        root.title('PianoScript - %s' % f.name)
        f = open(f.name, 'w')
        f.write(json.dumps(Score, separators=(',', ':')))#, indent=2))# publish
        f.close()
        # update file_path
        file_path = f.name
        file_changed = False


def quit_editor(event='dummy'):
    print('quit_editor...')

    # check if user wants to save or cancel the task.
    if file_changed == True:
        ask = AskYesNo(root, 'Wish to save?', 'Do you wish to save the current Score?').result
        if ask == True:
            save()
        elif ask == False:
            ...
        elif ask == None:
            return

    print('')
    print('----------------------------------')
    print('| http://www.pianoscript.org/ :) |')
    print('| Much Love From Philip Bergwerf |')
    print('----------------------------------')
    # close thread
    global program_is_running
    with thread_auto_render.condition:
        thread_auto_render.program_is_running = False
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
renderpageno = 1

# piano-roll editor
x_scale_quarter_mm = 35 # 256 pianoticks == (...)mm on the screen
y_scale_percent = .75 # (...)% of canvas/screen height. (1 == 100%, 0.8 == 80% etc...)
last_pianotick = 0
new_id = 0
edit_grid = 128
input_mode = 'right'
edit_cursor = (0,40)
hand = 'l'
mouse_hover_on_editor = False
selection = None
active_selection = False
shiftbutton1click = False
selection_tags = []
selection_buffer = []
copycut_buffer = []
mouse_time = 0
ms_xy = [0,0]
new_slur = 0

# mouse edit
btn1_click = False
btn2_click = False
btn3_click = False
shift_key = False
ctl_key = False
alt_key = False
hold_id = ''





























def do_pianoroll(event='event'):
    '''
        This function draws the pianoroll-view
        based on the Score
    '''
    editor.delete('all')
    editor.create_text(0,0,
        text='Loading pianoroll...',
        fill='red',
        font=('courier', 30, 'bold'),
        tag='loading',
        anchor='nw')
    update_textbox()

    global last_pianotick, new_id, x_scale_quarter_mm, y_scale_percent

    x_scale_quarter_mm = 40 ##Publish
    y_scale_percent = 80 / 100 ##Publish
    
    # calculate last_pianotick (staff length)
    last_pianotick = 0
    for grid in Score['events']['grid']:
        ...
        last_pianotick += (grid['amount'] * measure_length((grid['numerator'], grid['denominator'])))

    # calculate dimensions for staff (in px)
    root.update()
    editor_height = editor.winfo_height() - hbar.winfo_height()
    staff_y_margin = (editor_height - (y_scale_percent * editor_height)) / 2
    editor_x_margin = staff_y_margin # not sure
    staff_height = editor_height - staff_y_margin - staff_y_margin
    
    staff_x0 = editor_x_margin
    staff_x1 = editor_x_margin + (((x_scale_quarter_mm / 256) * MM) * last_pianotick)
    staff_y0 = staff_y_margin
    staff_y1 = staff_y_margin + staff_height

    y_factor = staff_height / 490

    # DOC STAFF #
    x_curs = staff_x0
    measnum = 1
    for grid_msg in Score['events']['grid']:

        # draw time signature change
        if grid_msg['visible']:
            editor.create_text(x_curs+5,
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
                anchor='s',
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

    # update bbox
    _, _, bbox3, bbox4 = editor.bbox('all')
    editor.configure(scrollregion=(0, 0, bbox3 + editor_x_margin, bbox4 + staff_y_margin))

    # DOC EVENTS

    new_id = 0

    # draw note events
    for note in Score['events']['note']:
        note['id'] = 'note%i'%new_id
        draw_note_pianoroll(note, 
            False, 
            editor, 
            hbar, 
            y_scale_percent, 
            x_scale_quarter_mm, 
            MM, 
            color_notation_editor, 
            BLACK, 
            color_editor_canvas, 
            Score)
        new_id += 1

    # draw newline events
    for linebreak in Score['events']['line-break']:
        linebreak['id'] = 'linebreak%i'%new_id
        draw_linebreak_editor(linebreak,
            editor,
            hbar,
            y_scale_percent,
            x_scale_quarter_mm,
            MM,
            color_notation_editor,
            color_highlight)
        new_id += 1

    update_drawing_order_editor(editor)

    editor.delete('loading')

    




            



















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
    global hold_id, hand, new_id, cursor_note, cursor_time, edit_cursor, file_changed, new_slur
    global selection, shiftbutton1click, selection_tags, mouse_time, active_selection, ms_xy

    editor.tag_lower('cursor')

    # define mouse_x and mouse_y, event_x and event_y.
    mx = editor.canvasx(event.x)
    my = editor.canvasy(event.y)
    ex = x2tick_editor(mx, editor, hbar, y_scale_percent, x_scale_quarter_mm, last_pianotick, edit_grid, MM)
    ey = y2pitch_editor(my, editor, hbar, y_scale_percent)

    # if event_type == 'shiftbtn1click':
    #     shiftbutton1click = True
    #     print('default-draw-scale')
    if event_type == 'shiftbtn1release':
        shiftbutton1click = False

    if input_mode == 'right' or input_mode == 'left':

        '''
            This part defines what to do if we are
            in 'note-adding/editing-mode'.
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

            if not editing:
                # create a new note in Score

                add_ctrl_z()#experimental

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
                draw_note_pianoroll(new_note, 
                    False, 
                    editor, 
                    hbar, 
                    y_scale_percent, 
                    x_scale_quarter_mm, 
                    MM, 
                    color_notation_editor, 
                    BLACK, 
                    color_editor_canvas, 
                    Score,
                    True)
                # write new_note to Score
                Score['events']['note'].append(new_note)
                # sort the events on the time key
                Score['events']['note'] = sorted(Score['events']['note'], key=lambda time: time['time'])
                hold_id = new_note['id']
                new_id += 1
            else:
                # update hand to current selected mode
                for evt in Score['events']['note']:
                    if evt['id'] == hold_id:
                        evt['hand'] = hand
                        editor.delete(hold_id)
                        draw_note_pianoroll(evt, 
                            False, 
                            editor, 
                            hbar, 
                            y_scale_percent, 
                            x_scale_quarter_mm, 
                            MM, 
                            color_notation_editor, 
                            BLACK, 
                            color_editor_canvas, 
                            Score,
                            True)


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
                    # write change to Score
                    for evt in Score['events']['note']:
                        if evt['id'] == hold_id:
                            mx = x2tick_editor(mx, editor, hbar, y_scale_percent, x_scale_quarter_mm, last_pianotick, edit_grid, MM)
                            if mx > evt['time']:
                                evt['duration'] = mx - evt['time']
                            if mx < evt['time']:
                                evt['pitch'] = y2pitch_editor(my, editor, hbar, y_scale_percent)
                            draw_note_pianoroll(evt, 
                                False, 
                                editor, 
                                hbar, 
                                y_scale_percent, 
                                x_scale_quarter_mm, 
                                MM, 
                                color_notation_editor, 
                                BLACK, 
                                color_editor_canvas, 
                                Score,
                                True)

            else:
                '''RENDER CURSOR'''
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
                draw_note_pianoroll(cursor, 
                    True, 
                    editor, 
                    hbar, 
                    y_scale_percent, 
                    x_scale_quarter_mm, 
                    MM, 
                    color_notation_editor, 
                    BLACK, 
                    color_editor_canvas, 
                    Score,
                    True)
                edit_cursor = (ex,ey)


        if event_type == 'btn1release':

            hold_id = ''

            '''RENDER CURSOR'''
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
            draw_note_pianoroll(cursor, 
                True, 
                editor, 
                hbar, 
                y_scale_percent, 
                x_scale_quarter_mm, 
                MM, 
                color_notation_editor, 
                BLACK, 
                color_editor_canvas, 
                Score,
                True)
            do_engrave()
            edit_cursor = (ex,ey)


        # if we press the right mouse button we remove the selected note
        if event_type == 'btn3click':

            file_changed = True

            # Detecting if we are clicking a note
            note = editor.find_withtag('current')
            tags = editor.gettags(note)
            if tags:
                if 'note' in tags[0]:
                    # in this case we are removing the selected note from editor and Score
                    editor.delete(tags[0])
                    for idx,evt in enumerate(Score['events']['note']):
                        if evt['id'] == tags[0]:
                            Score['events']['note'].pop(idx)
                            update_connectstem(evt,editor,hbar,y_scale_percent,x_scale_quarter_mm,
                                MM,Score,color_notation_editor, True,'r')
                            update_connectstem(evt,editor,hbar,y_scale_percent,x_scale_quarter_mm,
                                MM,Score,color_notation_editor, True,'r')

            do_engrave()
            return

    if event_type == 'shiftbtn1click':

        # old selection: redraw previous selected notes/countlines; change to black again.
        for s in selection_tags:    
            for n in Score['events']['note']:
                if n['id'] == s:
                    draw_note_pianoroll(n, 
                        False, 
                        editor, 
                        hbar, 
                        y_scale_percent, 
                        x_scale_quarter_mm, 
                        MM, 
                        color_notation_editor, 
                        BLACK, 
                        color_editor_canvas, 
                        Score,
                        False)
                    update_drawing_order_editor(editor)

        # updating selection
        #if not ex >= last_pianotick:
        shiftbutton1click = True
        selection = {
            "time1":ex,
            "pitch1":ey,
            "time2":ex,
            "pitch2":ey,
            "x1":mx,
            "y1":my,
            "x2":mx,
            "y2":my
        }

    if event_type == 'motion':

        # draw time selector for indicating which point in time you are at with the mouse
        cursor = {
            "id":'timeselector',
            "time":ex
        }
        draw_linebreak_editor(cursor,
            editor,
            hbar,
            y_scale_percent,
            x_scale_quarter_mm,
            MM,
            color_notation_editor,
            color_highlight,
            True)

        if shiftbutton1click:
            if not ex >= last_pianotick:
                selection = {
                    "time1":selection['time1'],
                    "pitch1":selection['pitch1'],
                    "time2":ex,
                    "pitch2":ey,
                    "x1":selection['x1'],
                    "y1":selection['y1'],
                    "x2":mx,
                    "y2":my
                }
                draw_select_rectangle(selection, editor, hbar, 
                    y_scale_percent, x_scale_quarter_mm, MM)

        mouse_time = ex

    # if we release the shift key before releasing the left mouse button:
    if event_type == 'btn1release':
        editor.delete('selectionrectangle')
        shiftbutton1click = False

    if event_type == 'shiftbtn1release':

        editor.delete('selectionrectangle')
        
        if not ex >= last_pianotick:
            selection = {
                "time1":selection['time1'],
                "pitch1":selection['pitch1'],
                "time2":ex,
                "pitch2":ey,
                "x1":selection['x1'],
                "y1":selection['y1'],
                "x2":mx,
                "y2":my
            }    

            # new selection: make new selected notes/countlines blue and save the selection id to selection_tags
            editor.addtag_overlapping('selected', selection['x1'], selection['y1'], selection['x2'], selection['y2'])
            selection_tags = []
            for t in editor.find_withtag('selected'):
                tags = editor.gettags(t)
                if 'note' in tags[0] or 'countline' in tags[0]:
                    selection_tags.append(tags[0])
            editor.dtag('selected')
            selection_tags = list(dict.fromkeys(selection_tags))
            # making the selected note(s) blue:
            for s in selection_tags:    
                for n in Score['events']['note']:
                    if n['id'] == s:
                        draw_note_pianoroll(n, 
                            False, 
                            editor, 
                            hbar, 
                            y_scale_percent, 
                            x_scale_quarter_mm, 
                            MM, 
                            color_notation_editor, 
                            BLACK, 
                            color_editor_canvas, 
                            Score,
                            False,
                            True)
                        update_drawing_order_editor(editor)
                        break
                active_selection = True

    if input_mode == 'linebreak':
        '''
            This part defines what to do if we are
            in 'linebreak-adding-mode'.
        '''

        if event_type == 'btn1click':

            # it's not alowed to create a linebreak >= latest pianotick; we ignore this case
            if ex >= last_pianotick or ex <= 0:
                return
            # hold_id
            for lb in Score['events']['line-break']:
                if lb['time'] == ex:
                    hold_id = lb['id']


        if event_type == 'motion':

            # display the current mouse-linebreak-position:

            editor.delete('cursor')
            cursor = {
                "id":'cursor',
                "time":ex
            }
            draw_linebreak_editor(cursor,
                editor,
                hbar,
                y_scale_percent,
                x_scale_quarter_mm,
                MM,
                color_notation_editor,
                color_highlight,
                True)


        if event_type == 'btn1release':

            # it's not alowed to create a linebreak >= latest pianotick; we ignore this case
            # it's not alowed to create a linebreak <= latest pianotick; we ignore this case
            if ex >= last_pianotick or ex <= 0:
                if ex <= 0:
                    # edit the margins (after this scope break/return)
                    while True:
                        user_input = AskString(root, 'set margins for current line...', 
                            "Set the upper and lower margin of the line in mm.\n(starting at pianotick: 0)",
                            initialvalue=str(Score['events']['line-break'][0]['margin-up-left']) + ' ' + str(Score['events']['line-break'][0]['margin-down-right']))
                        if user_input.result is not None:
                            try:
                                user_input = user_input.result.split()
                                for idx, ui in enumerate(user_input):
                                    user_input[idx] = int(ui)
                                if len(user_input) < 2:
                                    raise Exception
                                break
                            except:
                                print('ERROR in set_margins; please provide two floats or integers seperated by space.')
                        else: 
                            hold_id = ''
                            file_changed = True
                            return
                    Score['events']['line-break'][0]['margin-up-left'] = user_input[0]
                    Score['events']['line-break'][0]['margin-down-right'] = user_input[1]
                    hold_id = ''
                    file_changed = True
                    do_engrave()
                hold_id = ''
                return
            if hold_id:
                # edit linebreak and all following linebreaks:
                old_lb_time = None
                old_lb_idx = None
                new_lb_time = ex
                diff_oldnew_lb = None
                for idx,lb in enumerate(Score['events']['line-break']):
                    if lb['id'] == hold_id:
                        old_lb_time = lb['time']
                        old_lb_idx = idx
                        diff_oldnew_lb = ex - old_lb_time
                        break
                for lb in Score['events']['line-break'][old_lb_idx:]:
                    if lb['id'] == hold_id:
                        # edit current linebreak time in Score
                        lb['time'] = ex
                        if old_lb_time == lb['time']:
                            # edit the margins (after this scope break/return)
                            while True:
                                user_input = AskString(root, 'set margins for current line...', 
                                    f"Set the upper and lower margin of the line in mm.\n(starting at tick: {lb['time']})",
                                    initialvalue=str(lb['margin-up-left']) + ' ' + str(lb['margin-down-right']))
                                if user_input.result is not None:
                                    try:
                                        user_input = user_input.result.split()
                                        for idx, ui in enumerate(user_input):
                                            user_input[idx] = float(ui)
                                        if len(user_input) < 2:
                                            raise Exception
                                        break
                                    except:
                                        print('ERROR in set_margins; please provide two floats or integers seperated by space.')
                                else: 
                                    hold_id = ''
                                    file_changed = True
                                    return
                            lb['margin-up-left'] = user_input[0]
                            lb['margin-down-right'] = user_input[1]
                            hold_id = ''
                            file_changed = True
                            break#/return
                        # edit all next linebreaks
                        for lb2 in Score['events']['line-break'][old_lb_idx:]:
                            if lb2['time'] > lb['time']:
                                lb2['time'] += diff_oldnew_lb
                                # redraw all next linebreaks
                                editor.delete(lb2['id'])
                                draw_linebreak_editor(lb2,
                                    editor,
                                    hbar,
                                    y_scale_percent,
                                    x_scale_quarter_mm,
                                    MM,
                                    color_notation_editor,
                                    color_highlight)
                                hold_id = ''
                                file_changed = True
                        # redraw linebreak on editor
                        editor.delete(lb['id'])
                        draw_linebreak_editor(lb,
                            editor,
                            hbar,
                            y_scale_percent,
                            x_scale_quarter_mm,
                            MM,
                            color_notation_editor,
                            color_highlight)
                        hold_id = ''
                        file_changed = True
                        break
            else:
                # add new linebreak
                new_linebreak = {
                    "id":'linebreak%i'%new_id,
                    "time":ex,
                    "margin-up-left":10,
                    "margin-down-right":10
                }
                new_id += 1
                draw_linebreak_editor(new_linebreak,
                    editor,
                    hbar,
                    y_scale_percent,
                    x_scale_quarter_mm,
                    MM,
                    color_notation_editor,
                    color_highlight)
                Score['events']['line-break'].append(new_linebreak)
            
            Score['events']['line-break'] = sorted(Score['events']['line-break'], key=lambda time: time['time'])

            # if linebreak time >= last pianotick; delete it from Score and editor
            for lb in Score['events']['line-break']:
                if lb['time'] >= last_pianotick or lb['time'] < 0:
                    Score['events']['line-break'].remove(lb)
                    editor.delete(lb['id'])

            do_engrave()
            return


        if event_type == 'btn3click':

            # remove linebreak

            # if the time == 0 we try to remove the first newline which is not allowed.
            # we need a minimum of one newline in a Score. Therefore we ignore this case.
            if not ex: return

            # remove linebreak if we clicked on it with the right mouse button:
            for lb in Score['events']['line-break']:
                if ex == lb['time']:
                    # remove linebreak from file
                    Score['events']['line-break'].remove(lb)
                    # remove linebreak from editor
                    editor.delete(lb['id'])
                    do_engrave()
                    file_changed = True
                    return

        

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

    if input_mode == 'slur':

        if event_type == 'btn1click':

            # xy points 
            ms_xy = [mx,my]

            new_slur = {
                "id":'slur%i'%new_id,
                "bezier-points":[[0,0],[0,0],[0,0],[0,0]],
                "width":7.5
            }
            new_id += 1
            
            # draw slur
            slur_editor(editor,
                new_slur['bezier-points'],
                new_slur['id'],
                Score['properties']['draw-scale'],
                new_slur['width'], 
                100, 
                False)

        if event_type == 'motion':

            if ms_xy[0]:
                # define middle two control points
                point1 = [ms_xy[0]+((mx-ms_xy[0])/10), ms_xy[1]+40]#((my-ms_xy[1])/10)]
                point2 = [ms_xy[0]+((mx-ms_xy[0])/10*9), ms_xy[1]+40]#((my-ms_xy[1])/10*9)]
                # draw slur
                slur_editor(editor,
                    [[ms_xy[0],ms_xy[1]],point1,point2,[mx,my]],
                    new_slur['id'],
                    Score['properties']['draw-scale'],
                    new_slur['width'],
                    100,
                    False)

        if event_type == 'btn1release':

            # save the slur to Score
            ms_xy = [0,0]

        if event_type == 'shiftbutton1click':

            ...

        if event_type == 'shiftbtn1release':

            ...

        if event_type == 'btn3click':

            # delete slur we clicked on from editor
            ...


    editor.tag_raise('cursor')














def keyboard_handling(event):

    ...














def midi_import():
    global file_changed

    # asking for save since we are creating a new file with the midifile in it.
    if file_changed == True:
        ask = messagebox.askyesnocancel('Wish to save?', 'Do you wish to save the current Score?', default='yes')
        if ask == True:# yes
            save()
        elif ask == False:# no
            ...
        elif ask == None:# cancel
            return

    midifile = filedialog.askopenfile(parent=root,
                                      mode='Ur',
                                      title='Open midi...',
                                      filetypes=[("MIDI files", "*.mid")])
    if midifile:
        print('midi_import...')
        global Score, new_id
        with open('template.pianoscript', 'r') as f:
            Score = json.load(f)
        Score['events']['grid'] = []
        Score['events']['note'] = []
        Score['events']['text'] = []
        Score['events']['bpm'] = []
        Score['events']['slur'] = []
        Score['events']['pedal'] = []
        Score['header']['title']['text'] = os.path.normpath(midifile.name).split(os.sep)[-1]
        new_id = 0

        # ---------------------------------------------
        # translate midi data to note messages with
        # the right start and stop (piano)ticks.
        # ---------------------------------------------
        mesgs = []
        mid = MidiFile(midifile.name)
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
                amount = int(round(i['duration'] / measure_length(tsig)))
                gridno = i['numerator']
                if tsig == '6/8':
                    gridno = 2
                if tsig == '12/8':
                    gridno = 4
                Score['events']['grid'].append(
                    {'amount': amount, 'numerator': i['numerator'], 'denominator': i['denominator'],
                     'grid': gridno, 'visible': 1})
                count += 1

        # write notes
        for i in mesgs:
            if i['type'] == 'note_on' and i['channel'] == 0:
                Score['events']['note'].append({'time': round(i['time']), 
                                                'duration': i['duration'], 
                                                'pitch': i['note'] - 20, 
                                                'hand': 'l', 
                                                'id':new_id,
                                                'stem-visible':True})
                new_id += 1
            if i['type'] == 'note_on' and i['channel'] >= 1:
                Score['events']['note'].append({'time': round(i['time']), 
                                                'duration': i['duration'], 
                                                'pitch': i['note'] - 20, 
                                                'hand': 'r', 
                                                'id':new_id,
                                                'stem-visible':True})
                new_id += 1

        threading.Thread(target=do_pianoroll).start()
        do_engrave()

















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

        f = filedialog.asksaveasfile(mode='w', parent=root, filetypes=[("pdf file", "*.pdf")], initialfile=Score['header']['title']['text'],
                                     initialdir='~/Desktop')
        if f:
            pslist = []
            if Score['properties']['engraver'] == 'pianoscript':
                numofpages = range(engrave_pianoscript('export',
                    renderpageno,
                    Score,
                    MM,
                    last_pianotick,
                    color_notation_editor,
                    color_editor_canvas,
                    pview,root,
                    BLACK))
            else:
                numofpages = range(engrave_klavarskribo('export',
                    renderpageno,
                    Score,
                    MM,
                    last_pianotick,
                    color_notation_editor,
                    color_editor_canvas,
                    pview,root,
                    BLACK))
            for rend in numofpages:
                pview.postscript(file=f"/tmp/tmp{rend}.ps", 
                    x=10000, 
                    y=rend * (Score['properties']['page-height'] * MM), 
                    width=Score['properties']['page-width'] * MM,
                    height=Score['properties']['page-height'] * MM, 
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
        f = filedialog.asksaveasfile(mode='w', parent=root, filetypes=[("pdf Score", "*.pdf")], initialfile=Score['properties']['title']['text'],
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
                    y=export * (Score['properties']['page-height'] * MM),
                    width=(Score['properties']['page-width'] * MM), 
                    height=(Score['properties']['page-height'] * MM), 
                    rotate=False,
                    fontmap='-*-Courier-Bold-R-Normal--*-120-*')
                pslist.append(str('"' + str(f.name) + str(counter) + '.ps' + '"'))
            try:
                do_pianoroll = subprocess.Popen(
                    f'''"{windowsgsexe}" -dQUIET -dBATCH -dNOPAUSE -dFIXEDMEDIA -sPAPERSIZE=a4 -dEPSFitPage -sDEVICE=pdfwrite -sOutputFile="{f.name}.pdf" {' '.join(pslist)}''',
                    shell=True)
                do_pianoroll.wait()
                do_pianoroll.terminate()
                for i in pslist:
                    os.remove(i.strip('"'))
                f.close()
                os.remove(f.name)
            except:
                messagebox.showinfo(title="Can't export PDF!",
                                    message='''Be sure you have selected a valid path in the default.pnoscript Score. 
                                    You have to set the path+gswin64c.exe. 
                                    example: ~windowsgsexe{C:/Program Files/gs/gs9.54.0/bin/gswin64c.exe}''')

    do_engrave()

















def exportPostscript():

    f = filedialog.asksaveasfile(mode='w', 
        parent=root, 
        filetypes=[("postscript file", "*.ps")], 
        initialfile=Score['properties']['title']['text'],
        initialdir='~/Desktop')

    if f:
        for export in range(engrave('export')):
            print('printing page ', export)
            pview.postscript(file=f"{f.name}{export}.ps", 
                colormode='gray', 
                x=10000, 
                y=export * (Score['properties']['page-width'] * MM),
                width=Score['properties']['page-width'] * MM, 
                height=Score['properties']['page-width'] * MM, 
                rotate=False,
                fontmap='-*-Courier-Bold-R-Normal--*-120-*')









def do_engrave(event='dummy', page=0):
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
        self.program_is_running = True

    def run(self):
        try:
            while True:
                self.wait_and_render()
        except QuitThread:
            pass

    def wait_and_render(self):
        with self.condition:
            if not self.program_is_running:
                raise QuitThread
            while not self.needs_to_render:
                self.condition.wait()
                if not self.program_is_running:
                    raise QuitThread
            self.needs_to_render = False
        try:
            # on this scope we call the render function based on engraver:
            if Score['properties']['engraver'] == 'pianoscript':
                engrave_pianoscript('',
                    renderpageno,
                    Score,
                    MM,
                    last_pianotick,
                    color_notation_editor,
                    color_editor_canvas,
                    pview,root,
                    BLACK)
            else:
                engrave_klavarskribo('',
                    renderpageno,
                    Score,
                    MM,
                    last_pianotick,
                    color_notation_editor,
                    color_editor_canvas,
                    pview,root,
                    BLACK)
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
        threading.Thread(target=do_pianoroll()).start()
        do_engrave()
    root.after(500,check_resize)
check_resize()
















# --------------
# editor tools |
# --------------
def set_value(t):
    global Score, Settings, file_changed

    # Score settings
    if t == 'title':
        user_input = AskString(root, 
            f'Set {t}...', 
            f'Please provide the {t} for the document:', 
            initialvalue=Score['header'][t]['text'])
        if user_input.result is not None: 
            Score['header'][t]['text'] = user_input.result
            file_changed = True
    elif t == 'composer':
        user_input = AskString(root, 
            f'Set {t}...', 
            f'Please provide the {t} for the document:', 
            initialvalue=Score['header'][t]['text'])
        if user_input.result is not None: 
            Score['header'][t]['text'] = user_input.result
            file_changed = True
    elif t == 'copyright':
        user_input = AskString(root, 
            f'Set {t}...', 
            f'Please provide the {t} for the document:', 
            initialvalue=Score['header'][t]['text'])
        if user_input.result is not None: 
            Score['header'][t]['text'] = user_input.result
            file_changed = True
    elif t == 'page-width':
        user_input = AskFloat(root,
            f'Set {t}...', 
            f'Please provide the {t} for the document:', 
            initialvalue=Score['properties'][t])
        if user_input.result is not None: 
            print(user_input.result)
            Score['properties'][t] = user_input.result
            file_changed = True
    elif t == 'page-height':
        user_input = AskFloat(root,
            f'Set {t}...', 
            f'Please provide the {t} for the document:', 
            initialvalue=Score['properties'][t])
        if user_input.result is not None: 
            Score['properties'][t] = user_input.result
            file_changed = True
    elif t == 'page-margin-left':
        user_input = AskFloat(root,
            f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=Score['properties'][t])
        if user_input.result is not None: 
            Score['properties'][t] = user_input.result
            file_changed = True
    elif t == 'page-margin-right':
        user_input = AskFloat(root,
            f'Set {t}...', 
            f'Please provide the {t} for the document:', 
            initialvalue=Score['properties'][t])
        if user_input.result is not None: 
            Score['properties'][t] = user_input.result
            file_changed = True
    elif t == 'page-margin-up':
        user_input = AskFloat(root,
            f'Set {t}...', 
            f'Please provide the {t} for the document:', 
            initialvalue=Score['properties'][t])
        if user_input.result is not None: 
            Score['properties'][t] = user_input.result
            file_changed = True
    elif t == 'page-margin-down':
        user_input = AskFloat(root,
            f'Set {t}...', 
            f'Please provide the {t} for the document:', 
            initialvalue=Score['properties'][t])
        if user_input.result is not None: 
            Score['properties'][t] = user_input.result
            file_changed = True
    elif t == 'draw-scale':
        user_input = AskFloat(root,
            f'Set {t}...', 
            f'Please provide the {t}(1=default, 2=twice as big so from .5 to 1.5 is reasonable) for the document:', 
            initialvalue=Score['properties'][t])
        if user_input.result is not None: 
            Score['properties'][t] = user_input.result
            file_changed = True
    elif t == 'header-height':
        user_input = AskFloat(root,
            f'Set {t}...', f'Please provide the {t} in mm for the document:', 
            initialvalue=Score['properties'][t])
        if user_input.result is not None: 
            Score['properties'][t] = user_input.result
            file_changed = True
    elif t == 'footer-height':
        user_input = AskFloat(root,
            f'Set {t}...', 
            f'Please provide the {t} in mm for the document:', 
            initialvalue=Score['properties'][t])
        if user_input.result is not None: 
            Score['properties'][t] = user_input.result
            file_changed = True
    elif t == 'color-right-hand-midinote':
        user_input = colorchooser.askcolor(Score['properties'][t])[1]
        if user_input: 
            Score['properties'][t] = user_input
            file_changed = True   
            do_pianoroll()
    elif t == 'color-left-hand-midinote':
        user_input = colorchooser.askcolor(Score['properties'][t])[1]
        if user_input: 
            Score['properties'][t] = user_input
            file_changed = True
            do_pianoroll()

    
    # editor Settings
    elif t == 'editor-x-zoom':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} from 0 to 100(or more) for the editor:', 
            initialvalue=Settings[t])
        if user_input: Settings[t] = user_input
        else: Settings[t] = 35
    elif t == 'editor-y-zoom':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} (50 will make the staff height 50% of the editor view) for the editor:', initialvalue=Settings[t])
        if user_input: Settings[t] = user_input
        else: Settings[t] = 80
    
    do_engrave()

listbox_value = 8
def grid_selector(event='event'):
    global edit_grid, listbox_value

    for idx,i in enumerate(list_dur.curselection()):
        listbox_value = list_dur.get(i)
    # if event != 'event':
    #     listbox_value = event.keysym
    #     list_dur.select_set(int(event.keysym)-1)# implementing shortcuts in progress

    lengthdict = {1: 1024, 2: 512, 4: 256, 8: 128, 16: 64, 32: 32, 64: 16, 128: 8}
    edit_grid = ((lengthdict[int(listbox_value)] / int(div_spin.get())) * int(tim_spin.get()))

    root.focus()

def process_grid_map_editor():
    '''
        This function processes the grid map editor
        syntax and places it in the Score.
    '''
    global Score, last_pianotick
    t = gridedit_text.get('1.0', 'end').split('\n')
    Score['events']['grid'] = []
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
                    '''Please read the documentation about how to provide the grid mapping correctly.
                    a correct gridmap:
                    4/4 16 4 1''')
                return
        else:
            continue
        # gridmap add to Score
        Score['events']['grid'].append(
            {'amount': amount, 'numerator': numerator, 'denominator': denominator,
             'grid': grid, 'visible': visible})
    # remove linebreaks from Score that are >= then last_pianotick
    last_pianotick = 0
    for grid in Score['events']['grid']:
        last_pianotick += (grid['amount'] * measure_length((grid['numerator'], grid['denominator'])))
    for lb in reversed(Score['events']['line-break']):
        if lb['time'] >= last_pianotick:
            print('!')
            Score['events']['line-break'].remove(lb)
    do_pianoroll()
    do_engrave()
    update_textbox()


def update_textbox():
    '''
        This function updates the gui textboxes from Score
    '''

    # grid map editor
    txt = ''
    for ts,idx in zip(Score['events']['grid'],range(len(Score['events']['grid']))):

        numerator = ts['numerator']
        denominator = ts['denominator']
        amount = ts['amount']
        grid_div = ts['grid']
        visible = ts['visible']

        if not idx == len(Score['events']['grid'])-1:
            txt += str(numerator) + '/' + str(denominator) + ' ' + str(amount) + ' ' + str(grid_div) + ' ' + str(visible) + '\n'
        else:
            txt += str(numerator) + '/' + str(denominator) + ' ' + str(amount) + ' ' + str(grid_div) + ' ' + str(visible)
    gridedit_text.delete('1.0','end')
    gridedit_text.insert('1.0', txt)

def transpose():
    '''
        the user selects the range(from bar x to bar y) and
        gives a integer to transpose all notes in the selection.
    '''
    user_input = simpledialog.askstring('Transpose', HELP2)
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
            note = Score['events']['note']
            grid = Score['events']['grid']
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
            do_pianoroll()
            do_engrave()
        except:
            print('ERROR in transpose function; please provide three integers. \nAction is ignored.')

def insert_measure():

    global Score
    user_input = simpledialog.askstring('Insert measure(s)', HELP3, initialvalue='0 1')
    
    if user_input:
        
        # validate user_input
        try:
            print(len(barline_times(Score['events']['grid'])))
            selection = int(user_input.split()[0])
            amount = int(user_input.split()[1])
            if selection >= len(barline_times(Score['events']['grid'])): raise Exception
            if amount < 0: raise Exception
        except:
            print('ERROR in add_measure; please provide two integer values seperated by <space>.\nAction is ignored')
            return

            # calculating the measure length of the current selection



def remove_measure():
    
    ...

def remove_notes():
    
    ...


def add_quick_linebreaks(e=''):
    
    global Score, new_id

    # get user input
    while True:
        user_input = AskString(root,
            'add quick line breaks...', 
            HELP5, 
            initialvalue='4')
        user_input = user_input.result
        if user_input:
            try:
                user_input = user_input.split()
                for idx, ui in enumerate(user_input):
                    user_input[idx] = int(ui)
                break
            except:
                print('ERROR in add_quick_linebreaks; please provide one or more integers seperated by <space>.')
        else:
            return

    # rewrite entire line-break list using the user input and delete all linebreak drawings
    for lb in Score['events']['line-break']:
        editor.delete(lb['id'])
    # add first linebreak
    new_linebreak = {
        "id":'linebreak',
        "time":0,
        "margin-up-left":10,
        "margin-down-right":10
    }
    draw_linebreak_editor(new_linebreak,
        editor,
        hbar,
        y_scale_percent,
        x_scale_quarter_mm,
        MM,
        color_notation_editor,
        color_highlight)
    Score['events']['line-break'] = [new_linebreak]
    new_id += 1
    
    bl_times = barline_times(Score['events']['grid'])
    c = 0
    uidx = 0
    for idx, bl in enumerate(bl_times[:-1]):
        try: ui = user_input[uidx]
        except IndexError: ui = user_input[-1]
        if c == ui:
            # add all new linebreaks
            new_linebreak = {
                "id":'linebreak%i'%new_id,
                "time":bl,
                "margin-up-left":10,
                "margin-down-right":10
            }
            new_id += 1
            draw_linebreak_editor(new_linebreak,
                editor,
                hbar,
                y_scale_percent,
                x_scale_quarter_mm,
                MM,
                color_notation_editor,
                color_highlight)
            Score['events']['line-break'].append(new_linebreak)
        c += 1
        if c > ui: 
            c = 1
            uidx += 1

    do_engrave()













# -------------
# MODE TOOLBAR
# -------------
def mode_select(mode,i_mode):
    
    global input_mode

    modes = [
    input_right_button,
    input_left_button,
    linebreak_button,
    txt_button,
    countline_button,
    slur_button
    ]

    for i,conf in enumerate(modes):
        if i == mode:
            conf.configure(bg=color_highlight)
        if not i == mode:
            conf.configure(bg='#f0f0f0')

    if mode == 0:
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
        draw_note_pianoroll(cursor, 
            True, 
            editor, 
            hbar, 
            y_scale_percent, 
            x_scale_quarter_mm, 
            MM, 
            color_notation_editor, 
            BLACK, 
            color_editor_canvas, 
            Score)
    elif mode == 1:
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
        draw_note_pianoroll(cursor, 
            True, 
            editor, 
            hbar, 
            y_scale_percent, 
            x_scale_quarter_mm, 
            MM, 
            color_notation_editor, 
            BLACK, 
            color_editor_canvas, 
            Score)

    input_mode = i_mode

input_right_button.configure(command=lambda: [mode_select(0,'right'), mode_label.focus_force()])
input_left_button.configure(command=lambda: [mode_select(1,'left'), mode_label.focus_force()])
linebreak_button.configure(command=lambda: [mode_select(2,'linebreak'), mode_label.focus_force()])
txt_button.configure(command=lambda: [mode_select(3,'countline'), mode_label.focus_force()])
countline_button.configure(command=lambda: [mode_select(4,'text'), mode_label.focus_force()])
slur_button.configure(command=lambda: [mode_select(5,'slur'), mode_label.focus_force()])

def space_shift(event):
    '''
        This is a switch for mode 1 & 2 (right and left)
    '''
    if input_mode in ['linebreak', 'select', 'text', 'countline']:
        mode_select(0,'right')
        return
    if input_mode == 'right':
        mode_select(1,'left')
    elif input_mode == 'left':
        mode_select(0,'right')










# -------------
# Control-z
# -------------
'''
    For ctrl-z i choose to make a copy of the entire file on every edit.
    When undo is called I can load the previous Score version. On every
    new edit the redo's are removed.
'''
CtlZ = [Score]
levels_of_undo = 100
current_undo_index = -1

def undo(event=''):
    print('undo...')
    
    global Score,current_undo_index
    succeed = False
    
    # first we try to do the undo
    try: 
        Score = CtlZ[current_undo_index]
        current_undo_index -= 1
        succeed = True
    except IndexError: 
        return

    # if the undo succeeded we redraw the editor and do_render()
    if succeed:
        do_engrave()
        threading.Thread(target=do_pianoroll()).start()

def redo(event=''):
    print('redo...')
    
    global Score,current_undo_index
    succeed = False
    
    # first we try to do the redo
    try:
        #current_undo_index += 1
        Score = CtlZ[current_undo_index]
        succeed = True
    except IndexError:
        return

    # if the undo succeeded we redraw the editor and do_render()
    if succeed:
        do_engrave()
        threading.Thread(target=do_pianoroll()).start()

def add_ctrl_z():
    #print('add_ctrl_z')
    
    global CtlZ,current_undo_index

    # delete all redo
    try:
        rm = False
        for z in reversed(CtlZ[current_undo_index:]):
            CtlZ.remove(z)#check if it works delete current
            rm = True
        if rm:
            current_undo_index = -1
    except IndexError:
        ...

    # add ctrl-z
    CtlZ.append(Score)

def empty_ctrl_z():
    
    global CtlZ
    CtlZ = []










def cycle_trough_pages(event):
    global renderpageno
    
    if platform.system() in ['Windows', 'Linux']:

        if event.num == 3:
            print('next page')
            renderpageno += 1
        if event.num == 2:
            print('all pages')
            renderpageno = 0

    elif platform.system() == 'Darwin':

        if event.num == 2:
            print('next page')
            renderpageno += 1
        if event.num == 3:
            print('all pages')
            renderpageno = 0


    if event.num == 1:
        print('previous page')
        renderpageno -= 1

    do_engrave()



# --------------------------------------------------------
# Cut Copy Paste
# --------------------------------------------------------
def cut_selection(e=''):
    print('cut...')
    global selection_buffer, active_selection, file_changed
    file_changed = True
    selection_buffer = []
    lowest_time_from_selection = 0
    lowest_assign = True
    for note in Score['events']['note']:
        if note['id'] in selection_tags:
            if lowest_assign:
                lowest_time_from_selection = note['time']
                lowest_assign = False
            note['time'] -= lowest_time_from_selection
            selection_buffer.append(note)
    for note in reversed(Score['events']['note']):
        if note['id'] in selection_tags:
            Score['events']['note'].remove(note)
            editor.delete(note['id'])
    do_engrave()
    active_selection = False

def copy_selection(e=''):
    if not active_selection:
        return
    print('copy...')
    global selection_buffer 
    selection_buffer = []
    lowest_time_from_selection = 0
    lowest_assign = True
    for note in Score['events']['note']:
        if note['id'] in selection_tags:
            if lowest_assign:
                lowest_time_from_selection = note['time']
                lowest_assign = False
            new = {
                "id":"note",
                "time":note['time']-lowest_time_from_selection,
                "duration":note['duration'],
                "pitch":note['pitch'],
                "hand":note['hand'],
                "stem-visible":note['stem-visible'],
                "type":note['type'],
                "notestop":note['notestop']
            }
            selection_buffer.append(new)

def paste_selection(e=''):
    print('paste...')
    global new_id, selection_buffer, file_changed
    file_changed = True
    for e in selection_buffer:
        if 'note' in e['id']:
            new = {
                "id":"note%i"%new_id,
                "time":mouse_time+e['time'],
                "duration":e['duration'],
                "pitch":e['pitch'],
                "hand":e['hand'],
                "stem-visible":e['stem-visible'],
                "type":e['type'],
                "notestop":e['notestop']
            }
            new_id += 1
            Score['events']['note'].append(new)
            draw_note_pianoroll(new,
                False, 
                editor, 
                hbar, 
                y_scale_percent, 
                x_scale_quarter_mm, 
                MM, 
                color_notation_editor, 
                BLACK, 
                color_editor_canvas, 
                Score)
            update_drawing_order_editor(editor)
    do_engrave()

def select_all(e=''):
    
    ...

def transpose_up(e=''):
    print('transpose_up')
    global new_id, selection_buffer
    mt = mouse_time
    print(selection_buffer)
    for e in selection_buffer:
        if 'note' in e['id']:
            print(e)
            e['pitch'] += 1
            draw_note_pianoroll(e,
                False, 
                editor, 
                hbar, 
                y_scale_percent, 
                x_scale_quarter_mm, 
                MM, 
                color_notation_editor, 
                BLACK, 
                color_editor_canvas, 
                Score,
                False,
                True)
            update_drawing_order_editor(editor)
    do_engrave()            



# --------------------------------------------------------
# MENU
# --------------------------------------------------------
menubar = Menu(root, relief='flat', bg=color_basic_gui, fg=color_editor_canvas, font=('courier', 14))
root.config(menu=menubar)
fileMenu = Menu(menubar, tearoff=0, bg=color_basic_gui, fg=color_editor_canvas, font=('courier', 14))
fileMenu.add_command(label='|new          [ctl+n]|', command=new_file)
fileMenu.add_command(label='|open         [ctl+o]|', command=load_file)
fileMenu.add_command(label='|save         [ctl+s]|', command=save)
fileMenu.add_command(label='|save as...   [alt+s]|', command=save_as)
fileMenu.add_separator()
fileMenu.add_command(label='|load midi    [ctl+m]|', command=midi_import)
fileMenu.add_separator()
fileMenu.add_command(label="|export ps           |", command=transpose)
fileMenu.add_command(label="|export pdf   [ctl+e]|", command=exportPDF)
fileMenu.add_command(label="|export midi*        |", command=lambda: midiexport(root,Score))
fileMenu.add_separator()
fileMenu.add_command(label="|exit                |", underline=None, command=quit_editor)
menubar.add_cascade(label="|Menu|", underline=None, menu=fileMenu)
selectionMenu = Menu(menubar, tearoff=0, bg=color_basic_gui, fg=color_editor_canvas, font=('courier', 14))
selectionMenu.add_command(label="|cut         [ctl+x]|", underline=None, command=cut_selection)
selectionMenu.add_command(label="|copy        [ctl+c]|", underline=None, command=copy_selection)
selectionMenu.add_command(label="|paste       [ctl+v]|", underline=None, command=paste_selection)
selectionMenu.add_separator()
selectionMenu.add_command(label="|select all  [ctl+a]|", underline=None, command=select_all)
menubar.add_cascade(label="|Selection|", underline=None, menu=selectionMenu)
setMenu = Menu(menubar, tearoff=1, bg=color_basic_gui, fg=color_editor_canvas, font=('courier', 14))
setMenu.add_command(label='|title (string)               |', command=lambda: set_value('title'))
setMenu.add_command(label='|composer (string)            |', command=lambda: set_value('composer'))
setMenu.add_command(label='|copyright (string)           |', command=lambda: set_value('copyright'))
setMenu.add_separator()
setMenu.add_command(label='|draw scale (0.3-2.5)         |', command=lambda: set_value('draw-scale'))
setMenu.add_command(label='|page width (mm)              |', command=lambda: set_value('page-width'))
setMenu.add_command(label='|page height (mm)             |', command=lambda: set_value('page-height'))
setMenu.add_command(label='|header height (mm)           |', command=lambda: set_value('header-height'))
setMenu.add_command(label='|footer height (mm)           |', command=lambda: set_value('footer-height'))
setMenu.add_command(label='|page margin left (mm)        |', command=lambda: set_value('page-margin-left'))
setMenu.add_command(label='|page margin right (mm)       |', command=lambda: set_value('page-margin-right'))
setMenu.add_command(label='|page margin up (mm)          |', command=lambda: set_value('page-margin-up'))
setMenu.add_command(label='|page margin down (mm)        |', command=lambda: set_value('page-margin-down'))
setMenu.add_command(label='|color right hand midinote    |', command=lambda: set_value('color-right-hand-midinote'))
setMenu.add_command(label='|color left hand midinote     |', command=lambda: set_value('color-left-hand-midinote'))
setMenu.add_separator()
setMenu.add_command(label='|editor x zoom (0-100 or more)|', command=lambda: set_value('editor-x-zoom'))
setMenu.add_command(label='|editor y zoom (0-100)        |', command=lambda: set_value('editor-y-zoom'))
menubar.add_cascade(label="|Settings|", underline=None, menu=setMenu)
toolsMenu = Menu(menubar, tearoff=1, bg=color_basic_gui, fg=color_editor_canvas, font=('courier', 14))
toolsMenu.add_command(label='|redraw editor        [ctl+r]|', command=lambda: do_pianoroll())
#toolsMenu.add_command(label='|transpose                   |', command=lambda: transpose())
toolsMenu.add_command(label='|add quick line breaks       |', command=lambda: add_quick_linebreaks())
toolsMenu.add_command(label='|transpose                   |', command=lambda: transpose())
menubar.add_cascade(label="|Tools|", underline=None, menu=toolsMenu)




# --------------------------------------------------------
# BIND (shortcuts)
# --------------------------------------------------------
root.bind('<Escape>', quit_editor)
editor.bind('<Motion>', lambda event: mouse_handling(event, 'motion'))
editor.bind('<Button-1>', lambda event: mouse_handling(event, 'btn1click'))
editor.bind('<ButtonRelease-1>', lambda event: mouse_handling(event, 'btn1release'))
if platform.system() == 'Linux' or platform.system() == 'Windows':
    editor.bind('<Double-Button-1>', lambda event: mouse_handling(event, 'double-btn1'))
    editor.bind('<Button-2>', lambda event: mouse_handling(event, 'btn2click'))
    editor.bind('<ButtonRelease-2>', lambda event: mouse_handling(event, 'btn2release'))
    editor.bind('<Button-3>', lambda event: mouse_handling(event, 'btn3click'))
    editor.bind('<ButtonRelease-3>', lambda event: mouse_handling(event, 'btn3release'))
    leftpanel.bind('<Button-3>', lambda e: do_popup(e, setMenu))
    pview.bind('<Button-1>', lambda e: cycle_trough_pages(e))
    pview.bind('<Button-3>', lambda e: cycle_trough_pages(e))
if platform.system() == 'Darwin':
    editor.bind('<Double-Button-1>', lambda event: mouse_handling(event, 'double-btn1'))
    editor.bind('<Button-3>', lambda event: mouse_handling(event, 'btn2click'))
    editor.bind('<ButtonRelease-3>', lambda event: mouse_handling(event, 'btn2release'))
    editor.bind('<Button-2>', lambda event: mouse_handling(event, 'btn3click'))
    editor.bind('<ButtonRelease-2>', lambda event: mouse_handling(event, 'btn3release'))
    leftpanel.bind('<Button-2>', lambda e: do_popup(e, setMenu))
    # mac scroll
    editor.bind("<MouseWheel>", lambda event: editor.xview_scroll(-1 * event.delta, 'units'))
    pview.bind("<MouseWheel>", lambda event: pview.yview_scroll(-1 * event.delta, 'units'))
    pview.bind('<Button-1>', lambda e: cycle_trough_pages(e))
    pview.bind('<Button-2>', lambda e: cycle_trough_pages(e))
# linux scroll
if platform.system() == 'Linux':
    editor.bind("<5>", lambda event: editor.xview('scroll', 1, 'units'))
    editor.bind("<4>", lambda event: editor.xview('scroll', -1, 'units'))
    pview.bind("<5>", lambda event: pview.yview('scroll', 1, 'units'))
    pview.bind("<4>", lambda event: pview.yview('scroll', -1, 'units'))
    divide_spin.bind("<5>", lambda event: divide_spin.xview('scroll', 1, 'units'))
    divide_spin.bind("<4>", lambda event: divide_spin.xview('scroll', -1, 'units'))
def function():
    pass
# windows scroll
if platform.system() == 'Windows':
    editor.bind("<MouseWheel>", lambda event: editor.xview('scroll', -round(event.delta / 120), 'units'))
    pview.bind("<MouseWheel>", lambda event: pview.yview('scroll', -round(event.delta / 120), 'units'))
list_dur.bind('<<ListboxSelect>>', grid_selector)
divide_spin.configure(command=lambda: grid_selector())
divide_spin.bind('<Return>', lambda event: grid_selector())
times_spin.configure(command=lambda: grid_selector())
times_spin.bind('<Return>', lambda event: grid_selector())
applygrid_button.configure(command=process_grid_map_editor)
midpanel.bind('<ButtonRelease-1>', lambda event: do_engrave(event))
root.bind('<space>', lambda e: space_shift(e))
root.option_add('*Dialog.msg.font', 'Courier 20')
editor.bind('<Leave>', lambda e: editor.delete('cursor'))
root.protocol("WM_DELETE_WINDOW", quit_editor)
editor.bind("<Shift-Button-1>", lambda event: mouse_handling(event, 'shiftbtn1click'))
editor.bind("<Shift-ButtonRelease-1>", lambda event: mouse_handling(event, 'shiftbtn1release'))
editor.bind('<Key-1>', grid_selector)
editor.bind('<Key-2>', grid_selector)
editor.bind('<Key-3>', grid_selector)
editor.bind('<Key-4>', grid_selector)
editor.bind('<Key-5>', grid_selector)
editor.bind('<Key-6>', grid_selector)
editor.bind('<Key-7>', grid_selector)
editor.bind('<Key-8>', grid_selector)
root.bind('<Control-z>', undo)
root.bind('<Control-Z>', redo)
root.bind('<Control-x>', cut_selection)
root.bind('<Control-c>', copy_selection)
root.bind('<Control-v>', paste_selection)
root.bind('<Control-a>', select_all)
root.bind('<Control-n>', new_file)
root.bind('<Control-o>', load_file)
root.bind('<Control-s>', save)
root.bind('<Alt-s>', save_as)
root.bind('<Control-r>', do_pianoroll)
root.bind('<Control-q>', add_quick_linebreaks)
root.bind('<Up>', transpose_up)


# fullscreen toggle
fscreen = False
def fullscreen(event):
    global fscreen
    if fscreen: 
        root.attributes('-fullscreen', False)
        fscreen = False
    else: 
        root.attributes('-fullscreen', True)
        fscreen = True
root.bind('<F11>', fullscreen)


if __name__ == '__main__':
    new_file()
    #test_file()
    root.mainloop()
