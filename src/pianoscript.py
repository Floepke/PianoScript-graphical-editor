'''
Copyright 2023 Philip Bergwerf

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
print('| PianoScript Version: 1.0.0                     |')
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


# --------------------
# IMPORTS
# --------------------
from tkinter import Tk, Canvas, Menu, Scrollbar, messagebox, PanedWindow, Listbox, Text
from tkinter import filedialog, Label, Spinbox, StringVar
from tkinter import simpledialog
import platform, subprocess, os, threading, json, traceback
from mido import MidiFile
from shutil import which
import tkinter.ttk as ttk
if platform.system() == 'Darwin':
    from tkmacosx import Button
else:
    from tkinter import Button

# my own messy imports haha :)
from imports.midiexport import *
from imports.drawstaff import *
import imports.savefilestructure, imports.loadsettings
from imports.savefilestructure import Score
from imports.loadsettings import Settings
from imports.tools import *
from imports.pianorolleditor import *
from imports.tooltip import *
# --------------------
# GUI
# --------------------
# colors
color_basic_gui = '#002B36'
color_right_midinote = '#999999'
color_left_midinote = color_right_midinote 
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
editorpanel = PanedWindow(midpanel, relief='groove', orient='h', bg=color_basic_gui, width=scrwidth-(scrwidth / 3 * 1.2))
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
mode_label = Label(leftpanel, text='MODE:', bg=color_basic_gui, fg='white', anchor='w', font=("courier"))
mode_label.pack(fill='x')
input_right_button = Button(leftpanel, text='right', activebackground=color_highlight, bg=color_highlight)
input_right_button.pack(fill='x')
input_left_button = Button(leftpanel, text='left', bg='#f0f0f0', activebackground=color_highlight)
input_left_button.pack(fill='x')
fill_label9 = Label(leftpanel, text='', bg=color_basic_gui, fg='white', anchor='w', font=("courier"))
fill_label9.pack(fill='x')
linebreak_button = Button(leftpanel, text='linebreak', activebackground=color_highlight, bg='#f0f0f0')
linebreak_button.pack(fill='x')
select_button = Button(leftpanel, text='*select', activebackground=color_highlight, bg='#f0f0f0')
select_button.pack(fill='x')
txt_button = Button(leftpanel, text='*text', bg='#f0f0f0', activebackground=color_highlight)
txt_button.pack(fill='x')
countline_button = Button(leftpanel, text='*countline', bg='#f0f0f0', activebackground=color_highlight)
countline_button.pack(fill='x')

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





    





# ------------
# SMALL TOOLS
# ------------
def space_shift(event):
    '''
        This is a switch for mode 1 & 2 (right and left)
    '''
    if input_mode == 'right':
        mode_select(1,'left')
    elif input_mode == 'left':
        mode_select(0,'right')



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
# Score management
# ------------------
file_changed = False
file_path = 'New'


def test_file():
    print('test_file...')
    with open('templatetest.pianoscript', 'r') as f:
        global Score
        Score = json.load(f)
        # run the piano-roll and print-view
        draw_pianoroll()
        do_engrave('')
        root.title('PianoScript - %s' % f.name)

def new_file():
    global Score, file_changed,file_path
    print('new_file...')

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
    with open('template.pianoscript', 'r') as f:
        Score = json.load(f)

    # set window title
    root.title('PianoScript - New')
    file_path = 'New'

    # render pianoroll and printview
    draw_pianoroll()
    do_engrave()


def load_file():
    print('load_file...')

    global Score, file_changed, file_path

    # check if user wants to save or cancel the task.
    if file_changed == True:
        ask = messagebox.askyesnocancel('Wish to save?', 'Do you wish to save the current Score?')
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
        draw_pianoroll()
        do_engrave()
        root.title('PianoScript - %s' % f.name)
    
    return


def save():
    print('save...')
    global file_changed

    if file_path != 'New':
        f = open(file_path, 'w')
        f.write(json.dumps(Score, separators=(',', ':')))
        f.close()
        file_changed = False
    else:
        save_as()


def save_as():
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
        f.write(json.dumps(Score, separators=(',', ':')))
        f.close()
        # update file_path
        file_path = f.name
        file_changed = False


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
renderpageno = 0

# piano-roll editor
x_scale_quarter_mm = 35 # 256 pianoticks == (...)mm on the screen
y_scale_percent = .75 # (...)% of canvas/screen height. (1 == 100%, 0.8 == 80% etc...)
total_pianoticks = 0
new_id = 0
edit_grid = 128
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

    global total_pianoticks, new_id, x_scale_quarter_mm, y_scale_percent

    x_scale_quarter_mm = Settings['editor-x-zoom']
    y_scale_percent = Settings['editor-y-zoom'] / 100
    
    # calculate total_pianoticks (staff length)
    total_pianoticks = 0
    for grid in Score['properties']['grid']:
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
    for grid_msg in Score['properties']['grid']:

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
            Score,
            color_right_midinote,
            color_left_midinote,
            False)
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
    global hold_id, hand, new_id, cursor_note, cursor_time, edit_cursor, file_changed

    editor.tag_lower('cursor')

    # define mouse_x and mouse_y, event_x and event_y.
    mx = editor.canvasx(event.x)
    my = editor.canvasy(event.y)
    ex = x2tick_editor(mx, editor, hbar, y_scale_percent, x_scale_quarter_mm, total_pianoticks, edit_grid, MM)
    ey = y2pitch_editor(my, editor, hbar, y_scale_percent)

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
                    color_right_midinote,
                    color_left_midinote,
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
                            color_right_midinote,
                            color_left_midinote,
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
                            mx = x2tick_editor(mx, editor, hbar, y_scale_percent, x_scale_quarter_mm, total_pianoticks, edit_grid, MM)
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
                                color_right_midinote,
                                color_left_midinote,
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
                    color_right_midinote,
                    color_left_midinote,
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
                color_right_midinote,
                color_left_midinote,
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
                            update_connectstem(evt,editor,hbar,y_scale_percent,x_scale_quarter_mm,MM,Score,color_notation_editor, True,'r')
                            update_connectstem(evt,editor,hbar,y_scale_percent,x_scale_quarter_mm,MM,Score,color_notation_editor, True,'r')

            do_engrave()
            return

    if input_mode == 'select':
        '''
            This part defines what to do if we are
            in 'select-mode'.
        '''

        ...

    if input_mode == 'linebreak':
        '''
            This part defines what to do if we are
            in 'newline-adding-mode'.
        '''

        if event_type == 'btn1click':


            # it's not alowed to create a linebreak >= latest pianotick; we ignore this case
            if ex >= total_pianoticks or ex <= 0:
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
            if ex >= total_pianoticks:
                return
            if hold_id:
                # edit linebreak | and all following linebreaks:
                old_lb_time = None
                old_lb_idx = None
                new_lb_time = ex
                for idx,lb in enumerate(Score['events']['line-break']):
                    if lb['id'] == hold_id:
                        old_lb_time = lb['time']
                        old_lb_idx = idx
                        diff_oldnew_lb = ex - old_lb_time
                        break
                for lb in Score['events']['line-break']:
                    if lb['id'] == hold_id:
                        # edit current linebreak time in Score
                        lb['time'] = ex
                        #Score['events']['line-break'] = sorted(Score['events']['line-break'], key=lambda time: time['time'])
                        if old_lb_time == lb['time']:
                            # edit the margins (after this scope break/return)
                            while True:
                                user_input = simpledialog.askstring('set margins for current line...', 
                                    HELP4, 
                                    initialvalue=str(lb['margin-up-left']) + ' ' + str(lb['margin-down-right']))
                                if user_input:
                                    try:
                                        user_input = user_input.split()
                                        for idx, ui in enumerate(user_input):
                                            user_input[idx] = float(ui)
                                        if len(user_input) < 2:
                                            raise Exception
                                        break
                                    except:
                                        print('ERROR in set_margins; please provide two floats or integers seperated by space.')
                                else: return
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
                    "margin-up-left":Settings['default-margin-up-left'],
                    "margin-down-right":Settings['default-margin-down-right']
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
                                      title='Open midi (experimental)...',
                                      filetypes=[("MIDI files", "*.mid")])
    if midifile:
        print('midi_import...')
        global Score, new_id
        with open('template.pianoscript', 'r') as f:
            Score = json.load(f)
        Score['properties']['grid'] = []
        Score['events']['note'] = []
        Score['events']['text'] = []
        Score['events']['bpm'] = []
        Score['events']['slur'] = []
        Score['events']['pedal'] = []
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
                Score['properties']['grid'].append(
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
                                                'id':new_id})
                new_id += 1
            if i['type'] == 'note_on' and i['channel'] >= 1:
                Score['events']['note'].append({'time': round(i['time']), 
                                                'duration': i['duration'], 
                                                'pitch': i['note'] - 20, 
                                                'hand': 'r', 
                                                'id':new_id})
                new_id += 1

        threading.Thread(target=draw_pianoroll).start()
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
            for rend in range(engrave('export')):
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












# --------------
# engraving
# --------------





def engrave(render_type, pageno=1, auto_scaling=True, renderer='pianoscript'):
    '''
        auto_scaling == the drawing gets scaled to the width of the printview.
        renderer == 'pianoscript' or 'klavarskribo'.
    '''

    if render_type == 'export':
        pageno = 0

    # check if there is a time_signature in the Score
    if not Score['properties']['grid']:
        print('ERROR: There is no time signature in the Score!')
        return

    # place all data in variables from Score for cleaner code
    page_width = Score['properties']['page-width'] * MM
    page_height = Score['properties']['page-height'] * MM
    p_marg_l = Score['properties']['page-margin-left'] * MM
    p_marg_r = Score['properties']['page-margin-right'] * MM
    p_marg_u = Score['properties']['page-margin-up'] * MM
    p_marg_d = Score['properties']['page-margin-down'] * MM
    draw_scale = Score['properties']['draw-scale']
    measure_line_division = Score['properties']['measure-line-division']
    line_break = Score['events']['line-break']
    line_margin = Score['properties']['line-margin']
    header_h = Score['properties']['header-height'] * MM
    footer_h = Score['properties']['footer-height'] * MM
    grid = Score['properties']['grid']
    note = Score['events']['note']
    text = Score['events']['text']
    bpm = Score['events']['bpm']
    slur = Score['events']['slur']
    pedal = Score['events']['pedal']
    title = Score['header']['title']
    composer = Score['header']['composer']
    copyright = Score['header']['copyright']
    minipiano = Score['properties']['minipiano']


    

    def read():
        '''
            read the music from Score an place in the DOC list.
            DOC is an structured list with all events in it.
            structure: [pages[line[events]lines]pages]
            In the draw function we can easily loop over it
            to engrave the document.
        '''
        # data to collect:
        DOC = []
        page_spacing = []
        staff_heights = []
        t_sig_map = []

        # time_signature
        bln_time = 0
        grd_time = 0
        for idx,g in enumerate(Score['properties']['grid']):
            t_sig_map.append(g)
            # barline and grid messages
            meas_len = measure_length((g['numerator'], g['denominator']))
            grid_len = meas_len / g['grid']
            for meas in range(0, g['amount']):
                DOC.append({'type': 'barline', 'time': bln_time})
                DOC.append({'type': 'endoflinebarline', 'time': bln_time-0.0000001})
                for grid in range(0, g['grid']):
                    DOC.append({'type': 'gridline', 'time': grd_time})
                    grd_time += grid_len
                bln_time += meas_len
            if g['visible'] == 1:
                DOC.append({'type': 'time_signature_text', 'time': t_sig_start_tick(t_sig_map, idx),
                            'duration': meas_len, 'text': str(g['numerator']) + '/' + str(g['denominator'])})
            idx += 1

        # add endbarline event
        DOC.append({'type': 'endbarline', 'time': total_pianoticks-1})

        # we add all events from Score to the DOC list
        for note_evt in note:
            e = note_evt
            e['type'] = 'note'
            e = note_split_processor(e, Score)
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
        
        # we first need to get the split times from Score
        bl_times = barline_times(Score['properties']['grid'])
        
        split_times = [0]
        for spl in Score['events']['line-break']:
            if spl['time'] > 0 and not spl['time'] > total_pianoticks:
                split_times.append(spl['time'])
        split_times.append(total_pianoticks)
        
        # now we split the DOC list into parts of lines
        doc = DOC
        DOC = []
        for _,spl in enumerate(split_times):
            buffer = []
            try: nxt = split_times[_+1]
            except IndexError: nxt = split_times[-1]
            for e in doc:
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

        # in this part we calculate how many systems fit on each page
        # also we gather the free space in the printarea in a list
        # called 'page_spacing'.
        doc = DOC
        DOC = []
        y_cursor = header_h
        printarea_height = (page_height - p_marg_u - p_marg_d)
        remaining_space = 0
        page = []
        for line, sh, c in zip(doc,staff_heights, range(len(doc))):
            lmu = line_break[c]['margin-up-left'] * MM
            lmd = line_break[c]['margin-down-right'] * MM
            y_cursor += lmu + sh + lmd
            # if the line fits on paper:
            if y_cursor <= printarea_height - header_h - footer_h:
                page.append(line)
                remaining_space = printarea_height - header_h - footer_h - y_cursor
            # if the line does NOT fit on paper:
            else:
                y_cursor = lmu + sh + lmd
                DOC.append(page)
                page = []
                page.append(line)
                page_spacing.append(remaining_space)
            # if this is the last line:
            if c+1 == len(doc):
                DOC.append(page)
                page_spacing.append(remaining_space)
                    
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
    












    ##-------------------------##
    ## DRAW ENGINE PIANOSCRIPT ##
    ##-------------------------##
    def event_x_pos_engrave(pos,start_line_tick,end_line_tick, indent=False):
        '''
        returns the x position on the paper.
        '''
        factor = interpolation(start_line_tick, end_line_tick, pos)
        if not indent:
            return p_marg_l + ((page_width - p_marg_l - p_marg_r) * factor)
        else:
            return p_marg_l + ((page_width - p_marg_l - p_marg_r - (40 * draw_scale)) * factor)

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
            color_black = color_notation_editor
            color_white = color_editor_canvas

        y_cursor = 0
        idx_l = 0
        b_counter = update_bcounter(DOC,pageno % len(DOC))
        for idx_p, page in enumerate(DOC):

            # render only one page
            if not render_type == 'export':
                if idx_p == pageno % len(DOC):
                    ...
                else:
                    for l in page:
                        idx_l += 1
                    continue
            
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
            pview.create_text(p_marg_l,
                y_cursor + page_height - p_marg_d,
                text='page ' + str(idx_p+1) + ' of ' + str(len(DOC)) + ' | ' + title['text'] + ' | ' + copyright['text'],
                anchor='sw',
                fill=color_black,
                font=('courier', 12, "normal"))

            y_cursor += p_marg_u

            if not idx_p: # if on the first page
                # draw header (title & composer text)
                pview.create_text(p_marg_l,
                    p_marg_u,
                    text=Score['header']['title']['text'],
                    anchor='nw',
                    font=('courier', 18, "normal"),
                    fill=color_black)
                pview.create_text(page_width - p_marg_r,
                    p_marg_u,
                    text=Score['header']['composer']['text'],
                    anchor='ne',
                    font=('courier', 12, "normal"),
                    fill=color_black)

                y_cursor += header_h
            
            for idx_ll, line in enumerate(page):

                sh = staff_heights[idx_l]
                lmu = line_break[idx_l]['margin-up-left'] * MM
                lmd = line_break[idx_l]['margin-down-right'] * MM
                
                y_cursor += lmu + (page_spacing[idx_p] / (len(DOC[idx_p])) / 2)

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
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        pview.create_line(x,
                                          y_cursor,
                                          x,
                                          y_cursor + sh,
                                          width=2 * draw_scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill=color_black)
                        pview.create_text(x,
                                          y_cursor,
                                          text=b_counter,
                                          tag='grid',
                                          fill=color_black,
                                          font=('courier', round(12 * draw_scale), "normal"),
                                          anchor='sw')
                        b_counter += 1

                    # draw barline at end of the system/line:
                    if obj['type'] == 'endoflinebarline':
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        pview.create_line(x,
                                          y_cursor,
                                          x,
                                          y_cursor + sh,
                                          width=2 * draw_scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill=color_black)

                    # draw the last barline that's more thick
                    if obj['type'] == 'endbarline':
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        pview.create_line(x,
                                          y_cursor,
                                          x,
                                          y_cursor + sh,
                                          width=4 * draw_scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill=color_black)

                    # grid
                    if obj['type'] == 'gridline':
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        pview.create_line(x,
                                          y_cursor,
                                          x,
                                          y_cursor + sh,
                                          width=.5 * draw_scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill=color_black,
                                          dash=(6, 6))

                    # note start
                    if obj['type'] == 'note':
                        if not idx_l:
                            x0 = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                            x1 = event_x_pos_engrave(obj['time'] + obj['duration'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x0 = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                            x1 = event_x_pos_engrave(obj['time'] + obj['duration'], split_times[idx_l],split_times[idx_l + 1])
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
                        # notestop
                        if obj['notestop']:
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
                                                  outline='black',
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

                        # connect stems abs(evt['time'] - note['time']) <= 1
                        for stem in line:
                            if abs(stem['time'] - obj['time']) <= 1 and stem['type'] == 'note' and stem['pitch'] != obj['pitch']:
                                if abs(stem['time'] - obj['time']) <= 1 and stem['hand'] == obj['hand']:
                                    stem_y = note_y_pos(stem['pitch'], mn, mx, y_cursor, draw_scale)
                                    if not idx_l:
                                        stem_x = event_x_pos_engrave(stem['time'], split_times[idx_l], split_times[idx_l + 1],True)
                                    else:
                                        stem_x = event_x_pos_engrave(stem['time'], split_times[idx_l], split_times[idx_l + 1])
                                    pview.create_line(stem_x,
                                                      stem_y,
                                                      x0,
                                                      y,
                                                      width=3 * draw_scale,
                                                      capstyle='round',
                                                      tag='connect_stem',
                                                      fill=color_black)

                    # note active
                    if obj['type'] in ['note', 'split']:
                        if not idx_l:
                            x0 = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                            x1 = event_x_pos_engrave(obj['time'] + obj['duration'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x0 = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                            x1 = event_x_pos_engrave(obj['time'] + obj['duration'], split_times[idx_l],split_times[idx_l + 1])
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
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        pview.create_text(x + (2.5 * draw_scale),
                                          y_cursor + sh + (20 * draw_scale),
                                          text=obj['text'],
                                          tag='tsigtext',
                                          anchor='w',
                                          font=('courier', round(12 * draw_scale), 'underline'),
                                          fill=color_black)

                    # text
                    if obj['type'] == 'text':
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
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
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
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

                    # end for obj ----------------------------------------

                # if this is the first line of the file:
                if not idx_l and minipiano:
                    draw_staff(y_cursor,
                        mn,
                        mx,
                        p_marg_l,
                        page_width,
                        p_marg_r,
                        color_black,
                        draw_scale,
                        pview,
                        sh,
                        True)
                else:
                    draw_staff(y_cursor,
                        mn,
                        mx,
                        p_marg_l,
                        page_width,
                        p_marg_r,
                        color_black,
                        draw_scale,
                        pview,
                        sh,
                        False)

                # update y_cursor and divide the systems equal:
                y_cursor += sh + lmd + (page_spacing[idx_p] / (len(DOC[idx_p])) / 2)

                idx_l += 1

                # end for line ---------------------------------------

            y_cursor = page_height * (idx_p + 1)


        # draw bottom line last page
        if not render_type:
            pview.create_line(0,
                page_height,
                page_width,
                page_height,
                fill=color_black,
                width=2,
                dash=(6,4,5,2,3,1))

        # drawing order
        pview.tag_raise('staff')
        pview.tag_raise('notestop')
        pview.tag_raise('grid')
        pview.tag_raise('white_space')
        pview.tag_raise('stem')
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
        #pview.tag_lower('midi_note')
        
        # make the new render update fluently(without blinking) and scale
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
            engrave('',renderpageno)
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
        do_engrave()
    root.after(500,check_resize)
check_resize()
















# --------------
# editor tools |
# --------------
def set_value(t):
    global Score, Settings, file_changed
    file_changed = True

    # Score settings
    if t == 'title':
        user_input = simpledialog.askstring(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=Score['header']['title']['text'])
        if user_input: Score['header'][t]['text'] = user_input
    elif t == 'composer':
        user_input = simpledialog.askstring(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=Score['header']['composer']['text'])
        if user_input: Score['header'][t]['text'] = user_input
    elif t == 'copyright':
        user_input = simpledialog.askstring(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=Score['header']['copyright']['text'])
        if user_input: Score['header'][t]['text'] = user_input
    elif t == 'page-width':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=Score['properties']['page-width'])
        if user_input: Score['properties'][t] = user_input
        else: Score['properties'][t] = 210
    elif t == 'page-height':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=Score['properties']['page-height'])
        if user_input: Score['properties'][t] = user_input
        else: Score['properties'][t] = 297
    elif t == 'page-margin-left':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=Score['properties']['page-margin-left'])
        if user_input: Score['properties'][t] = user_input
        else: Score['properties'][t] = 10
    elif t == 'page-margin-right':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=Score['properties']['page-margin-right'])
        if user_input: Score['properties'][t] = user_input
        else: Score['properties'][t] = 10
    elif t == 'page-margin-up':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=Score['properties']['page-margin-up'])
        if user_input: Score['properties'][t] = user_input
        else: Score['properties'][t] = 10
    elif t == 'page-margin-down':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} for the document:', initialvalue=Score['properties']['page-margin-down'])
        if user_input: Score['properties'][t] = user_input
        else: Score['properties'][t] = 10
    elif t == 'draw-scale':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t}(1=default, 2=twice as big so from .5 to 1.5 is reasonable) for the document:', initialvalue=Score['properties']['draw-scale'])
        if user_input: Score['properties'][t] = user_input
        else: Score['properties'][t] = 1
    elif t == 'header-height':
        user_input = simpledialog.askfloat(f'Set {t}...', f'Please provide the {t} in mm for the document:', initialvalue=Score['properties']['header-height'])
        if user_input: Score['properties'][t] = user_input
        else: Score['properties'][t] = 15
    
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
    do_engrave()

listbox_value = 8
def grid_selector(event='event'):
    global edit_grid, listbox_value

    for idx,i in enumerate(list_dur.curselection()):
        listbox_value = list_dur.get(i)

    lengthdict = {1: 1024, 2: 512, 4: 256, 8: 128, 16: 64, 32: 32, 64: 16, 128: 8}
    edit_grid = ((lengthdict[int(listbox_value)] / int(div_spin.get())) * int(tim_spin.get()))

    root.focus()

def process_grid_map_editor():
    '''
        This function processes the grid map editor
        syntax and places it in the Score.
    '''
    global Score

    t = gridedit_text.get('1.0', 'end').split('\n')
    ignore = False

    Score['properties']['grid'] = []

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

        # gridmap add to Score
        Score['properties']['grid'].append(
            {'amount': amount, 'numerator': numerator, 'denominator': denominator,
             'grid': grid, 'visible': visible})

    draw_pianoroll()
    do_engrave()
    update_textbox()


def update_textbox():
    '''
        This function updates the gui textboxes from Score
    '''

    # grid map editor
    txt = ''
    for ts,idx in zip(Score['properties']['grid'],range(len(Score['properties']['grid']))):

        numerator = ts['numerator']
        denominator = ts['denominator']
        amount = ts['amount']
        grid_div = ts['grid']
        visible = ts['visible']

        if not idx == len(Score['properties']['grid'])-1:
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
            grid = Score['properties']['grid']
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
            print('ERROR in transpose function; please provide three integers. \nAction is ignored.')

def insert_measure():

    global Score
    user_input = simpledialog.askstring('Insert measure(s)', HELP3, initialvalue='0 1')
    
    if user_input:
        
        # validate user_input
        try:
            print(len(barline_times(Score['properties']['grid'])))
            selection = int(user_input.split()[0])
            amount = int(user_input.split()[1])
            if selection >= len(barline_times(Score['properties']['grid'])): raise Exception
            if amount < 0: raise Exception
        except:
            print('ERROR in add_measure; please provide two integer values seperated by <space>.\nAction is ignored')
            return

            # calculating the measure length of the current selection



def remove_measure():
    
    ...

def remove_notes():
    
    ...
            
    
















# --------------------------------------------------------
# MENU
# --------------------------------------------------------
menubar = Menu(root, relief='flat', bg=color_basic_gui, fg=color_editor_canvas, font=('courier', 14))
root.config(menu=menubar)
fileMenu = Menu(menubar, tearoff=0, bg=color_basic_gui, fg=color_editor_canvas, font=('courier', 14))
fileMenu.add_command(label='|new         |', command=new_file)
fileMenu.add_command(label='|load        |', command=load_file)
fileMenu.add_command(label='|save        |', command=save)
fileMenu.add_command(label='|save as...  |', command=save_as)
fileMenu.add_separator()
fileMenu.add_command(label='|load midi   |', command=midi_import)
fileMenu.add_separator()
fileMenu.add_command(label="|export ps   |", command=exportPostscript)
fileMenu.add_command(label="|*export pdf |", command=exportPDF)
fileMenu.add_command(label="|*export midi|", command=lambda: midiexport(root,Score))
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
toolsMenu.add_command(label='|redraw editor             |', command=lambda: draw_pianoroll())
toolsMenu.add_command(label='|transpose                 |', command=lambda: transpose())
toolsMenu.add_command(label='|*insert measure           |', command=lambda: insert_measure())
toolsMenu.add_command(label='|*remove measure           |', command=lambda: remove_measure())
toolsMenu.add_command(label='|*remove notes from measure|', command=lambda: remove_notes())
menubar.add_cascade(label="|Tools|", underline=None, menu=toolsMenu)














# -------------
# MODE TOOLBAR
# -------------
def mode_select(mode,i_mode):
    
    global input_mode

    modes = [
    input_right_button,
    input_left_button,
    select_button,
    linebreak_button,
    txt_button,
    countline_button
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
            Score,
            color_right_midinote,
            color_left_midinote)
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
            Score,
            color_right_midinote,
            color_left_midinote)

    input_mode = i_mode

input_right_button.configure(command=lambda: [mode_select(0,'right'), mode_label.focus_force()])
input_left_button.configure(command=lambda: [mode_select(1,'left'), mode_label.focus_force()])
select_button.configure(command=lambda: [mode_select(2,'select'), mode_label.focus_force()])
linebreak_button.configure(command=lambda: [mode_select(3,'linebreak'), mode_label.focus_force()])
txt_button.configure(command=lambda: [mode_select(4,'text'), mode_label.focus_force()])
countline_button.configure(command=lambda: [mode_select(5,'countline'), mode_label.focus_force()])












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
        threading.Thread(target=draw_pianoroll()).start()

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
        threading.Thread(target=draw_pianoroll()).start()

def add_ctrl_z():
    print('add_ctrl_z')# publish
    
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
    pview.bind('<Button-2>', lambda e: cycle_trough_pages(e))
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
    pview.bind('<Button-3>', lambda e: cycle_trough_pages(e))
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
root.bind('<KeyPress-space>', lambda: space_shift)# review later
root.bind('<KeyRelease-space>', space_shift)
root.option_add('*Dialog.msg.font', 'Courier 20')
editor.bind('<Leave>', lambda e: editor.delete('cursor'))
root.protocol("WM_DELETE_WINDOW", quit_editor)
editor.bind("<Shift-Button-1>", lambda event: mouse_handling(event, 'shiftbtn1click'))
root.bind('<Control-z>', undo)
root.bind('<Control-Z>', redo)











if __name__ == '__main__':
    new_file()

root.mainloop()
