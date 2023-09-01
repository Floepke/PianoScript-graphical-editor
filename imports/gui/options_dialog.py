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

'''
Dialog where we can change the io['score'] options. The dialog allows the user 
to change the properties of the save file(io['score']).
'''

from tkinter import Tk, Button, Label, Toplevel, Entry, Frame, Text, Scale, Listbox, Checkbutton, IntVar, Checkbutton, Spinbox, StringVar, ttk
from imports.colors import color_light, color_dark, color_gui_light, color_gui_dark, color_highlight


class OptionsDialog:
    
    def __init__(self, parent, io):
        self.parent = parent
        self.close = False
        self.score = io['score']

        # create the popup window
        self.popup = Toplevel(self.parent)
        self.popup.title('PianoScript - Score Options')
        self.popup.wm_attributes("-topmost", 1)

        # tab
        self.notebookframe = Frame(self.popup, bg='#eee8d5')
        self.notebookframe.pack(padx=10, pady=10, fill='both')
        self.notebook = ttk.Notebook(self.notebookframe)
        self.notebook.pack(side='left',padx=5,pady=5, expand=True)
        
        # tab 1; titles
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Titles')
        self.title_label = Label(self.tab1, text='Title:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.title_label.grid(row=0, column=0, sticky='e')
        self.title_entry = Entry(self.tab1, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.title_entry.grid(row=0, column=1)
        self.composer_label = Label(self.tab1, text='Composer:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.composer_label.grid(row=1, column=0, sticky='e')
        self.composer_entry = Entry(self.tab1, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.composer_entry.grid(row=1, column=1)
        self.copyright_label = Label(self.tab1, text='Copyright:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.copyright_label.grid(row=2, column=0, sticky='e')
        self.copyright_entry = Entry(self.tab1, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.copyright_entry.grid(row=2, column=1)

        #tab 2; layout
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Layout')
        self.threelinescale_label = Label(self.tab2, text='Three line thickness/scale:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.threelinescale_label.grid(row=0, column=0, ipadx=10, sticky='e')
        self.threelinescale_entry = Entry(self.tab2, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.threelinescale_entry.grid(row=0, column=1, ipadx=10)
        self.drawscale_label = Label(self.tab2, text='Global scale:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.drawscale_label.grid(row=1, column=0, ipadx=10, sticky='e')
        self.drawscale_entry = Entry(self.tab2, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.drawscale_entry.grid(row=1, column=1, ipadx=10)
        self.pagewidth_label = Label(self.tab2, text='Page width(mm):', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.pagewidth_label.grid(row=2, column=0, ipadx=10, sticky='e')
        self.pagewidth_entry = Entry(self.tab2, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.pagewidth_entry.grid(row=2, column=1, ipadx=10)
        self.pageheight_label = Label(self.tab2, text='Page height(mm):', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.pageheight_label.grid(row=3, column=0, ipadx=10, sticky='e')
        self.pageheight_entry = Entry(self.tab2, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.pageheight_entry.grid(row=3, column=1, ipadx=10)
        self.headerheight_label = Label(self.tab2, text='Header height(mm):', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.headerheight_label.grid(row=4, column=0, ipadx=10, sticky='e')
        self.headerheight_entry = Entry(self.tab2, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.headerheight_entry.grid(row=4, column=1, ipadx=10)
        self.footerheight_label = Label(self.tab2, text='Footer height(mm):', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.footerheight_label.grid(row=5, column=0, ipadx=10, sticky='e')
        self.footerheight_entry = Entry(self.tab2, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.footerheight_entry.grid(row=5, column=1, ipadx=10)
        self.pagemargl_label = Label(self.tab2, text='Page margin left(mm):', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.pagemargl_label.grid(row=6, column=0, ipadx=10, sticky='e')
        self.pagemargl_entry = Entry(self.tab2, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.pagemargl_entry.grid(row=6, column=1, ipadx=10)
        self.pagemargr_label = Label(self.tab2, text='Page margin right(mm):', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.pagemargr_label.grid(row=7, column=0, ipadx=10, sticky='e')
        self.pagemargr_entry = Entry(self.tab2, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.pagemargr_entry.grid(row=7, column=1, ipadx=10)
        self.pagemargu_label = Label(self.tab2, text='Page margin up(mm):', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.pagemargu_label.grid(row=8, column=0, ipadx=10, sticky='e')
        self.pagemargu_entry = Entry(self.tab2, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.pagemargu_entry.grid(row=8, column=1, ipadx=10)
        self.pagemargd_label = Label(self.tab2, text='Page margin down(mm):', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.pagemargd_label.grid(row=9, column=0, ipadx=10, sticky='e')
        self.pagemargd_entry = Entry(self.tab2, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.pagemargd_entry.grid(row=9, column=1, ipadx=10)
        self.leftcolor_label = Label(self.tab2, text='left hand midinote color:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.leftcolor_label.grid(row=10, column=0, ipadx=10, sticky='e')
        self.leftcolor_entry = Entry(self.tab2, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.leftcolor_entry.grid(row=10, column=1, ipadx=10)
        self.rightcolor_label = Label(self.tab2, text='right hand midinote color:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.rightcolor_label.grid(row=11, column=0, ipadx=10, sticky='e')
        self.rightcolor_entry = Entry(self.tab2, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.rightcolor_entry.grid(row=11, column=1, ipadx=10)
        
        self.blackstyle_label = Label(self.tab2, text='Black note style:', 
            font=('Courier', 16), bg=color_light, fg=color_dark)
        self.blackstyle_label.grid(row=12, column=0, ipadx=10, sticky='e')
        self.blackstyle_variable = StringVar()
        self.blackstyle_combo = ttk.Combobox(self.tab2, font=('Courier', 16),
            textvariable=self.blackstyle_variable, 
            values=['PianoScript', 'Klavarskribo'], 
            state='readonly', width=self.rightcolor_entry['width']-1)
        self.blackstyle_combo.grid(row=12, column=1, ipadx=10, sticky='e')
        self.blackstyle_combo.current(0)

        self.stopstyle_label = Label(self.tab2, text='Stop sign style:', 
            font=('Courier', 16), bg=color_light, fg=color_dark)
        self.stopstyle_label.grid(row=13, column=0, ipadx=10, sticky='e')
        self.stopstyle_variable = StringVar()
        self.stopstyle_combo = ttk.Combobox(self.tab2, font=('Courier', 16),
            textvariable=self.stopstyle_variable, 
            values=['PianoScript', 'Klavarskribo'], 
            state='readonly', width=self.rightcolor_entry['width']-1)
        self.stopstyle_combo.grid(row=13, column=1, ipadx=10, sticky='e')
        self.stopstyle_combo.current(0)

        # tab 3; elements on/off
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Elements')
        self.minipiano_variable = IntVar()
        self.minipiano_label = Label(self.tab3, text='Piano-keyboard:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.minipiano_label.grid(row=0, column=0, ipadx=10, sticky='e')
        self.minipiano_checkbutton = Checkbutton(self.tab3, variable=self.minipiano_variable, bg=color_light, fg=color_dark)
        self.minipiano_checkbutton.grid(row=0, column=1, ipadx=10)
        
        self.staff_variable = IntVar()
        self.staff_label = Label(self.tab3, text='Staff:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.staff_label.grid(row=1, column=0, ipadx=10, sticky='e')
        self.staff_checkbutton = Checkbutton(self.tab3, variable=self.staff_variable, bg=color_light, fg=color_dark)
        self.staff_checkbutton.grid(row=1, column=1, ipadx=10, sticky='e')

        self.stem_variable = IntVar()
        self.stem_label = Label(self.tab3, text='Stem:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.stem_label.grid(row=2, column=0, ipadx=10, sticky='e')
        self.stem_checkbutton = Checkbutton(self.tab3, variable=self.stem_variable, bg=color_light, fg=color_dark)
        self.stem_checkbutton.grid(row=2, column=1, ipadx=10, sticky='e')

        self.beam_variable = IntVar()
        self.beam_label = Label(self.tab3, text='Beam:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.beam_label.grid(row=3, column=0, ipadx=10, sticky='e')
        self.beam_checkbutton = Checkbutton(self.tab3, variable=self.beam_variable, bg=color_light, fg=color_dark)
        self.beam_checkbutton.grid(row=3, column=1, ipadx=10, sticky='e')

        self.note_variable = IntVar()
        self.note_label = Label(self.tab3, text='Note-head:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.note_label.grid(row=4, column=0, ipadx=10, sticky='e')
        self.note_checkbutton = Checkbutton(self.tab3, variable=self.note_variable, bg=color_light, fg=color_dark)
        self.note_checkbutton.grid(row=4, column=1, ipadx=10, sticky='e')

        self.midinote_variable = IntVar()
        self.midinote_label = Label(self.tab3, text='Midi-note:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.midinote_label.grid(row=5, column=0, ipadx=10, sticky='e')
        self.midinote_checkbutton = Checkbutton(self.tab3, variable=self.midinote_variable, bg=color_light, fg=color_dark)
        self.midinote_checkbutton.grid(row=5, column=1, ipadx=10, sticky='e')

        self.notestop_variable = IntVar()
        self.notestop_label = Label(self.tab3, text='Note-stop:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.notestop_label.grid(row=6, column=0, ipadx=10, sticky='e')
        self.notestop_checkbutton = Checkbutton(self.tab3, variable=self.notestop_variable, bg=color_light, fg=color_dark)
        self.notestop_checkbutton.grid(row=6, column=1, ipadx=10, sticky='e')

        self.pagenumbering_variable = IntVar()
        self.pagenumbering_label = Label(self.tab3, text='Page-numbering:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.pagenumbering_label.grid(row=7, column=0, ipadx=10, sticky='e')
        self.pagenumbering_checkbutton = Checkbutton(self.tab3, variable=self.pagenumbering_variable, bg=color_light, fg=color_dark)
        self.pagenumbering_checkbutton.grid(row=7, column=1, ipadx=10, sticky='e')

        self.barlines_variable = IntVar()
        self.barlines_label = Label(self.tab3, text='Barlines:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.barlines_label.grid(row=8, column=0, ipadx=10, sticky='e')
        self.barlines_checkbutton = Checkbutton(self.tab3, variable=self.barlines_variable, bg=color_light, fg=color_dark)
        self.barlines_checkbutton.grid(row=8, column=1, ipadx=10, sticky='e')

        self.basegrid_variable = IntVar()
        self.basegrid_label = Label(self.tab3, text='Base-grid:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.basegrid_label.grid(row=9, column=0, ipadx=10, sticky='e')
        self.basegrid_checkbutton = Checkbutton(self.tab3, variable=self.basegrid_variable, bg=color_light, fg=color_dark)
        self.basegrid_checkbutton.grid(row=9, column=1, ipadx=10, sticky='e')

        self.countline_variable = IntVar()
        self.countline_label = Label(self.tab3, text='Count-line:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.countline_label.grid(row=10, column=0, ipadx=10, sticky='e')
        self.countline_checkbutton = Checkbutton(self.tab3, variable=self.countline_variable, bg=color_light, fg=color_dark)
        self.countline_checkbutton.grid(row=10, column=1, ipadx=10, sticky='e')

        self.measurenumbering_variable = IntVar()
        self.measurenumbering_label = Label(self.tab3, text='Measure-numbering:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.measurenumbering_label.grid(row=11, column=0, ipadx=10, sticky='e')
        self.measurenumbering_checkbutton = Checkbutton(self.tab3, variable=self.measurenumbering_variable, bg=color_light, fg=color_dark)
        self.measurenumbering_checkbutton.grid(row=11, column=1, ipadx=10, sticky='e')

        self.accidental_variable = IntVar()
        self.accidental_label = Label(self.tab3, text='Accidentals:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.accidental_label.grid(row=12, column=0, ipadx=10, sticky='e')
        self.accidental_checkbutton = Checkbutton(self.tab3, variable=self.accidental_variable, bg=color_light, fg=color_dark)
        self.accidental_checkbutton.grid(row=12, column=1, ipadx=10, sticky='e')

        self.sounding_variable = IntVar()
        self.sounding_label = Label(self.tab3, text='Sounding-dot:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.sounding_label.grid(row=13, column=0, ipadx=10, sticky='e')
        self.sounding_checkbutton = Checkbutton(self.tab3, variable=self.sounding_variable, bg=color_light, fg=color_dark)
        self.sounding_checkbutton.grid(row=13, column=1, ipadx=10, sticky='e')
        
        self.leftdot_variable = IntVar()
        self.leftdot_label = Label(self.tab3, text='Left-note-dot:', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.leftdot_label.grid(row=14, column=0, ipadx=10, sticky='e')
        self.leftdot_checkbutton = Checkbutton(self.tab3, variable=self.leftdot_variable, bg=color_light, fg=color_dark)
        self.leftdot_checkbutton.grid(row=14, column=1, ipadx=10, sticky='e')

        # tab4; staff editor
        self.tab4 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab4, text='Staff')

        # create staff selector
        self.select_frame = Frame(self.tab4, bg=color_light, padx=5, pady=5)
        self.select_frame.pack(padx=10, pady=10, fill='both')
        self.previous_button = Button(self.select_frame, text='<', command=self.previous_staff)
        self.previous_button.grid(row=0, column=0, sticky='e')
        self.next_button = Button(self.select_frame, text='>', command=self.next_staff)
        self.next_button.grid(row=0, column=1, sticky='e')
        self.staffno = 0
        self.staffno_label = Label(self.select_frame, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.staffno_label.grid(row=0, column=2, sticky='e')
        self.staff_onoff_variable = IntVar()
        self.staff_onoff_check = Checkbutton(self.select_frame, variable=self.staff_onoff_variable, text='on/off', bg=color_light, fg=color_dark, font=('Courier', 16))
        self.staff_onoff_check.grid(row=0, column=3, ipadx=10, sticky='e')

        # create entry's & buttons
        self.staff_frame = Frame(self.tab4, bg=color_light)
        self.staff_frame.pack(padx=10, pady=10, fill='both')

        self.name_label = Label(self.staff_frame, text='Staff name (text):', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.name_label.grid(row=0, column=0, ipadx=10, sticky='e')
        self.name_entry = Entry(self.staff_frame, font=('Courier', 16), validate="focusout", 
                                validatecommand=lambda: self.save_staff(self.score), bg=color_light, fg=color_dark)
        self.name_entry.grid(row=0, column=1, ipadx=10, sticky='e')
        
        self.staffscale_label = Label(self.staff_frame, text='Staff scale (number):', font=('Courier', 16), bg=color_light, fg=color_dark)
        self.staffscale_label.grid(row=1, column=0, ipadx=10, sticky='e')
        self.staffscale_entry = Entry(self.staff_frame, font=('Courier', 16), bg=color_light, fg=color_dark)
        self.staffscale_entry.grid(row=1, column=1, ipadx=10, sticky='e')


        # Apply and Close buttons:
        self.applycloseframe = Frame(self.popup)
        self.applycloseframe.pack(padx=10, pady=10, fill='both')
        # create the "Close" button
        self.close_button = Button(self.applycloseframe, text="Close", command=self._close, font=('Courier', 16))
        self.close_button.pack(side='left',padx=5,pady=5)
        # create the "apply" button
        self.apply_button = Button(self.applycloseframe, text="Apply", font=('Courier', 16))
        self.apply_button.pack(side='left',padx=5,pady=5)
        self.apply_button.configure(command=lambda: self.evaluate(self.score))

        self.popup.bind('<Return>', lambda e: self.evaluate(self.score))
        self.popup.bind('<Escape>', self._close)

        # sugar coating
        self.popup.configure(bg='#002B36')
        self.applycloseframe.configure(bg='#eee8d5')

        
        # insert io['score'] values in Entry's
        # tab 1
        self.title_entry.insert(0,io['score']['header']['title']['text'])
        self.composer_entry.insert(0,io['score']['header']['composer']['text'])
        self.copyright_entry.insert(0,io['score']['header']['copyright']['text'])
        
        # tab 2
        self.threelinescale_entry.insert(0,io['score']['properties']['threelinescale'])
        self.drawscale_entry.insert(0,io['score']['properties']['draw-scale'])
        self.pagewidth_entry.insert(0,io['score']['properties']['page-width'])
        self.pageheight_entry.insert(0,io['score']['properties']['page-height'])
        self.headerheight_entry.insert(0,io['score']['properties']['header-height'])
        self.footerheight_entry.insert(0,io['score']['properties']['footer-height'])
        self.pagemargl_entry.insert(0,io['score']['properties']['page-margin-left'])
        self.pagemargr_entry.insert(0,io['score']['properties']['page-margin-right'])
        self.pagemargu_entry.insert(0,io['score']['properties']['page-margin-up'])
        self.pagemargd_entry.insert(0,io['score']['properties']['page-margin-down'])
        self.leftcolor_entry.insert(0,io['score']['properties']['color-left-hand-midinote'])
        self.rightcolor_entry.insert(0,io['score']['properties']['color-right-hand-midinote'])
        if io['score']['properties']['black-note-style'] == 'PianoScript':
            self.blackstyle_combo.set('PianoScript')
        else:
            self.blackstyle_combo.set('Klavarskribo')
        if io['score']['properties']['stop-sign-style'] == 'PianoScript':
            self.stopstyle_combo.set('PianoScript')
        else:
            self.stopstyle_combo.set('Klavarskribo')

        # tab 3
        if io['score']['properties']['minipiano'] == True: self.minipiano_checkbutton.select()
        if io['score']['properties']['staffonoff'] == True: self.staff_checkbutton.select()
        if io['score']['properties']['stemonoff'] == True: self.stem_checkbutton.select()
        if io['score']['properties']['beamonoff'] == True: self.beam_checkbutton.select()
        if io['score']['properties']['noteonoff'] == True: self.note_checkbutton.select()
        if io['score']['properties']['midinoteonoff'] == True: self.midinote_checkbutton.select()
        if io['score']['properties']['notestoponoff'] == True: self.notestop_checkbutton.select()
        if io['score']['properties']['pagenumberingonoff'] == True: self.pagenumbering_checkbutton.select()
        if io['score']['properties']['barlinesonoff'] == True: self.barlines_checkbutton.select()
        if io['score']['properties']['basegridonoff'] == True: self.basegrid_checkbutton.select()
        if io['score']['properties']['countlineonoff'] == True: self.countline_checkbutton.select()
        if io['score']['properties']['measurenumberingonoff'] == True: self.measurenumbering_checkbutton.select()
        if io['score']['properties']['accidentalonoff'] == True: self.accidental_checkbutton.select()
        if io['score']['properties']['soundingdotonoff'] == True: self.sounding_checkbutton.select()
        if io['score']['properties']['leftdotonoff'] == True: self.leftdot_checkbutton.select()

        # tab 4
        self.read_staff()

        self.show()

    def next_staff(self):

        self.save_staff(self.score)
        
        self.staffno += 1
        if self.staffno > 3: self.staffno = 3

        self.read_staff()

    def previous_staff(self):

        self.save_staff(self.score)
        
        self.staffno -= 1
        if self.staffno < 0: self.staffno = 0

        self.read_staff()

    def save_staff(self, score):

        # read entry:
        staffname = self.name_entry.get()
        try: staffscale = float(self.staffscale_entry.get())
        except: staffscale = 1
        blackstyle = self.blackstyle_combo.get()
        try: margupleft = float(self.margl_entry.get())
        except: margupleft = 10
        try: margdownright = float(self.margr_entry.get())
        except: margdownright = 10

        # update in io['score']:
        for st in score['properties']['staff']:
            if st['staff-number'] == self.staffno:
                st['onoff'] = bool(self.staff_onoff_variable.get())
                st['name'] = staffname
                st['staff-scale'] = staffscale

    def read_staff(self):
        # clear input
        self.name_entry.delete(0,'end')
        self.staffscale_entry.delete(0,'end')

        self.staffno_label.configure(text=str(self.staffno + 1))

        # fill input from io['score']
        for st in self.score['properties']['staff']:
            if st['staff-number'] == self.staffno:
                self.staff_onoff_variable.set(st['onoff'])
                self.name_entry.insert(0,st['name'])
                self.staffscale_entry.insert(0,st['staff-scale'])



    def _close(self, event=''):
        self.close = True
        self.popup.destroy()

    def evaluate(self, score, event=''):
        # tab 1; titles
        score['header']['title']['text'] = self.title_entry.get()
        score['header']['composer']['text'] = self.composer_entry.get()
        score['header']['copyright']['text'] = self.copyright_entry.get()

        # tab 2; properties
        try:
            score['properties']['threelinescale'] = float(self.threelinescale_entry.get())
            score['properties']['draw-scale'] = float(self.drawscale_entry.get())
            score['properties']['page-width'] = float(self.pagewidth_entry.get())
            score['properties']['page-height'] = float(self.pageheight_entry.get())
            score['properties']['header-height'] = float(self.headerheight_entry.get())
            score['properties']['footer-height'] = float(self.footerheight_entry.get())
            score['properties']['page-margin-left'] = float(self.pagemargl_entry.get())
            score['properties']['page-margin-right'] = float(self.pagemargr_entry.get())
            score['properties']['page-margin-up'] = float(self.pagemargu_entry.get())
            score['properties']['page-margin-down'] = float(self.pagemargd_entry.get())
            score['properties']['color-left-hand-midinote'] = self.leftcolor_entry.get()
            score['properties']['color-right-hand-midinote'] = self.rightcolor_entry.get()
            score['properties']['black-note-style'] = self.blackstyle_variable.get()
            score['properties']['stop-sign-style'] = self.stopstyle_variable.get()
        except:
            return

        # tab 3; onoff
        score['properties']['minipiano'] = self.minipiano_variable.get()
        score['properties']['staffonoff'] = self.staff_variable.get()
        score['properties']['stemonoff'] = self.stem_variable.get()
        score['properties']['beamonoff'] = self.beam_variable.get()
        score['properties']['noteonoff'] = self.note_variable.get()
        score['properties']['midinoteonoff'] = self.midinote_variable.get()
        score['properties']['notestoponoff'] = self.notestop_variable.get()
        score['properties']['pagenumberingonoff'] = self.pagenumbering_variable.get()
        score['properties']['barlinesonoff'] = self.barlines_variable.get()
        score['properties']['basegridonoff'] = self.basegrid_variable.get()
        score['properties']['countlineonoff'] = self.countline_variable.get()
        score['properties']['measurenumberingonoff'] = self.measurenumbering_variable.get()
        score['properties']['accidentalonoff'] = self.accidental_variable.get()
        score['properties']['soundingdotonoff'] = self.sounding_variable.get()
        score['properties']['leftdotonoff'] = self.leftdot_variable.get()

        # tab 4; staff editor
        self.save_staff(self.score)

        self.score = score
        self.popup.destroy()

    def show(self):
        # display the popup window and wait for it to be destroyed
        self.parent.wait_window(self.popup)