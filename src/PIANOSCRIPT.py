'''
    This is the main file of the PianoScript project. This file contains:
        - global variable storage
        - tkinter GUI design
        - render management
        - binds (binding of user events)
        - tkinter mainloop
'''

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

from file_management import *
from render_management import *













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

# colors
color_basic_gui = '#444444'
color_right_midinote = '#666666'
color_left_midinote = '#666666'
color_editor_canvas = '#999999'#d9d9d9#fdffd1
color_highlight = '#03a1fc'#a6a832
color_notation_editor = 'black'












# ----
# GUI
# ----
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














# -----
# BIND
# -----
root.bind('<Escape>', lambda e: quit_editor(e, thread_auto_render))
editor.bind('<Motion>', lambda event: mouse_handling(event, 'motion'))
editor.bind('<Button-1>', lambda event: mouse_handling(event, 'btn1click'))
editor.bind('<ButtonRelease-1>', lambda event: mouse_handling(event, 'btn1release'))
editor.bind('<Double-Button-1>', lambda event: mouse_handling(event, 'double-btn1'))
editor.bind('<Button-2>', lambda event: mouse_handling(event, 'btn2click'))
editor.bind('<ButtonRelease-2>', lambda event: mouse_handling(event, 'btn2release'))
editor.bind('<Button-3>', lambda event: mouse_handling(event, 'btn3click'))
editor.bind('<ButtonRelease-3>', lambda event: mouse_handling(event, 'btn3release'))

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

#list_dur.bind('<<ListboxSelect>>', grid_selector)
divide_spin.configure(command=lambda: grid_selector())
divide_spin.bind('<Return>', lambda event: grid_selector())
times_spin.configure(command=lambda: grid_selector())
times_spin.bind('<Return>', lambda event: grid_selector())

#midpanel.bind('<ButtonRelease-1>', lambda event: do_engrave(event))

root.bind('<Key-1>', lambda e: mode_select(1))
root.bind('<Key-2>', lambda e: mode_select(2))
root.bind('<Key-3>', lambda e: mode_select(3))
root.bind('<Key-4>', lambda e: mode_select(4))

#root.bind('<KeyPress-space>', space_shift)
#root.bind('<KeyRelease-space>', space_shift)

help_button1.configure(command=lambda: messagebox.showinfo('Grid map editor help', HELP1))
help_button2.configure(command=lambda: messagebox.showinfo('System margin editor help', HELP2))
help_button3.configure(command=lambda: messagebox.showinfo('Measure division editor help', HELP3))

editor.bind('<Leave>', lambda e: editor.delete('cursor'))













# --------------------------------------------------------
# MENU
# --------------------------------------------------------
menubar = Menu(root, relief='flat', bg=color_basic_gui, fg='white', font=('courier', 14))
root.config(menu=menubar)

fileMenu = Menu(menubar, tearoff=0, bg=color_basic_gui, fg='white', font=('courier', 14))

fileMenu.add_command(label='new', command=None)
fileMenu.add_command(label='load', command=lambda: load_file(root))
fileMenu.add_command(label='save', command=None)
fileMenu.add_command(label='save as...', command=None)

fileMenu.add_separator()

fileMenu.add_command(label='import midi', command=None)

fileMenu.add_separator()

fileMenu.add_command(label="export ps", command=None)
fileMenu.add_command(label="export pdf", command=None, underline=None)
fileMenu.add_command(label="export midi", command=None, underline=None)

fileMenu.add_separator()

fileMenu.add_command(label="exit", underline=None, command=None)
menubar.add_cascade(label="File", underline=None, menu=fileMenu)

setMenu = Menu(menubar, tearoff=1, bg=color_basic_gui, fg='white', font=('courier', 14))
setMenu.add_command(label='title', command=lambda: set_titles('title'))
setMenu.add_command(label='composer', command=lambda: set_titles('composer'))
setMenu.add_command(label='copyright', command=lambda: set_titles('copyright'))
setMenu.add_separator()
setMenu.add_command(label='global scale', command=None)
setMenu.add_command(label='page margins', command=None)
menubar.add_cascade(label="Set", underline=None, menu=setMenu)

optionsMenu = Menu(menubar, tearoff=1, bg=color_basic_gui, fg='white', font=('courier', 14))
optionsMenu.add_command(label='redraw editor', command=lambda: draw_pianoroll())
menubar.add_cascade(label="Options", underline=None, menu=optionsMenu)





















if __name__ == '__main__':
    ...#test_file()
    thread_auto_render = AutoRender()
    thread_auto_render.start()

# tkinter mainloop:
root.mainloop()