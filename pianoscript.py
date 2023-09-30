#!python3.11
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

# third party imports
from tkinter import Tk, Menu
import platform

# own imports code :)
from imports.editor.editor import MainEditor
from imports.gui.gui import Gui
from imports.colors import color_light, color_gui_light, color_highlight
from imports.editor.mouse_handling import MouseHandling
from imports.editor.kbd_handling import Keyboard
from imports.gui.options_dialog import OptionsDialog
from imports.engraver.thread_engraver import ThreadEngraver
from imports.engraver.engraver_pianoscript import engrave_pianoscript_vertical
from imports.tools import root_update
from imports.editor.ctlz import CtlZ
from imports.midi.midi import Midi
from imports.editor.selectoperations import SelectOperations

class App:

    def __init__(self):
        
        # root
        self.root = Tk()

        # gui
        self.gui = Gui(master=self.root)
        self.root.update()
        self.gui.editor.update()

        # the self.data stores all data from the app in one dict:
        self.io = {
            # root window
            'root':self.root,
            # main_frame
            'main_frame':self.gui.main_frame,
            # panels:
            'toolbarpanel':self.gui.leftpanel,
            'editorpanel':self.gui.editorpanel,
            'printviewpanel':self.gui.printpanel,
            # Paned widget
            'main_paned':self.gui.main_paned,
            # editor canvas
            'editor':self.gui.editor,
            # scrollbar
            'sbar':self.gui.sbar,
            # printview canvas
            'pview':self.gui.pview,
            # the curstomized elements tree widget
            'tree':self.gui.treeview,
            # gridselector
            'grid_selector':self.gui.grid_selector,
            # the score object where all score data is stored (the savefile)
            'score':{},
            # this class regulates all mouse related handlings
            'mouse_handling':MouseHandling(),
            # the last pianotick of the score
            'last_pianotick':0,
            # used to give every element a unique id
            'new_tag':0,
            # the current selected grid from the grid selector
            'snap_grid':128,
            # zoom setting in the y axis; we define the size of one pianotick in px on the screen
            'ticksizepx':.6,
            # 1 == the staff is the width of the editor canvas. in it's default value the staff == 80% of the editor width.
            'xscale':.7,
            # all info for the mouse
            'mouse':{
                'x':0, # x position of the mouse in the editor view
                'y':0, # y position of the mouse in the editor view
                'ex':0, # event x note position of the mouse in the editor view
                'ey':0, # event y pianotick position of the mouse in the editor view
                'button1':False, # True if the button is clicked and hold, False if not pressed
                'button2':False, # ...
                'button3':False # ...
            },
            # keep track wether an object on the editor is clicked; this variable is the 
            # unique id from a clicked object on the editor canvas if an object is clicked+hold
            'hold_tag':'',
            'keyboard':{ # keep track wheter shift or ctl is pressed
                'shift':False,
                'ctl':False,
            },
            'selection':{ # everything about selection
                'rectangle_on':False,
                # True if there is a active selection
                'active':False,
                # coords for the selection rectangle
                'x1':None,
                'y1':None,
                'x2':None,
                'y2':None,
                # the buffer that holds any selected element; it's a dictionary that holds the structure of the 'events' folder in a score file
                'selection_buffer':{},
                # the buffer that holds any copied or cutted selection; same structure as above
                'copycut_buffer':{},
                # all event types that are alowed to copy, cut, paste
                'copy_types':['note', 'ornament', 'beam', 'countline', 'slur', 'text', 'pedal'],
                # all event types that are alowed to transpose
                'transpose_types':['note', 'text', 'ornament',],
                # all event types that are alowed to move forward or backward in time
                'move_types':['note', 'ornament', 'beam', 'countline', 'slur', 'text', 'pedal']
            },
            # a mm in pixels on the screen
            'mm': self.root.winfo_fpixels('1m'),
            'editor_width': self.gui.editor.winfo_width(),
            'editor_height': self.gui.editor.winfo_height(),
            # keeping track of the editor_width if it's changed in width.
            'old_editor_width':1,
            # False if the mouse pointer is not on the editor
            'cursor_on_editor':True,
            # the start tick from the viewport
            'view_start_tick':0,
            # the end tick from the viewport
            'view_end_tick':8192,
            # a list to keep track of the objects that are on the canvas. it are tags from create_line(), create_polygon() etc...
            'drawn_obj':[],
            # edit buffer; holds an event obj (dict) if we are editing an object, None in idle
            'edit_obj':None,
            # the savefilesystem variables:
            'savefile_system':{
                'filepath':'New',
                'filechanged':False
            },
            # editor settings:
            'editor_settings':{
                'note_color':'#aaa' 
            },
            # True if app is in idle
            'idle':False,
            # right-left switch for the note modes
            'hand':'r',
            # page counter that keeps track of the current page view in the printview
            'pageno':0,
            # the render type is 'normal' or 'export'
            'render_type':'normal'
        }

        # editor
        self.main_editor = MainEditor(self.io)
        self.io['main_editor'] = self.main_editor

        # set scroll
        self.io['editor'].yview('scroll', -10, 'unit')

        # keyboard binding
        self.keyboard = Keyboard(self.io, self.main_editor)

        # engraver
        self.engraver = ThreadEngraver(process=engrave_pianoscript_vertical, io=self.io)
        self.engraver.start()
        self.io['engraver'] = self.engraver

        self.io['root'].bind('<Configure>', self.io['engraver'].trigger_render())

        # printview auto width fit page on screen
        root_update(self.io)

        # ctl-z class
        self.io['ctlz'] = CtlZ(self.io)

        # selection operations class
        self.io['selectoperations'] = SelectOperations(self.io)

        # midi class
        self.io['midi'] = Midi(self.io)

        # menu (written in this area because commands are not accessable inside the GUI class, can't set it later due to limitations of tkinter)
        self.font = ('courier', 16, 'bold')
        self.menubar = Menu(self.root, relief='flat', bg=color_gui_light, fg=color_light, font=self.font)
        self.root.config(menu=self.menubar)
        self.fileMenu = Menu(self.menubar, tearoff=2)
        self.fileMenu.add_command(label='New [ctl+n]', command=self.main_editor.new, font=self.font)
        self.fileMenu.add_command(label='Open [ctl+o]', command=self.main_editor.load, font=self.font)
        self.fileMenu.add_command(label='Save [ctl+s]', command=self.main_editor.save, font=self.font)
        self.fileMenu.add_command(label='Save as... [alt+s]', command=self.main_editor.saveas, font=self.font)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Load midi [ctl+m]', command=self.io['midi'].load_midi, font=self.font)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Export ps", command=None, font=self.font)
        self.fileMenu.add_command(label="Export pdf [ctl+e]", command=None, font=self.font)
        self.fileMenu.add_command(label="Export midi*", command=None, font=self.font)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Grid editor... [g]", underline=None, command=None, font=self.font)
        self.fileMenu.add_command(label="Score options... [s]", underline=None, command=lambda: OptionsDialog(self.root, self.io), font=self.font)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", underline=None, command=self.quit, font=self.font)
        self.menubar.add_cascade(label="File", underline=None, menu=self.fileMenu, font=self.font)
        self.menubar.add_command(label='< previous', command=self.io['engraver'].prevpage, background='grey', activebackground=color_highlight)
        self.menubar.add_command(label='next >', command=self.io['engraver'].nextpage, background='grey', activebackground=color_highlight)

        if platform.system() in ['Windows', 'Linux']:
	        self.io['main_frame'].bind('<Configure>', lambda e: root_update(self.io, e))
	        self.io['main_paned'].bind('<Configure>', lambda e: root_update(self.io, e))
        
        self.root.bind('<Escape>', self.quit)

    def run(self):
        '''In run() we go into the mainloop of the app'''
        self.root.mainloop()

    def quit(self, event=''):
        
        # file-save-check
        ...

        # quit 
        self.root.destroy()
        



if __name__ == '__main__':
    app = App()
    app.run()