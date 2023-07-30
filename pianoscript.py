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

# -----
# TODO
# -----
'''
    * ...
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
print('| Code by:                                       |')
print('| Philip Bergwerf                                |')
print('| Henk van den Brink                             |')
print('| Harm Salomons                                  |')
print('--------------------------------------------------')
print('')



# ------------------
# constants
# ------------------
QUARTER = 256
BLACK = [2, 5, 7, 10, 12, 14, 17, 19, 22, 24, 26, 29, 31, 34, 36, 38, 41, 43, 46,
         48, 50, 53, 55, 58, 60, 62, 65, 67, 70, 72, 74, 77, 79, 82, 84, 86]

# grid map editor

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
from tkinter import filedialog, Label, Spinbox, StringVar, Listbox, ttk
from tkinter import simpledialog
import platform, subprocess, os, threading, json, traceback, ctypes
from mido import MidiFile
from shutil import which
import tkinter.ttk as ttk
if platform.system() == 'Darwin':
    from tkmacosx import Button
else:
    from tkinter import Button
from PIL import ImageTk, Image

# imports from my own code :)
from imports.midiutils import *
from imports.savefilestructure import *
from imports.tools import *
from imports.pianorolleditor import *
from imports.tooltip import *
from imports.engraver_pianoscript_vertical import *
from imports.engraver_pianoscript import *
from imports.dialogs import *
from imports.elementstree import Tree
from imports.griddialog import GridDialog
from imports.optionsdialog import OptionsDialog
from imports.colors import color_light, color_dark, color_gui_base, color_gui_contrast, color_highlight, color_right_midinote, color_left_midinote
from imports.editor import MainEditor

# --------------------
# GUI
# --------------------


# root
root = Tk()
root.configure(bg=color_gui_base)
MM = root.winfo_fpixels('1m')
root.title('PianoScript')
img_pianoscript = PhotoImage(file = 'pscript.png')
root.iconphoto(False, img_pianoscript)
if platform.system() == 'Windows': root.state('zoomed')
# Create an instance of ttk style
ttkstyle = ttk.Style()
ttkstyle.theme_create('pianoscript', settings={
    ".": {
        "configure": {
            "background": color_light, # All except tabs
            "foreground": color_dark,
            "font": ('courier', 16)
        }
    },
    "TNotebook": {
        "configure": {
            "background": color_light, # Your margin color
            "tabmargins": [2, 5, 0, 0], # margins: left, top, right, separator
        }
    },
    "TNotebook.Tab": {
        "configure": {
            "background": color_light, # tab color when not selected
            "padding": [10, 2], # [space between text and horizontal tab-button border, space between text and vertical tab_button border]
            "font":["courier", 16]
        },
        "map": {
            "background": [("selected", color_highlight)], # Tab color when selected
            "expand": [("selected", [1, 1, 1, 0])] # text margins
        }
    },
    "Treeview": {
        "configure": {
            "background": color_light,
            "foreground": color_dark,
            "font":("courier", 16),
            "fieldbackground": color_gui_base
        },
        "map": {
            "background": [("selected", color_highlight)],
            "foreground": [("selected", color_dark)], # Tab color when selected
            "expand": [("selected", [1, 1, 1, 0])] # text margins
        }
    }
})
ttk.Style(root).theme_use("pianoscript")

scrwidth = root.winfo_screenwidth()
scrheight = root.winfo_screenheight()
root.geometry("%sx%s+0+0" % (int(scrwidth), int(scrheight)))

# set dpi for different systems:
if platform.system() == 'Windows':  
    try: # >= win 8.1
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except: # win 8.0 or less
        ctypes.windll.user32.SetProcessDPIAware()
# if platform.system() == 'Linux':
#     root.tk.call('tk', 'scaling', 2.0)

# rootframe
rootframe = Frame(root, bg='#333333')
rootframe.pack(fill='both',expand=True)

# PanedWindow
master_paned = PanedWindow(rootframe, orient='h', sashwidth=7.5, relief='flat', bg=color_gui_base)
master_paned.pack(padx=2.5,pady=2.5,expand=True,fill='both')    

# grid selector
gridpanel = Frame(master_paned, bg=color_gui_base)
gridpanel.grid_columnconfigure(0,weight=1)
master_paned.add(gridpanel, width=250)
noteinput_label = Label(gridpanel, text='GRID:', bg=color_gui_base, fg=color_gui_contrast, anchor='w', font=("courier", 16, 'bold'))
noteinput_label.grid(column=0, row=0, sticky='ew')
list_dur = Listbox(gridpanel, height=8, bg=color_light, selectbackground=color_highlight,selectforeground=color_dark, fg=color_dark, font=('courier', 16))
list_dur.grid(column=0, row=1, sticky='ew')
list_dur.insert(0, "1")
list_dur.insert(1, "2")
list_dur.insert(2, "4")
list_dur.insert(3, "8")
list_dur.insert(4, "16")
list_dur.insert(5, "32")
list_dur.insert(6, "64")
list_dur.insert(7, "128")
list_dur.select_set(3)
divide_label = Label(gridpanel, text='÷', font=("courier", 20, "bold"), bg=color_gui_base, fg=color_gui_contrast, anchor='c')
divide_label.grid(column=0, row=2, sticky='ew')
divide_variable = StringVar(value=1)
divide_spin = Spinbox(gridpanel, from_=1, to=99, bg=color_light, fg=color_dark, font=('courier', 16, 'normal'), textvariable=divide_variable)
divide_spin.grid(column=0, row=3, sticky='ew')
times_label = Label(gridpanel, text='×', font=("courier", 20, "bold"), bg=color_gui_base, fg=color_gui_contrast, anchor='c')
times_label.grid(column=0, row=4, sticky='ew')
times_variable = StringVar(value=1)
times_spin = Spinbox(gridpanel, from_=1, to=99, bg=color_light, fg=color_dark, font=('courier', 16, 'normal'), textvariable=times_variable)
times_spin.grid(column=0, row=5, sticky='ew')
fill_label1 = Label(gridpanel, text='------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', 
    bg=color_gui_base, fg='#c8c8c8', anchor='c', font=("courier"))
fill_label1.grid(column=0, row=6, sticky='ew')

# staff selector
staffselect_label = Label(gridpanel, text='STAFF:', bg=color_gui_base, fg=color_gui_contrast, font=("courier", 16, 'bold'), anchor='w')
staffselect_label.grid(column=0, row=7, sticky='ew')
staffselect_variable = StringVar(value=1)
staffselect_spin = Spinbox(gridpanel, from_=1, to=4, bg=color_light, fg=color_dark, font=('courier', 16, 'normal'), textvariable=staffselect_variable)
staffselect_spin.grid(column=0, row=8, sticky='ew')
fill_label2 = Label(gridpanel, text='------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------', 
    bg=color_gui_base, fg='#c8c8c8', anchor='c', font=("courier"))
fill_label2.grid(column=0, row=10, sticky='ew')

# elements selector
elements_label = Label(gridpanel, text='TOOL:', bg=color_gui_base, fg=color_gui_contrast, anchor='w', font=("courier", 16, 'bold'))
elements_label.grid(column=0, row=11, sticky='ew')
elements_treeview = Tree(gridpanel)
elements_treeview.grid(column=0, row=12, sticky='ew')

# editor
root.update()
editorpanel = Frame(master_paned, bg=color_gui_base, width=scrwidth / 3 * 1.54)
master_paned.add(editorpanel)
editor = Canvas(editorpanel, bg=color_light, relief='flat', cursor='cross')
editor.place(relwidth=1, relheight=1)
hbar = Scrollbar(editor, orient='horizontal', width=20, relief='flat', bg=color_gui_base)
hbar.pack(side='bottom', fill='x')
hbar.config(command=editor.xview)
editor.configure(xscrollcommand=hbar.set)

# print view
printpanel = Frame(master_paned, bg=color_light)
master_paned.add(printpanel)
pview = Canvas(printpanel, bg=color_light, relief='flat')
pview.place(relwidth=1, relheight=1)



  





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
    with open('test2.pianoscript', 'r') as f:
        global Score
        Score = json.load(f)
        # run the piano-roll and print-view
        do_pianoroll()
        do_engrave('')
        root.title('PianoScript - %s' % f.name)

def new_file(e=''):
    global Score, file_changed,file_path, renderpageno
    print('new_file')

    # check if user wants to save or cancel the task.
    if file_changed == True:
        ask = AskYesNoCancel(root, 'Wish to save?', 'Do you wish to save the current Score?').result
        if ask == True:# yes
            save()
        elif ask == False:# no
            ...
        elif ask == None:# cancel
            return

    file_changed = False
    renderpageno = 0

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

    # set button switch horz. vert.
    # if Score['properties']['engraver'] == 'pianoscript':
    #     engraver_button.configure(text='V')
    # else:
    #     engraver_button.configure(text='H')

    # set the staff to staff 1
    staffselect_variable.set(1)


def load_file(e=''):
    print('load_file...')

    global Score, file_changed, file_path, renderpageno

    # check if user wants to save or cancel the task.
    if file_changed == True:
        ask = AskYesNoCancel(root, 'Wish to save?', 'Do you wish to save the current Score?').result
        if ask == True:
            save()
        elif ask == False:
            ...
        elif ask == None:
            return
    else:
        ...

    file_changed = False
    renderpageno = 0

    # open Score
    try: 
        f = subprocess.check_output(["zenity", "--file-selection", "--title=Open file..."]).decode("utf-8").strip()
    except:
        f = filedialog.askopenfile(parent=root, 
            mode='r',
            title='Open', 
            filetypes=[("PianoScript files", "*.pianoscript")])
        if f: f = f.name
    if f:
        # update file_path
        file_path = f

        # load f:
        with open(f, 'r') as f:
            fjson = json.load(f)
            try:
                if fjson['header']['app-name'] == 'pianoscript':
                    Score = fjson
                else:
                    print('ERROR: file is not a pianoscript file.')
            except:
                print('ERROR: file is not a pianoscript file or is damaged.')

        # converter(filepath)
        Score = compatibility_checker(Score)

        # run the piano-roll and print-view
        do_pianoroll()
        do_engrave()
        root.title('PianoScript - %s' % f.name)
        # set button switch horz. vert.
        # if Score['properties']['engraver'] == 'pianoscript':
        #     engraver_button.configure(text='V')
        # else:
        #     engraver_button.configure(text='H')
    
    return


def save(e=''):
    print('save...')
    global file_changed

    if file_path != 'New':
        f = open(file_path, 'w')
        f.write(json.dumps(Score, separators=(',', ':'), indent=2))# indent=2
        f.close()
        file_changed = False
    else:
        save_as()


def save_as(e=''):
    print('save_as...')
    global file_path, file_changed

    # save Score
    try: 
        f = subprocess.check_output(["zenity", "--file-selection", "--save", "--title=Save file as..."]).decode("utf-8").strip()
    except:
        f = filedialog.asksaveasfile(parent=root, 
            mode='w', 
            filetypes=[("PianoScript files", "*.pianoscript")],
            title='Save as...',
            initialdir='~/Desktop/')
        f = f.name
    if f:
        root.title('PianoScript - %s' % f)
        file = open(f, 'w')
        file.write(json.dumps(Score, separators=(',', ':'), indent=2))# indent=2
        file.close()
        # update file_path
        file_path = f
        file_changed = False


def quit_editor(event='dummy'):
    print('quit_editor...')

    # check if user wants to save or cancel the task.
    if file_changed == True:
        ask = AskYesNoCancel(root, 'Wish to save?', 'Do you wish to save the current Score?').result
        if ask == True:
            save()
        elif ask == False:
            ...
        elif ask == None:
            return

    print('')
    print('----------------------------------')
    print('| http://www.pianoscript.org/ :) |')
    print('| Many Love From Philip Bergwerf |')
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
copycut_buffer = []
selection_buffer = []
mouse_time = 0
ms_xy = [0,0]
new_slur = 0
handle = ''

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

    global last_pianotick, new_id, x_scale_quarter_mm, y_scale_percent

    x_scale_quarter_mm = Score['properties']['editor-x-zoom']
    y_scale_percent = Score['properties']['editor-y-zoom'] / 100
    
    # calculate last_pianotick (staff length)
    last_pianotick = 0
    for grid in Score['events']['grid']:

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
                fill=color_dark)

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
                fill=color_dark,
                state='disabled')
            editor.create_text(x_curs+5,
                staff_y0,
                text=measnum,
                anchor='sw',
                fill=color_dark,
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
                    fill=color_dark,
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
        fill=color_dark,
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
                fill=color_dark,
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
                    fill=color_dark,
                    state='disabled')
            else:
                editor.create_line(staff_x0,
                    y_curs,
                    staff_x1,
                    y_curs,
                    width=1,
                    tag='staffline',
                    fill=color_dark,
                    state='disabled')
            y_curs += 10 * y_factor

        y_curs += 10 * y_factor

    editor.create_line(staff_x0,
        y_curs,
        staff_x1,
        y_curs,
        width=2,
        tag='staffline',
        fill=color_dark,
        state='disabled')

    # update bbox
    _, _, bbox3, bbox4 = editor.bbox('all')
    editor.configure(scrollregion=(0, 0, bbox3 + editor_x_margin, bbox4 + staff_y_margin))

    # DOC EVENTS

    new_id = 0

    # draw note events
    for note in Score['events']['note']:
        note['id'] = 'note%i'%new_id
        if note['staff'] == int(staffselect_variable.get())-1: draw_note_pianoroll(note,
            False, 
            editor, 
            hbar, 
            y_scale_percent, 
            x_scale_quarter_mm, 
            MM, 
            color_dark, 
            BLACK, 
            color_light, 
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
            color_dark,
            color_highlight)
        new_id += 1

    # draw countline events
    for cl in Score['events']['count-line']:
        cl['id'] = 'countline%i'%new_id
        if cl['staff'] == int(staffselect_variable.get())-1: 
            draw_countline_editor(cl,
                editor,
                hbar,
                y_scale_percent,
                x_scale_quarter_mm,
                MM,
                color_dark)
        new_id += 1

    # draw text events
    for txt in Score['events']['text']:
        txt['id'] = 'text%i'%new_id
        if txt['staff'] == int(staffselect_variable.get())-1: draw_text_editor(txt,
            editor, hbar, y_scale_percent, 
            x_scale_quarter_mm, MM)
        new_id += 1

    # draw staffsizer events
    for ss in Score['events']['staff-sizer']:
        ss['id'] = 'staffsizer%i'%new_id
        if ss['staff'] == int(staffselect_variable.get())-1: draw_staffsizer_editor(ss,
            editor, hbar, y_scale_percent, 
            x_scale_quarter_mm, MM)
        new_id += 1

    # draw start repeat events
    for sr in Score['events']['start-repeat']:
        sr['id'] = 'startrepeat%i'%new_id
        draw_startrepeat_editor(sr,
            editor, hbar, y_scale_percent, 
            x_scale_quarter_mm, MM)
        new_id += 1

    # draw end repeat events
    for er in Score['events']['end-repeat']:
        er['id'] = 'endrepeat%i'%new_id
        draw_endrepeat_editor(er,
            editor, hbar, y_scale_percent, 
            x_scale_quarter_mm, MM)
        new_id += 1

    # draw beam events
    for bm in Score['events']['beam']:
        bm['id'] = 'beam%i'%new_id
        if bm['staff'] == int(staffselect_variable.get())-1: 
            draw_beam_editor(bm,
                editor, hbar, y_scale_percent, 
                x_scale_quarter_mm, MM)
        new_id += 1

    # draw slur events
    for sl in Score['events']['slur']:
        sl['id'] = 'slur%i'%new_id
        if sl['staff'] == int(staffselect_variable.get())-1:
            slur_editor(sl,
                editor,
                hbar,
                y_scale_percent,
                x_scale_quarter_mm,
                MM)
        new_id += 1

    update_drawing_order_editor(editor)

    editor.delete('loading')

    




            





def staffselect_variable_callback():
    '''This function runs if you select another staff in the staff selector'''
    do_pianoroll()

staffselect_spin.configure(command=staffselect_variable_callback)













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
    global hold_id, hand, new_id, cursor_note, cursor_time, edit_cursor, file_changed, new_slur, selection_buffer
    global selection, shiftbutton1click, selection_tags, mouse_time, active_selection, ms_xy, handle

    editor.tag_lower('cursor')

    input_mode = elements_treeview.get

    # define mouse_x and mouse_y, event_x and event_y.
    mx = editor.canvasx(event.x)
    my = editor.canvasy(event.y)
    ex = x2tick_editor(mx, editor, hbar, y_scale_percent, x_scale_quarter_mm, last_pianotick, edit_grid, MM)
    ey = y2pitch_editor(my, editor, hbar, y_scale_percent)

    if event_type == 'shiftbtn1release':
        shiftbutton1click = False

    if input_mode == 'right' or input_mode == 'left':

        '''
            This part defines what to do if we are
            in 'note-adding/editing-mode'.
        '''

        # we add a note when not clicking on an existing note with left-mouse-button:
        if event_type == 'btn1click' or event_type == 'ctl-click-btn1':

            # if control was hold while clicking the stem is set to invisible
            if event_type == 'ctl-click-btn1':
                stem_visible = False
            else:
                stem_visible = True

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
            add_ctrl_z()
            if not editing:
                # create a new note in Score

                new_note = {
                    "id": 'note%i'%new_id,
                    "time": ex,
                    "duration": edit_grid,
                    "pitch": ey,
                    "hand": hand,
                    "x-offset": 0,
                    "y-offset": 0,
                    "stem-visible": stem_visible,
                    "accidental":0,
                    "type":'note',
                    "staff":int(staffselect_variable.get()) - 1
                }

                draw_note_pianoroll(new_note, 
                    False, 
                    editor, 
                    hbar, 
                    y_scale_percent, 
                    x_scale_quarter_mm, 
                    MM, 
                    color_dark, 
                    BLACK, 
                    color_light, 
                    Score,
                    True)
                # write new_note to Score
                Score['events']['note'].append(new_note)
                # sort the events on the time key
                Score['events']['note'] = sorted(Score['events']['note'], key=lambda time: time['time'])
                hold_id = new_note['id']
                new_id += 1
            else:
                # update hand  and stem-visible
                for evt in Score['events']['note']:
                    if evt['id'] == hold_id:
                        evt['hand'] = hand
                        evt['stem-visible'] = stem_visible
                        editor.delete(hold_id)
                        draw_note_pianoroll(evt, 
                            False, 
                            editor, 
                            hbar, 
                            y_scale_percent, 
                            x_scale_quarter_mm, 
                            MM, 
                            color_dark, 
                            BLACK, 
                            color_light, 
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
                            m_x = x2tick_editor(mx, editor, hbar, y_scale_percent, x_scale_quarter_mm, last_pianotick, edit_grid, MM, False)
                            if m_x > evt['time']:
                                evt['duration'] = m_x - evt['time']
                            if m_x < evt['time']:
                                evt['pitch'] = y2pitch_editor(my, editor, hbar, y_scale_percent)
                            draw_note_pianoroll(evt, 
                                False, 
                                editor, 
                                hbar, 
                                y_scale_percent, 
                                x_scale_quarter_mm, 
                                MM, 
                                color_dark, 
                                BLACK, 
                                color_light, 
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
                    "stem-visible": True,
                    "accidental":0,
                    "staff":int(staffselect_variable.get())-1
                }
                draw_note_pianoroll(cursor, 
                    True, 
                    editor, 
                    hbar, 
                    y_scale_percent, 
                    x_scale_quarter_mm, 
                    MM, 
                    color_dark, 
                    BLACK, 
                    color_light, 
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
                "stem-visible": True,
                "accidental":0,
                "staff":int(staffselect_variable.get())-1
            }
            draw_note_pianoroll(cursor, 
                True, 
                editor, 
                hbar, 
                y_scale_percent, 
                x_scale_quarter_mm, 
                MM, 
                color_dark, 
                BLACK, 
                color_light, 
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
                                MM,Score,color_dark, True,'r')
                            update_connectstem(evt,editor,hbar,y_scale_percent,x_scale_quarter_mm,
                                MM,Score,color_dark, True,'r')

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
                        color_dark, 
                        BLACK, 
                        color_light, 
                        Score,
                        False)
                    update_drawing_order_editor(editor)

        # empty selection_buffer
        selection_buffer = []

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

        if input_mode == 'beamtool':

            # draw a arrow on the cursor to give the user feedback
            # on which hand we add the beam if we click in case of
            # beamtool.
            if ey > 40:
                beam = 'up'
            else:
                beam = 'down'
        else:
            beam = None
        draw_cursor_editor(cursor,
            editor,
            hbar,
            y_scale_percent,
            x_scale_quarter_mm,
            MM,
            color_highlight,
            beam)
        Score['cursor'] = cursor

        editor.tag_lower(cursor['id'])

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
                draw_select_rectangle(selection, editor)

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
            # making the selected note(s) blue and adding to selection_buffer:
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
                            color_dark, 
                            BLACK, 
                            color_light,
                            Score,
                            False,
                            True)
                        update_drawing_order_editor(editor)
                        selection_buffer.append(n)
                        break
                active_selection = True

    if input_mode == 'linebreak':
        '''
            This part defines what to do if we are
            in 'linebreak-adding-mode'.
        '''

        if event_type == 'ctl-click-btn1':
            # run add quick linebreaks when we ctl+click and return after that to prevent
            # double edits.
            add_quick_linebreaks()
            return

        if event_type == 'btn1click':

            # it's not alowed to create a linebreak >= latest pianotick; we ignore this case
            if ex >= last_pianotick or ex <= 0:
                return
            # hold_id
            for lb in Score['events']['line-break']:
                if lb['time'] == ex:
                    hold_id = lb['id']

        if event_type == 'btn1release':

            # it's not alowed to create a linebreak >= latest pianotick; we ignore this case
            # it's not alowed to create a linebreak <= 0; we ignore this case
            if ex >= last_pianotick or ex <= 0:
                if ex <= 0:
                    # edit the margins (after this scope break/return)
                    Score['events']['line-break'][0] = LinebreakDialog(root,Score['events']['line-break'][0]).result
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
                            lb = LinebreakDialog(root,lb).result
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
                                    color_dark,
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
                            color_dark,
                            color_highlight)
                        hold_id = ''
                        file_changed = True
                        break
            else:
                # add new linebreak
                new_linebreak = {
                    "id":'linebreak%i'%new_id,
                    "time":ex,
                    "margin-staff1-left":10,
                    "margin-staff1-right":10,
                    "margin-staff2-left":10,
                    "margin-staff2-right":10,
                    "margin-staff3-left":10,
                    "margin-staff3-right":10,
                    "margin-staff4-left":10,
                    "margin-staff4-right":10,
                    "type":'linebreak'
                }
                new_id += 1
                draw_linebreak_editor(new_linebreak,
                    editor,
                    hbar,
                    y_scale_percent,
                    x_scale_quarter_mm,
                    MM,
                    color_dark,
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

        if event_type == 'btn1click':

            tags = editor.gettags('current')
            edit = False
            try:
                if 'text' in tags[0]:
                    edit = True
            except IndexError: ...

            if edit:
                # editing position
                hold_id = tags[0]

            else:
                # adding new text
                user_input = AskTextEditor(root)
                # if user_input.text == None: return
                new = {
                    "id":'text%i'%new_id,
                    "time":ex,
                    "pitch":ey,
                    "text":user_input.text,
                    "angle":user_input.angle,
                    "staff":int(staffselect_variable.get())-1
                }
                new_id += 1

                draw_text_editor(new,editor,hbar,y_scale_percent,
                    x_scale_quarter_mm,MM)
                do_engrave()

                # add to Score
                Score['events']['text'].append(new)

        if event_type == 'motion':

            if 'text' in hold_id:

                for t in Score['events']['text']:
                    if t['id'] == hold_id:
                        t['time'] = ex
                        t['pitch'] = ey
                        draw_text_editor(t,editor,hbar,y_scale_percent,
                            x_scale_quarter_mm,MM)

        if event_type == 'btn1release':

            if 'text' in hold_id:
                # moving the text while moving the mouse
                for t in Score['events']['text']:
                    if t['id'] == hold_id:
                        t['time'] = ex
                        t['pitch'] = ey
                        draw_text_editor(t,editor,hbar,y_scale_percent,
                            x_scale_quarter_mm,MM)

                hold_id = ''
                do_engrave()        


        if event_type == 'btn3click':

            # remove text at right mouse click
            tags = editor.gettags('current')
            if 'text' in tags[0]:
                editor.delete(tags[0])
            else: return
            for t in Score['events']['text']:
                if t['id'] == tags[0]:
                    Score['events']['text'].remove(t)
                    do_engrave()

        if event_type == 'ctl-click-btn1':

            tags = editor.gettags('current')
            if tags:
                if 'text' in tags[0]:
                    for t in Score['events']['text']:
                        if t['id'] == tags[0]:
                            # Edit existing text
                            user_input = AskTextEditor(root,t)
                            if user_input.textmsg == None: return
                            t['text'] = user_input.text
                            t['angle'] = user_input.angle
                            # redraw in editor
                            draw_text_editor(t,
                                editor, hbar, y_scale_percent, 
                                x_scale_quarter_mm, MM)
                            do_engrave()

    
    if input_mode == 'countline':
        '''
            This part defines what to do if we are
            in 'countline-adding-mode'.
        '''

        if event_type == 'btn1click':

            # there are two options; editing or adding
            tags = editor.gettags('current')
            edit = False
            try:
                if 'countline' in tags[0]:
                    edit = True
            except IndexError: ...

            if edit:
                # editing
                handle = tags[1]
                hold_id = tags[0]

            else:
                # adding
                new = {
                    "id":'countline%i'%new_id,
                    "time":ex,
                    "pitch1":ey,
                    "pitch2":ey,
                    "staff":int(staffselect_variable.get())-1
                }
                new_id += 1

                draw_countline_editor(new,editor,hbar,y_scale_percent,
                    x_scale_quarter_mm,MM)

                hold_id = new['id']

                # add to Score
                Score['events']['count-line'].append(new)


        if event_type == 'motion':

            if 'countline' in hold_id:

                for cl in Score['events']['count-line']:
                    if cl['id'] == hold_id:
                        if handle == 'handle1':
                            cl['pitch1'] = ey
                        else:
                            cl['pitch2'] = ey
                        draw_countline_editor(cl,editor,hbar,y_scale_percent,
                            x_scale_quarter_mm,MM)

        if event_type == 'btn1release':

            if 'countline' in hold_id:

                for cl in Score['events']['count-line']:
                    if cl['id'] == hold_id:
                        if handle == 'handle1':
                            cl['pitch1'] = ey
                        else:
                            cl['pitch2'] = ey
                        draw_countline_editor(cl,editor,hbar,y_scale_percent,
                            x_scale_quarter_mm,MM)
                
                hold_id = ''
                do_engrave()

        if event_type == 'btn3click':

            # remove countline at right mouse click
            tags = editor.gettags('current')
            if 'countline' in tags[0]:
                editor.delete(tags[0])
            else: return
            for cl in Score['events']['count-line']:
                if cl['id'] == tags[0]:
                    Score['events']['count-line'].remove(cl)
                    do_engrave()



    if input_mode == 'slur':

        if event_type == 'btn1click':

            # Detecting if we are clicking a slur/handle
            tags = editor.gettags(editor.find_withtag('current'))
            editing = False
            if tags:    
                if 'slur' in tags[0]:
                    editing = True
                    hold_id = tags[0]
            
            if editing:
                handle = tags[1]
                print(tags)
            else:
                # adding a new slur
                new_slur = {
                    'id':'slur%i'%new_id,
                    'time':ex,
                    'points':[[ex,ey],[ex,ey],[ex,ey],[ex,ey]],
                    'staff':int(staffselect_variable.get())-1,
                    'type':'slur'
                }
                new_id += 1
                hold_id = new_slur['id']
                
                # draw slur on editor
                slur_editor(new_slur,
                    editor,
                    hbar,
                    y_scale_percent,
                    x_scale_quarter_mm,
                    MM)

                handle = 'new'
            
                # write new event to Score
                Score['events']['slur'].append(new_slur)

        if event_type == 'motion':

            if hold_id and handle == 'new':
                
                for sl in Score['events']['slur']:
                    if sl['id'] == hold_id:
                        sl['points'][1][0] = sl['time'] + ((sl['points'][3][0] - sl['points'][0][0])*0.25)
                        sl['points'][2][0] = sl['time'] + ((sl['points'][3][0] - sl['points'][0][0])*0.75)
                        sl['points'][3][0] = ex
                        sl['points'][3][1] = ey
                        
                        slur_editor(sl,
                            editor,
                            hbar,
                            y_scale_percent,
                            x_scale_quarter_mm,
                            MM,
                            True)
            if hold_id and handle:
                for sl in Score['events']['slur']:
                    if sl['id'] == hold_id:
                        # change selected ctl point
                        if handle == 'ctl1':
                            sl['time'] = ex
                            sl['points'][0][0] = ex
                            sl['points'][0][1] = ey
                            sl['points'][1][0] = sl['time'] + ((sl['points'][3][0] - sl['points'][0][0])*0.25)
                            sl['points'][2][0] = sl['time'] + ((sl['points'][3][0] - sl['points'][0][0])*0.75)
                        if handle == 'ctl2':
                            sl['points'][1][0] = ex
                            sl['points'][1][1] = ey
                        if handle == 'ctl3':
                            sl['points'][2][0] = ex
                            sl['points'][2][1] = ey
                        if handle == 'ctl4':
                            sl['points'][3][0] = ex
                            sl['points'][3][1] = ey
                            sl['points'][1][0] = sl['time'] + ((sl['points'][3][0] - sl['points'][0][0])*0.25)
                            sl['points'][2][0] = sl['time'] + ((sl['points'][3][0] - sl['points'][0][0])*0.75)
                        print(handle)
                        slur_editor(sl,
                            editor,
                            hbar,
                            y_scale_percent,
                            x_scale_quarter_mm,
                            MM,
                            True)


        if event_type == 'btn1release':

            # save the slur to Score
            hold_id = ''
            editor.delete('selectionline')
            do_engrave()

        if event_type == 'shiftbutton1click':

            ...

        if event_type == 'shiftbtn1release':

            ...

        if event_type == 'btn3click':

            # delete slur we clicked on from editor
            tags = editor.gettags('current')
            if tags:
                if 'slur' in tags[0]: editor.delete(tags[0])
                else: return
                for sl in Score['events']['slur']:
                    if sl['id'] == tags[0]:
                        Score['events']['slur'].remove(sl)
                        do_engrave()

    if input_mode == 'staffsizer':

        if event_type == 'btn1click':
            # there are two options; editing or adding
            tags = editor.gettags('current')
            edit = False
            try:
                if 'staffsizer' in tags[0]:
                    edit = True
            except IndexError: ...

            if edit:
                # editing
                handle = tags[1]
                hold_id = tags[0]

            else:
                # adding
                new = {
                    "id":'staffsizer%i'%new_id,
                    "time":ex,
                    "pitch1":ey,
                    "pitch2":ey,
                    "staff":int(staffselect_variable.get()) - 1
                }
                new_id += 1
                hold_id = new['id']
                draw_staffsizer_editor(new,editor,hbar,y_scale_percent,
                    x_scale_quarter_mm,MM)
                Score['events']['staff-sizer'].append(new)
                do_engrave()

        if event_type == 'motion':

            if 'staffsizer' in hold_id:
                for ss in Score['events']['staff-sizer']:
                    if ss['id'] == hold_id:
                        if handle == 'pitch1':
                            ss['pitch1'] = ey
                        else:
                            ss['pitch2'] = ey
                        draw_staffsizer_editor(ss,editor,hbar,y_scale_percent,
                                                x_scale_quarter_mm,MM)

        if event_type == 'btn1release':

            if 'staffsizer' in hold_id:

                hold_id = ''
                do_engrave()

        if event_type == 'btn3click':

            # removing sizer
            tags = editor.gettags('current')
            if tags:
                if 'staffsizer' in tags[0]: editor.delete(tags[0])
                else: return
                for r in Score['events']['staff-sizer']:
                    if r['id'] == tags[0]:
                        Score['events']['staff-sizer'].remove(r)
                        do_engrave()


    if input_mode == 'repeats':

        if event_type == 'btn1click':

            # adding start repeat
            ...
            new = {
                "id":'startrepeat%i'%new_id,
                "time":ex
            }
            new_id += 1

            draw_startrepeat_editor(new,editor,hbar,y_scale_percent,
                x_scale_quarter_mm,MM)

            # add to Score
            Score['events']['start-repeat'].append(new)

            do_engrave()

        if event_type == 'ctl-click-btn1':

            # add end repeat
            new = {
                "id":'endrepeat%i'%new_id,
                "time":ex
            }
            new_id += 1

            draw_endrepeat_editor(new,editor,hbar,y_scale_percent,
                x_scale_quarter_mm,MM)

            # add to Score
            Score['events']['end-repeat'].append(new)

            do_engrave()

        if event_type == 'btn3click':

            # remove start repeat if we clicked on it with the right mouse button:
            for sr in Score['events']['start-repeat']:
                if ex == sr['time']:
                    # remove start repeat from file
                    Score['events']['start-repeat'].remove(sr)
                    # remove start repeat from editor
                    editor.delete(sr['id'])
                    do_engrave()
                    file_changed = True
            for er in Score['events']['end-repeat']:
                if abs(ex - er['time']) <= 1:
                    # remove end repeat from file
                    Score['events']['end-repeat'].remove(er)
                    # remove end repeat from editor
                    editor.delete(er['id'])
                    do_engrave()
                    file_changed = True

    editor.tag_raise('cursor')




    if input_mode == 'beamtool':

        if event_type == 'btn1click':

            # Detecting if we are clicking a beam start
            tags = editor.gettags(editor.find_withtag('current'))
            editing = False
            if tags:    
                if 'beam' in tags[0]:
                    editing = True
                    hold_id = tags[0]

            if not editing:

                # create a new beam in Score:
                if ey > 40:
                    h = 'r'
                else:
                    h = 'l'
                new = {
                    "id": 'beam%i'%new_id,
                    "time": ex,
                    "duration": 0,
                    "hand":h,
                    "staff":int(staffselect_variable.get()) - 1
                }
                new_id += 1
                draw_beam_editor(new,
                    editor, hbar, y_scale_percent, 
                    x_scale_quarter_mm, MM)
                # write new_note to Score
                Score['events']['beam'].append(new)
                # sort the events on the time key
                Score['events']['beam'] = sorted(Score['events']['beam'], key=lambda time: time['time'])
                hold_id = new['id']

        if event_type == 'ctl-click-btn1':

            # if we ctrl+click we add a default beam pattern entered by a simple dialog.
            # you can enter one or multiple pianotick lengths(quarter note = 256 pianoticks).
            
            # get and test user input:
            while True:
                user_input = AskString(root,
                        'Set default beam grouping...',
                        'You can set the beam grouping in "pianoticks". A quarter note is 256 pianoticks.\nPlease enter one or more beamrouping lengths in pianoticks, seperated by <space>.\nExample in a 7/8 time-signature: "384 512" will put the default beam grouping to 3 and 4 eight notes.\nthis beam grouping is applied from the point in time you clicked to the rest of the document.')
                if user_input.result is not None:
                    try:
                        user_input = user_input.result.split()
                        for idx, ui in enumerate(user_input):
                            user_input[idx] = float(ui)
                            if float(ui) <= 0:
                                raise Exception 
                        break
                    except:
                        print('ERROR in set_beam_grouping; please provide one or more floats or integers seperated by <space>.')
                else: 
                    hold_id = ''
                    file_changed = True
                    return
            
            # apply valid user input:
            if ey > 40:
                h = 'r'
            else:
                h = 'l'
            pt_cursor = ex
            # delete old beams after event click(ex)
            for bm in Score['events']['beam']:
                if bm['time'] >= ex and bm['hand'] == h:
                    Score['events']['beam'].remove(bm)
            while True:
                if pt_cursor >= last_pianotick:
                    break
                for pt in user_input:
                    # insert beam
                    new = {
                        "id": 'beam%i'%new_id,
                        "time": pt_cursor,
                        "duration": pt,
                        "hand":h,
                        "staff":int(staffselect_variable.get())-1
                    }
                    new_id += 1
                    # write to Score
                    Score['events']['beam'].append(new)
                    # draw on editor
                    draw_beam_editor(new,
                    editor, hbar, y_scale_percent, 
                    x_scale_quarter_mm, MM)
                    pt_cursor += pt
            Score['events']['beam'] = sorted(Score['events']['beam'], key=lambda time: time['time'])
            do_engrave()
            return

        if event_type == 'motion':

            if hold_id:
                for bm in Score['events']['beam']:
                    if bm['id'] == hold_id:
                        # write changed beam to Score:
                        bm['duration'] = ex - bm['time']
                        if bm['duration'] < edit_grid:
                            bm['duration'] = edit_grid
                        # redraw beam on editor: 
                        draw_beam_editor(bm,
                            editor, hbar, y_scale_percent, 
                            x_scale_quarter_mm, MM)

        if event_type == 'btn1release':

            hold_id = ''
            do_engrave()

        if event_type == 'btn3click':


            for bm in Score['events']['beam']:
                if ey > 40:
                    if abs(ex - bm['time']) <= 1 and bm['hand'] == 'r':
                        # remove end beam from file
                        Score['events']['beam'].remove(bm)
                        # remove end beam from editor
                        editor.delete(bm['id'])
                        do_engrave()
                        file_changed = True
                else:
                    if abs(ex - bm['time']) <= 1 and bm['hand'] == 'l':
                        # remove end beam from file
                        Score['events']['beam'].remove(bm)
                        # remove end beam from editor
                        editor.delete(bm['id'])
                        do_engrave()
                        file_changed = True

    if input_mode == 'accidental':

        if event_type == 'btn1click':

            # detect note
            tags = editor.gettags(editor.find_withtag('current'))
            if tags:
                if 'note' in tags[0]:
                    tags = tags[0]
            
            for evt in Score['events']['note']:
                if evt['id'] == tags:
                    evt['accidental'] = 1

                    # redraw note
                    draw_note_pianoroll(evt,
                            False, 
                            editor,
                            hbar, 
                            y_scale_percent, 
                            x_scale_quarter_mm, 
                            MM, 
                            color_dark, 
                            BLACK, 
                            color_light, 
                            Score,
                            False)
                    update_drawing_order_editor(editor)
        
        if event_type == 'btn2click':

            # detect note
            tags = editor.gettags(editor.find_withtag('current'))
            if tags:
                if 'note' in tags[0]:
                    tags = tags[0]
            
            for evt in Score['events']['note']:
                if evt['id'] == tags:
                    evt['accidental'] = 0

                    # redraw note
                    draw_note_pianoroll(evt,
                            False, 
                            editor,
                            hbar, 
                            y_scale_percent, 
                            x_scale_quarter_mm, 
                            MM, 
                            color_dark, 
                            BLACK, 
                            color_light, 
                            Score,
                            False)
                    update_drawing_order_editor(editor)

        if event_type == 'btn3click':

            # detect note
            tags = editor.gettags(editor.find_withtag('current'))
            if tags:
                if 'note' in tags[0]:
                    tags = tags[0]
            
            for evt in Score['events']['note']:
                if evt['id'] == tags:
                    evt['accidental'] = -1

                    # redraw note
                    draw_note_pianoroll(evt,
                            False, 
                            editor,
                            hbar, 
                            y_scale_percent, 
                            x_scale_quarter_mm, 
                            MM, 
                            color_dark, 
                            BLACK, 
                            color_light, 
                            Score,
                            False)
                    update_drawing_order_editor(editor)

        if not event_type == 'motion': do_engrave()


            

            

                    


    











def keyboard_handling(event):

    ...














def midi_import():
    global file_changed, Score

    # asking for save since we are creating a new file with the midifile in it.
    if file_changed == True:
        ask = AskYesNoCancel(root, 'Wish to save?', 'Do you wish to save the current Score?').result
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
                        print(n['time'], ' - ', i['time'], ' = ', n['time']-i['time'])
                        i['duration'] = n['time'] - i['time']
                        break

            if i['type'] == 'time_signature':
                for t in mesgs[index + 1:]:
                    if t['type'] == 'time_signature' or t['type'] == 'end_of_track':
                        i['duration'] = t['time'] - i['time']
                        break
            index += 1

        # check for messages without duration:
        for i in mesgs:
            if i['type'] == 'note_on':
                if not 'duration' in i:
                    i['duration'] = 0

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
        # we calculate the average of the notes, if we have more than 2 channels, the lowest is called p(edal), the 2nd lowest l(eft), the 
        # 3rd r(ight). If there are more than 3 channels, they are directed to 'l' and 'r' 
        channelsum={}
        notes_in_channel={}
        channelmax={}
        channelmin={}
        channelmean={}
        for i in mesgs:
            if i['type'] == 'note_on':
                c=i['channel']
                if c not in channelsum:
                    channelsum[c]=0
                    notes_in_channel[c]=0
                    channelmax[c]=-99
                    channelmin[c]=99

                channelsum[c]+=i['note']
                notes_in_channel[c]+=1
                if i['note'] < channelmin[c]:
                    channelmin[c]=i['note']
                if i['note'] > channelmax[c]:
                    channelmax[c]=i['note']

        for c in channelsum:
            channelmean[c]=channelsum[c]/notes_in_channel[c]

        xx=dict(sorted(channelmean.items(), key=lambda item: item[1]))
        hand={}
        name=['r','l','r','l','r','l','r','l','r','l','r','l','r','l','r','l','r','l','r','l']
        if len(xx) > 2:
            for i,x in enumerate(xx):
                hand[x]=name[i]
        else:
            for i,x in enumerate(xx):
                hand[x]=name[i+1]

        for i in mesgs:
            if i['type'] == 'note_on':
                print(i)
                Score['events']['note'].append({'time': i['time'], 
                                                'duration': i['duration'], 
                                                'pitch': i['note'] - 20, 
                                                'hand': hand[i['channel']], 
                                                'id':new_id,
                                                'stem-visible':True,
                                                'accidental':0,
                                                'staff':0,
                                                'notestop':True})
                new_id += 1

        add_quick_linebreaks()

        # engraving and drawing the pianoroll
        threading.Thread(target=do_pianoroll).start()
        do_engrave()

















# ------------------
# export
# ------------------
def exportPDF(event=''):    
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
                    color_dark,
                    color_light,
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
            else:
                numofpages = range(engrave_pianoscript_vertical('export',
                    renderpageno,
                    Score,
                    MM,
                    last_pianotick,
                    color_dark,
                    color_light,
                    pview,root,
                    BLACK))
                for rend in numofpages:
                    pview.postscript(file=f"/tmp/tmp{rend}.ps", 
                        x=rend * (Score['properties']['page-width'] * MM),
                        y=10000, 
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
        f = filedialog.asksaveasfile(mode='w', parent=root, filetypes=[("pdf Score", "*.pdf")], initialfile=Score['header']['title']['text'],
                                     initialdir='~/Desktop')
        if f:
            pslist = []
            if Score['properties']['engraver'] == 'pianoscript':
                print(f.name)
                counter = 0
                numofpages = range(engrave_pianoscript('export',
                        renderpageno,
                        Score,
                        MM,
                        last_pianotick,
                        color_dark,
                        color_light,
                        pview,root,
                        BLACK))
                for export in numofpages:
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
                    do_rend = subprocess.Popen(
                        f'''"C:/Program Files/gs/gs10.01.1/bin/gswin64c.exe" -dQUIET -dBATCH -dNOPAUSE -dFIXEDMEDIA -sPAPERSIZE=a4 -dEPSFitPage -sDEVICE=pdfwrite -sOutputFile="{f.name}.pdf" {' '.join(pslist)}''', shell=True)
                    do_rend.wait()
                    do_rend.terminate()    
                    for i in pslist:
                        os.remove(i.strip('"'))
                    f.close()
                    os.remove(f.name)
                except:
                    messagebox.showinfo(title="Can't export PDF!",
                                        message='''Be sure you have selected a valid path to "gswin64c.exe" in the gspath.json file that is located in the same folder as PianoScript program. You have to set the path+gswin64c.exe. example: "gspath":"C:/Program Files/gs/gs9.54.0/bin/gswin64c.exe". Then, restart PianoScript app.''')
            else:
                print(f.name)
                counter = 0
                numofpages = range(engrave_pianoscript_vertical('export',
                        renderpageno,
                        Score,
                        MM,
                        last_pianotick,
                        color_dark,
                        color_light,
                        pview,root,
                        BLACK))
                for export in numofpages:
                    counter += 1
                    print('printing page ', counter)
                    pview.postscript(file=f"{f.name}{counter}.ps", 
                        colormode='gray', 
                        x=export * (Score['properties']['page-width'] * MM), 
                        y=10000,
                        width=(Score['properties']['page-width'] * MM), 
                        height=(Score['properties']['page-height'] * MM),
                        rotate=False,
                        fontmap='-*-Courier-Bold-R-Normal--*-120-*')
                    pslist.append(str('"' + str(f.name) + str(counter) + '.ps' + '"'))
                try:
                    do_rend = subprocess.Popen(
                        f'''"C:/Program Files/gs/gs10.01.1/bin/gswin64c.exe" -dQUIET -dBATCH -dNOPAUSE -dFIXEDMEDIA -sPAPERSIZE=a4 -dEPSFitPage -sDEVICE=pdfwrite -sOutputFile="{f.name}.pdf" {' '.join(pslist)}''', shell=True)
                    do_rend.wait()
                    do_rend.terminate()    
                    for i in pslist:
                        os.remove(i.strip('"'))
                    f.close()
                    os.remove(f.name)
                except:
                    messagebox.showinfo(title="Can't export PDF!",
                                        message='''Be sure you have selected a valid path to "gswin64c.exe" in the gspath.json file that is located in the same folder as PianoScript program. You have to set the path+gswin64c.exe. example: "gspath":"C:/Program Files/gs/gs9.54.0/bin/gswin64c.exe". Then, restart PianoScript app.''')
    
    elif platform.system() == 'Darwin':
        f = filedialog.asksaveasfile(mode='w', parent=root, 
                                     filetypes=[("pdf Score", "*.pdf")], 
                                     initialfile=Score['header']['title']['text'],
                                     initialdir='~/Desktop')
        if f:
            pslist = []
            if Score['properties']['engraver'] == 'pianoscript':
                numofpages = range(engrave_pianoscript('export',
                    renderpageno,
                    Score,
                    MM,
                    last_pianotick,
                    color_dark,
                    color_light,
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
            else:
                numofpages = range(engrave_pianoscript_vertical('export',
                    renderpageno,
                    Score,
                    MM,
                    last_pianotick,
                    color_dark,
                    color_light,
                    pview,root,
                    BLACK))
                for rend in numofpages:
                    pview.postscript(file=f"tmp{rend}.ps",
                        x=rend * (Score['properties']['page-width'] * MM),
                        y=10000, 
                        width=Score['properties']['page-width'] * MM,
                        height=Score['properties']['page-height'] * MM, 
                        rotate=False,
                        fontmap='-*-Courier-Bold-R-Normal--*-120-*')
                    process = subprocess.Popen(
                        f'''pstopdf tmp{rend}.ps''', shell=True)
                    process.wait()
                    os.remove(f"tmp{rend}.ps")
                    pslist.append(f"tmp{rend}.pdf")
            cmd = 'pdfunite '
            for i in range(len(pslist)):
                cmd += pslist[i] + ' '
            cmd += '"%s"' % f.name
            process = subprocess.Popen(cmd, shell=True)
            process.wait()
            # remove temporary pdf page files
            for rend in numofpages:
                os.remove(f"tmp{rend}.pdf")
    do_engrave()

















def exportPostscript():

    f = filedialog.asksaveasfile(mode='w', 
        parent=root, 
        filetypes=[("postscript file", "*.ps")], 
        initialfile=Score['header']['title']['text'],
        initialdir='~/Desktop')

    if f:
        if Score['properties']['engraver'] == 'pianoscript':
            numofpages = range(engrave_pianoscript('export',
                renderpageno,
                Score,
                MM,
                last_pianotick,
                color_dark,
                color_light,
                pview,root,
                BLACK))
            for rend in numofpages:
                pview.postscript(file=f"{f.name[:-3]}{rend}.ps", 
                    x=10000,
                    y=rend * (Score['properties']['page-height'] * MM), 
                    width=Score['properties']['page-width'] * MM,
                    height=Score['properties']['page-height'] * MM, 
                    rotate=False,
                    fontmap='-*-Courier-Bold-R-Normal--*-120-*')
        else:
            numofpages = range(engrave_pianoscript_vertical('export',
                renderpageno,
                Score,
                MM,
                last_pianotick,
                color_dark,
                color_light,
                pview,root,
                BLACK))
            for rend in numofpages:
                pview.postscript(file=f"/tmp/tmp{rend}.ps", 
                    x=rend * (Score['properties']['page-width'] * MM),
                    y=10000, 
                    width=Score['properties']['page-width'] * MM,
                    height=Score['properties']['page-height'] * MM, 
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
            # on this scope we call the engrave function based on engraver:
            if Score['properties']['engraver'] == 'pianoscript':
                engrave_pianoscript('',
                    renderpageno,
                    Score,
                    MM,
                    last_pianotick,
                    color_dark,
                    color_light,
                    pview,root,
                    BLACK)
            if Score['properties']['engraver'] == 'pianoscript vertical':
                engrave_pianoscript_vertical('',
                    renderpageno,
                    Score,
                    MM,
                    last_pianotick,
                    color_dark,
                    color_light,
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
listbox_value = 8
def grid_selector(event='event'):
    global edit_grid, listbox_value

    for idx,i in enumerate(list_dur.curselection()):
        listbox_value = list_dur.get(i)
    # if event != 'event':
    #     listbox_value = event.keysym
    #     list_dur.select_set(int(event.keysym)-1)# implementing shortcuts in progress

    lengthdict = {1: 1024, 2: 512, 4: 256, 8: 128, 16: 64, 32: 32, 64: 16, 128: 8}
    edit_grid = ((lengthdict[int(listbox_value)] / int(divide_variable.get())) * int(times_variable.get()))

    root.focus()

def grideditor(event=''):
    '''
        This function runs the GridEditor class and 
        assigns the returning value to the Score object.
    '''
    global Score, last_pianotick
    edit = GridDialog(root,Score)
    Score = edit.processed_score
    last_pianotick = edit.last_pianotick
    do_pianoroll()
    do_engrave()


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

def transpose():
    '''
        the user selects the range(from bar x to bar y) and
        gives a integer to transpose all notes in the selection.
    '''
    user_input = AskString(root,'Transpose', HELP2).result
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
        "margin-staff1-left":10,
        "margin-staff1-right":10,
        "margin-staff2-left":10,
        "margin-staff2-right":10,
        "margin-staff3-left":10,
        "margin-staff3-right":10,
        "margin-staff4-left":10,
        "margin-staff4-right":10
    }
    draw_linebreak_editor(new_linebreak,
        editor,
        hbar,
        y_scale_percent,
        x_scale_quarter_mm,
        MM,
        color_dark,
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
                "margin-staff1-left":10,
                "margin-staff1-right":10,
                "margin-staff2-left":10,
                "margin-staff2-right":10,
                "margin-staff3-left":10,
                "margin-staff3-right":10,
                "margin-staff4-left":10,
                "margin-staff4-right":10
            }
            new_id += 1
            draw_linebreak_editor(new_linebreak,
                editor,
                hbar,
                y_scale_percent,
                x_scale_quarter_mm,
                MM,
                color_dark,
                color_highlight)
            Score['events']['line-break'].append(new_linebreak)
        c += 1
        if c > ui: 
            c = 1
            uidx += 1

    do_engrave()

def switch_hand_selection(e, direction):

    global Score

    for s in selection_buffer:

        for n in Score['events']['note']:
            if n['id'] == s['id']:
                if direction == 'l':
                    n['hand'] = 'l'
                else:
                    n['hand'] = 'r'
                
                # redraw the changed note on the editor:
                editor.delete(n['id'])
                draw_note_pianoroll(n, 
                            False, 
                            editor, 
                            hbar, 
                            y_scale_percent, 
                            x_scale_quarter_mm, 
                            MM, 
                            color_dark, 
                            BLACK, 
                            color_light, 
                            Score,
                            False,
                            True)
                update_drawing_order_editor(editor)
                do_engrave()











# # -------------
# # MODE TOOLBAR
# # -------------
# def mode_select(mode,i_mode):
    
#     global input_mode

#     modes = [
#     input_right_button,
#     input_left_button,
#     linebreak_button,
#     countline_button,
#     txt_button,
#     slur_button,
#     staffsizer_button,
#     repeats_button,
#     beam_button,
#     accidental_button
#     ]

#     for i,conf in enumerate(modes):
#         if i == mode:
#             conf.configure(bg=color_highlight)
#         else:
#             conf.configure(bg='#f0f0f0')

#     if mode == 0:
#         cursor = {
#             "id": 'cursor',
#             "time": edit_cursor[0],
#             "duration": edit_grid,
#             "pitch": edit_cursor[1],
#             "hand": 'r',
#             "x-offset": 0,
#             "y-offset": 0,
#             "stem-visible": True,
#             "accidental":0,
#             "staff":0
#         }
#         draw_note_pianoroll(cursor, 
#             True, 
#             editor, 
#             hbar, 
#             y_scale_percent, 
#             x_scale_quarter_mm, 
#             MM, 
#             color_dark, 
#             BLACK, 
#             color_light, 
#             Score)
#     elif mode == 1:
#         cursor = {
#             "id": 'cursor',
#             "time": edit_cursor[0],
#             "duration": edit_grid,
#             "pitch": edit_cursor[1],
#             "hand": 'l',
#             "x-offset": 0,
#             "y-offset": 0,
#             "stem-visible": True,
#             "accidental":0,
#             "staff":0
#         }
#         draw_note_pianoroll(cursor, 
#             True, 
#             editor, 
#             hbar, 
#             y_scale_percent, 
#             x_scale_quarter_mm, 
#             MM, 
#             color_dark, 
#             BLACK, 
#             color_light, 
#             Score)

#     input_mode = i_mode

# input_right_button.configure(command=lambda: [mode_select(0,'right'), noteinput_label.focus_force()])
# input_left_button.configure(command=lambda: [mode_select(1,'left'), noteinput_label.focus_force()])
# linebreak_button.configure(command=lambda: [mode_select(2,'linebreak'), noteinput_label.focus_force()])
# countline_button.configure(command=lambda: [mode_select(3,'countline'), noteinput_label.focus_force()])
# txt_button.configure(command=lambda: [mode_select(4,'text'), noteinput_label.focus_force()])
# slur_button.configure(command=lambda: [mode_select(5,'slur'), noteinput_label.focus_force()])
# staffsizer_button.configure(command=lambda: [mode_select(6,'staffsizer'), noteinput_label.focus_force()])
# repeats_button.configure(command=lambda: [mode_select(7,'repeats'), noteinput_label.focus_force()])
# beam_button.configure(command=lambda: [mode_select(8,'beamtool'), noteinput_label.focus_force()])
# accidental_button.configure(command=lambda: [mode_select(9,'accidental'), noteinput_label.focus_force()])

# root.bind('1', lambda e: [mode_select(0,'right'), noteinput_label.focus_force()])
# root.bind('2', lambda e: [mode_select(1,'left'), noteinput_label.focus_force()])
# root.bind('3', lambda e: [mode_select(2,'linebreak'), noteinput_label.focus_force()])
# root.bind('4', lambda e: [mode_select(3,'countline'), noteinput_label.focus_force()])
# root.bind('5', lambda e: [mode_select(4,'text'), noteinput_label.focus_force()])
# root.bind('6', lambda e: [mode_select(5,'slur'), noteinput_label.focus_force()])
# root.bind('7', lambda e: [mode_select(6,'staffsizer'), noteinput_label.focus_force()])
# root.bind('8', lambda e: [mode_select(7,'repeats'), noteinput_label.focus_force()])
# root.bind('9', lambda e: [mode_select(8,'beamtool'), noteinput_label.focus_force()])
# root.bind('0', lambda e: [mode_select(9,'accidental'), noteinput_label.focus_force()])

def space_shift(event):
    '''
        This is a switch for mode 1 & 2 (right and left)
    '''
    if input_mode in ['linebreak', 'select', 'text', 'countline', 'text', 'slur', 'staffsizer', 'repeats', 'beamtool', 'accidental']:
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
current_undo_index = 0
current_undo_levels = 0

def undo(event=''):
    global Score,current_undo_index
    print('undo...',current_undo_levels)
    if CtlZ:

        try: 
            Score = CtlZ[-2]
        except IndexError:
            Score = CtlZ[-1]
            print('default')

        do_engrave()
        threading.Thread(target=do_pianoroll()).start()

def redo(event=''):
    global Score,current_undo_index
    succeed = False
    print('redo...',current_undo_index)
    
    # first we try to do the redo
    # first we try to do the undo
    current_undo_index += 1
    Score = CtlZ[current_undo_index%len(CtlZ)]

    # if the undo succeeded we redraw the editor and do_render()
    if succeed:
        do_engrave()
        threading.Thread(target=do_pianoroll()).start()

def add_ctrl_z():
    #print('add_ctrl_z')
    
    global CtlZ,current_undo_levels,current_undo_index

    CtlZ.append(Score)
    current_undo_levels += 1
    current_undo_index += 1
    
    

def empty_ctrl_z():
    
    global CtlZ
    CtlZ = []
























def cycle_trough_pages(event):
    global renderpageno
    if platform.system() in ['Windows', 'Linux']:

        if event.num == 3:
            renderpageno += 1
        if event.num == 2:
            renderpageno = 0
    elif platform.system() == 'Darwin':

        if event.num == 2:
            renderpageno += 1
        if event.num == 3:
            renderpageno = 0
    if event.num == 1:
        renderpageno -= 1

    do_engrave()

def cycle_trough_pages_button(event=''):
    
    global renderpageno

    if event == '<':
        renderpageno -= 1
    else:
        renderpageno += 1
    do_engrave()
# nextpage_button.configure(command=lambda: cycle_trough_pages_button(':)'))
# prevpage_button.configure(command=cycle_trough_pages_button)





























# --------------------------------------------------------
# Cut Copy Paste
# --------------------------------------------------------
def cut_selection(e=''):
    print('cut...')
    global copycut_buffer, active_selection, file_changed
    file_changed = True
    copycut_buffer = []
    lowest_time_from_selection = 0
    lowest_assign = True
    for note in Score['events']['note']:
        if note['id'] in selection_tags:
            if lowest_assign:
                lowest_time_from_selection = note['time']
                lowest_assign = False
            note['time'] -= lowest_time_from_selection
            copycut_buffer.append(note)
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
    global copycut_buffer 
    copycut_buffer = []
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
                "notestop":note['notestop'],
                "accidental":note['accidental'],
                "staff":int(staffselect_variable.get())
            }
            copycut_buffer.append(new)

def paste_selection(e=''):
    print('paste...')
    global new_id, copycut_buffer, file_changed
    file_changed = True
    for e in copycut_buffer:
        if 'note' in e['id']:
            new = {
                "id":"note%i"%new_id,
                "time":mouse_time+e['time'],
                "duration":e['duration'],
                "pitch":e['pitch'],
                "hand":e['hand'],
                "stem-visible":e['stem-visible'],
                "type":e['type'],
                "notestop":e['notestop'],
                "accidental":e['accidental'],
                "staff":int(staffselect_variable.get())-1
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
                color_dark, 
                BLACK, 
                color_light, 
                Score)
            update_drawing_order_editor(editor)
    do_engrave()

def select_all(event=''):
    
    ...
































def transpose_up(event=''):
    global new_id, selection_buffer
    for e in selection_buffer:
        if 'note' in e['id']:
            e['pitch'] += 1
            if e['pitch'] > 88:
                e['pitch'] = 88
            draw_note_pianoroll(e,
                False, 
                editor, 
                hbar, 
                y_scale_percent, 
                x_scale_quarter_mm, 
                MM, 
                color_dark, 
                BLACK, 
                color_light, 
                Score,
                False,
                True)
            update_drawing_order_editor(editor)
    do_engrave()

def transpose_down(event=''):
    global new_id, selection_buffer
    for e in selection_buffer:
        if 'note' in e['id']:
            e['pitch'] -= 1
            if e['pitch'] < 1:
                e['pitch'] = 1
            draw_note_pianoroll(e,
                False, 
                editor, 
                hbar, 
                y_scale_percent, 
                x_scale_quarter_mm, 
                MM, 
                color_dark, 
                BLACK, 
                color_light, 
                Score,
                False,
                True)
            update_drawing_order_editor(editor)
    do_engrave()


def move_selection_left(event=''):
    global new_id, selection_buffer
    for e in selection_buffer:
        if 'note' in e['id']:
            e['time'] -= edit_grid
            if e['time'] < 0:
                e['time'] = 0
            draw_note_pianoroll(e,
                False, 
                editor, 
                hbar, 
                y_scale_percent, 
                x_scale_quarter_mm, 
                MM, 
                color_dark, 
                BLACK, 
                color_light, 
                Score,
                False,
                True)
            update_drawing_order_editor(editor)
    do_engrave()

def move_selection_right(event=''):
    global new_id, selection_buffer
    for e in selection_buffer:
        if 'note' in e['id']:
            e['time'] += edit_grid
            if e['time'] > last_pianotick:
                e['time'] = last_pianotick
            draw_note_pianoroll(e,
                False, 
                editor, 
                hbar, 
                y_scale_percent, 
                x_scale_quarter_mm, 
                MM, 
                color_dark, 
                BLACK, 
                color_light, 
                Score,
                False,
                True)
            update_drawing_order_editor(editor)
    do_engrave()


def quantize_selection(e=''):
    
    global Score

    for s in selection_buffer:

        
        for n in Score['events']['note']:
            # quantize start in savefile
            if n['id'] == s['id']:
                start = n['time']
                end = n['time'] + n['duration']
                n['time'] = round(start / edit_grid) * edit_grid
                n['duration'] = end - n['time']
            # quantize end in savefile
            if n['id'] == s['id']:
                start = n['time']
                end = n['time'] + n['duration']
                end = round(end / edit_grid) * edit_grid
                n['duration'] = end - n['time']

            # redraw the quantized note
            if n['id'] == s['id']:
                draw_note_pianoroll(n,
                False, 
                editor, 
                hbar, 
                y_scale_percent, 
                x_scale_quarter_mm, 
                MM, 
                color_dark, 
                BLACK, 
                color_light, 
                Score,
                False,
                True)

    do_engrave()
    update_drawing_order_editor(editor)



def quantize(Score):
    
    user_input = QuantizeDialog(root, 'Quantize...','Choose what you want to quantize. \nThe notes are quantized to the current selected grid \nso you may change the grid before choosing one \nof the options.').result
    if user_input:
        user_input = 'start'
    if user_input == False:
        user_input = 'duration'

    # quantizing notestart
    if user_input == 'start':

        for n in Score['events']['note']:

            start = n['time']
            end = n['time'] + n['duration']
            n['time'] = round(start / edit_grid) * edit_grid
            n['duration'] = end - n['time']

    # quantizing duration
    if user_input == 'duration':

        for n in Score['events']['note']:

            start = n['time']
            end = n['time'] + n['duration']
            end = round(end / edit_grid) * edit_grid
            n['duration'] = end - n['time']

    do_engrave()
    do_pianoroll()




def options_editor():
    global Score
    Score = OptionsDialog(root, Score).score
    do_engrave()


## engraver switch
def engraver_switch(event=''):
    global Score

    if Score['properties']['engraver'] == 'pianoscript':
        Score['properties']['engraver'] = 'pianoscript vertical'
        engraver_button.configure(text='H')
    else:
        Score['properties']['engraver'] = 'pianoscript'
        engraver_button.configure(text='V')
    do_engrave()



# --------------------------------------------------------
# MENU
# --------------------------------------------------------
menubar = Menu(root, relief='flat', bg=color_gui_base, fg=color_light, font=('courier', 16))
root.config(menu=menubar)
fileMenu = Menu(menubar, tearoff=0)
fileMenu.add_command(label='New [ctl+n]', command=new_file, font=('courier', 16))
fileMenu.add_command(label='Open [ctl+o]', command=load_file, font=('courier', 16))
fileMenu.add_command(label='Save [ctl+s]', command=save, font=('courier', 16))
fileMenu.add_command(label='Save as... [alt+s]', command=save_as, font=('courier', 16))
fileMenu.add_separator()
fileMenu.add_command(label='Load midi [ctl+m]', command=midi_import, font=('courier', 16))
fileMenu.add_separator()
fileMenu.add_command(label="Export ps", command=exportPostscript, font=('courier', 16))
fileMenu.add_command(label="Export pdf [ctl+e]", command=exportPDF, font=('courier', 16))
fileMenu.add_command(label="Export midi*", command=lambda: midiexport(root,Score), font=('courier', 16))
fileMenu.add_separator()
fileMenu.add_command(label="Grid editor... [g]", underline=None, command=grideditor, font=('courier', 16))
fileMenu.add_command(label="Score options... [s]", underline=None, command=options_editor, font=('courier', 16))
fileMenu.add_separator()
fileMenu.add_command(label="Exit", underline=None, command=quit_editor, font=('courier', 16))
menubar.add_cascade(label="File", underline=None, menu=fileMenu, font=('courier', 16))
selectionMenu = Menu(menubar, tearoff=0)
selectionMenu.add_command(label="Cut [ctl+x]", underline=None, command=cut_selection, font=('courier', 16))
selectionMenu.add_command(label="Copy [ctl+c]", underline=None, command=copy_selection, font=('courier', 16))
selectionMenu.add_command(label="Paste [ctl+v]", underline=None, command=paste_selection, font=('courier', 16))
selectionMenu.add_separator()
selectionMenu.add_command(label="Select all [ctl+a]", underline=None, command=select_all, font=('courier', 16))
menubar.add_cascade(label="Selection", underline=None, menu=selectionMenu, font=('courier', 16))
toolsMenu = Menu(menubar, tearoff=1)
toolsMenu.add_command(label='Redraw editor', command=lambda: do_pianoroll(), font=('courier', 16))
toolsMenu.add_command(label='Quantize', command=lambda: quantize(Score), font=('courier', 16))
toolsMenu.add_command(label='Add quick line breaks', command=lambda: add_quick_linebreaks(), font=('courier', 16))
toolsMenu.add_command(label='Transpose', command=lambda: transpose(), font=('courier', 16))
menubar.add_cascade(label="Tools", underline=None, menu=toolsMenu)
menubar.add_command(label='< previous', command=lambda: cycle_trough_pages_button('<'), background='grey', activebackground=color_highlight)
menubar.add_command(label='next >', command=lambda: cycle_trough_pages_button('>'), background='grey', activebackground=color_highlight)





# --------------------------------------------------------
# BIND (shortcuts)
# --------------------------------------------------------
root.bind('<Escape>', quit_editor)
editor.bind('<Motion>', lambda event: mouse_handling(event, 'motion'))
editor.bind('<Button-1>', lambda event: mouse_handling(event, 'btn1click'))
editor.bind('<ButtonRelease-1>', lambda event: mouse_handling(event, 'btn1release'))
if platform.system() == 'Linux' or platform.system() == 'Windows':
    editor.bind('<Control-Button-1>', lambda event: mouse_handling(event, 'ctl-click-btn1'))
    editor.bind('<Double-Button-1>', lambda event: mouse_handling(event, 'double-btn1'))
    editor.bind('<Button-2>', lambda event: mouse_handling(event, 'btn2click'))
    editor.bind('<ButtonRelease-2>', lambda event: mouse_handling(event, 'btn2release'))
    editor.bind('<Button-3>', lambda event: mouse_handling(event, 'btn3click'))
    editor.bind('<ButtonRelease-3>', lambda event: mouse_handling(event, 'btn3release'))
    #toolbarpanel.bind('<Button-3>', lambda e: do_popup(e, setMenu))
    pview.bind('<Button-1>', lambda e: cycle_trough_pages(e))
    pview.bind('<Button-3>', lambda e: cycle_trough_pages(e))
if platform.system() == 'Darwin':
    editor.bind('<Control-Button-1>', lambda event: mouse_handling(event, 'ctl-click-btn1'))
    editor.bind('<Double-Button-1>', lambda event: mouse_handling(event, 'double-btn1'))
    editor.bind('<Button-3>', lambda event: mouse_handling(event, 'btn2click'))
    editor.bind('<ButtonRelease-3>', lambda event: mouse_handling(event, 'btn2release'))
    editor.bind('<Button-2>', lambda event: mouse_handling(event, 'btn3click'))
    editor.bind('<ButtonRelease-2>', lambda event: mouse_handling(event, 'btn3release'))
    #toolbarpanel.bind('<Button-2>', lambda e: do_popup(e, setMenu))
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
    elements_treeview.bind("<5>", lambda event: elements_treeview.yview('scroll', 1, 'items'))
    elements_treeview.bind("<4>", lambda event: elements_treeview.yview('scroll', -1, 'units'))
    divide_spin.bind("<5>", lambda event: divide_spin.xview('scroll', 1, 'units'))
    divide_spin.bind("<4>", lambda event: divide_spin.xview('scroll', -1, 'units'))
def function():
    pass
# windows scroll
if platform.system() == 'Windows':
    editor.bind("<MouseWheel>", lambda event: editor.xview('scroll', -round(event.delta / 120), 'units'))
    pview.bind("<MouseWheel>", lambda event: pview.yview('scroll', -round(event.delta / 120), 'units'))
    elements_treeview.bind("<MouseWheel>", lambda event: elements_treeview.yview('scroll', -round(event.delta / 120), 'units'))
list_dur.bind('<<ListboxSelect>>', grid_selector)
divide_spin.configure(command=lambda: grid_selector())
divide_spin.bind('<Return>', lambda event: grid_selector())
times_spin.configure(command=lambda: grid_selector())
times_spin.bind('<Return>', lambda event: grid_selector())
master_paned.bind('<ButtonRelease-1>', lambda event: do_engrave(event))
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
#root.bind('<Control-z>', undo)
#root.bind('<Control-Z>', redo)
root.bind('<Control-x>', cut_selection)
root.bind('<Control-X>', cut_selection)
root.bind('<Control-c>', copy_selection)
root.bind('<Control-C>', copy_selection)
root.bind('<Control-v>', paste_selection)
root.bind('<Control-V>', paste_selection)
root.bind('<Control-a>', select_all)
root.bind('<Control-A>', select_all)
root.bind('<Control-n>', new_file)
root.bind('<Control-N>', new_file)
root.bind('<Control-o>', load_file)
root.bind('<Control-O>', load_file)
root.bind('<Control-s>', save)
root.bind('<Control-S>', save_as)
root.bind('<Control-r>', do_pianoroll)
root.bind('<Control-R>', do_pianoroll)
root.bind('<Control-e>', exportPDF)
root.bind('<Up>', transpose_up)
root.bind('<Down>', transpose_down)
root.bind('<Key-g>', grideditor)
root.bind('<Key-q>', lambda e: quantize_selection(Score))
root.bind(',', lambda e: switch_hand_selection(e,'l'))
root.bind('.', lambda e: switch_hand_selection(e,'r'))
#root.bind('p', lambda e: play_midi(e, Score, 'test2.mid', root))
root.bind('s', lambda e: options_editor())
root.bind('<Left>', move_selection_left)
root.bind('<Right>', move_selection_right)  

# spinbox on scroll + or -
def spin_scroll_linux(ev_type, spinvariable, range):

    # set value
    value = int(spinvariable.get())
    if ev_type == 'up':
        spinvariable.set(value + 1)
    else:
        spinvariable.set(value - 1)

    # check if value is in range
    value = int(spinvariable.get())
    if value < range[0]:
        spinvariable.set(range[0])
    elif value > range[1]:
        spinvariable.set(range[1])

    # update functions
    if range == (1,99):
        grid_selector()
    if range == (1,4):
        do_pianoroll()

def spin_scroll_macos(event, spinvariable, range):
    
    # update spin
    value = int(spinvariable.get())
    if event.delta > 0 and not value >= range[1]:
        spinvariable.set(value + 1)
    elif event.delta < 0 and not value <= range[0]:
        spinvariable.set(value - 1)

    # update functions
    if range == (1,99): 
        grid_selector()
    if range == (1,4):
        do_pianoroll()


if platform.system() == 'Linux':
    staffselect_spin.bind('<4>', lambda e: spin_scroll_linux('up',staffselect_variable,(1,4)))
    staffselect_spin.bind('<5>', lambda e: spin_scroll_linux('down',staffselect_variable,(1,4)))
    divide_spin.bind('<4>', lambda e: spin_scroll_linux('up',divide_variable,(1,99)))
    divide_spin.bind('<5>', lambda e: spin_scroll_linux('down',divide_variable,(1,99)))
    times_spin.bind('<4>', lambda e: spin_scroll_linux('up',times_variable,(1,99)))
    times_spin.bind('<5>', lambda e: spin_scroll_linux('down',times_variable,(1,99)))
if platform.system() == 'Darwin' or platform.system() == 'Windows':
    staffselect_spin.bind('<MouseWheel>', lambda e: spin_scroll_macos(e,staffselect_variable,(1,4)))
    divide_spin.bind('<MouseWheel>', lambda e: spin_scroll_macos(e,divide_variable,(1,99)))
    times_spin.bind('<MouseWheel>', lambda e: spin_scroll_macos(e,times_variable,(1,99)))



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

    #main_editor = MainEditor(editor, elements_treeview, Score)
    new_file()
    #test_file()
    root.mainloop()

