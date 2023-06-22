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

from tkinter import Tk, Button, Label, Toplevel, Entry, Frame, Text, Scale, Listbox, Checkbutton, IntVar, Checkbutton
from tkinter import ttk

if not __name__ == '__main__': 
    from imports.tools import measure_length

class AskString:
    def __init__(self, parent, title, prompt, initialvalue=''):
        self.parent = parent
        self.title = title
        self.prompt = prompt
        self.initialvalue = initialvalue
        self.result = None

        # create the popup window
        self.popup = Toplevel(self.parent)
        self.popup.title(self.title)
        self.popup.wm_attributes("-topmost", 1)

        # create frame
        self.frame = Frame(self.popup)
        self.frame.pack(padx=10, pady=10, fill='both')

        # create the Label widget
        self.label = Label(self.frame, text=self.prompt, font=('Courier', 16))
        self.label.pack(padx=5,pady=5)
        self.label.update()
        self.label.configure(wraplength=self.label.winfo_width(), justify='left')

        # create the Entry widget
        self.entry = Entry(self.frame, font=('Courier', 16),bg='white')
        self.entry.pack(fill='x',padx=5,pady=5)
        self.entry.insert(0, self.initialvalue)
        self.entry.select_range(0, 'end')
        self.entry.icursor('end')

        # create the "OK" button
        self.ok_button = Button(self.frame, text="OK", command=self._ok, font=('Courier', 16))
        self.ok_button.pack(side='left',padx=5,pady=5)

        # create the "Cancel" button
        self.cancel_button = Button(self.frame, text="Cancel", command=self._cancel, font=('Courier', 16))
        self.cancel_button.pack(side='left',padx=5,pady=5)

        # set the focus on the Entry widget
        self.entry.focus_set()

        self.popup.bind('<Escape>', self._cancel)
        self.popup.bind('<Return>', self._ok)

        # sugar coating
        self.popup.configure(bg='#002B36')
        self.label.configure(bg='#eee8d5', fg='#002b66')
        self.frame.configure(bg='#eee8d5')
        self.entry.configure(fg='#002b66')


        self.show()

    def _ok(self, event=''):
        # save the entered value and destroy the popup window
        self.result = self.entry.get()
        self.popup.destroy()

    def _cancel(self, event=''):
        # set the result to None and destroy the popup window
        self.result = None
        self.popup.destroy()

    def show(self):
        # display the popup window and wait for it to be destroyed
        self.parent.wait_window(self.popup)



class AskFloat:
    def __init__(self, parent, title, prompt, initialvalue=''):
        self.parent = parent
        self.title = title
        self.prompt = prompt
        self.initialvalue = initialvalue
        self.result = None

        # create the popup window
        self.popup = Toplevel(self.parent)
        self.popup.title(self.title)
        self.popup.wm_attributes("-topmost", 1)

        # create frame
        self.frame = Frame(self.popup)
        self.frame.pack(padx=10, pady=10, fill='both')

        # create the Label widget
        self.label = Label(self.frame, text=self.prompt, font=('Courier', 16))
        self.label.pack(padx=5,pady=5)
        self.label.update()
        self.label.configure(wraplength=self.label.winfo_width(), justify='left')

        # create the Entry widget
        self.entry = Entry(self.frame, font=('Courier', 16),bg='white')
        self.entry.pack(fill='x',padx=5,pady=5)
        self.entry.insert(0, self.initialvalue)
        self.entry.select_range(0, 'end')
        self.entry.icursor('end')

        # create the "OK" button
        self.ok_button = Button(self.frame, text="OK", command=self._ok, font=('Courier', 16))
        self.ok_button.pack(side='left',padx=5,pady=5)

        # create the "Cancel" button
        self.cancel_button = Button(self.frame, text="Cancel", command=self._cancel, font=('Courier', 16))
        self.cancel_button.pack(side='right',padx=5,pady=5)

        # set the focus on the Entry widget
        self.entry.focus_set()

        self.popup.bind('<Escape>', self._cancel)
        self.popup.bind('<Return>', self._ok)

        # sugar coating
        self.popup.configure(bg='#002B36')
        self.label.configure(bg='#eee8d5', fg='#002b66')
        self.frame.configure(bg='#eee8d5')
        self.entry.configure(fg='#002b66')

        self.show()

    def _ok(self, event=''):
        evaluate = self._evaluate()
        if evaluate:
            self.result = float(self.entry.get())
            self.popup.destroy()
        else:
            self.show()

    def _cancel(self, event=''):
        # set the result to None and destroy the popup window
        self.result = None
        self.popup.destroy()

    def _evaluate(self):
        # evaluate
        value = self.entry.get()
        try: 
            value = float(value)
        except: return False
        return True

    def show(self):
        # display the popup window and wait for it to be destroyed
        self.parent.wait_window(self.popup)


class AskInt:
    def __init__(self, parent, title, prompt, initialvalue=''):
        self.parent = parent
        self.title = title
        self.prompt = prompt
        self.initialvalue = initialvalue
        self.result = None

        # create the popup window
        self.popup = Toplevel(self.parent)
        self.popup.title(self.title)
        self.popup.wm_attributes("-topmost", 1)

        # create frame
        self.frame = Frame(self.popup)
        self.frame.pack(padx=10, pady=10, fill='both')

        # create the Label widget
        self.label = Label(self.frame, text=self.prompt, font=('Courier', 16))
        self.label.pack(padx=5,pady=5)
        self.label.update()
        self.label.configure(wraplength=self.label.winfo_width(), justify='left')

        # create the Entry widget
        self.entry = Entry(self.frame, font=('Courier', 16))
        self.entry.pack(fill='x',padx=5,pady=5)
        self.entry.insert(0, self.initialvalue)
        self.entry.select_range(0, 'end')
        self.entry.icursor('end')

        # create the "OK" button
        self.ok_button = Button(self.frame, text="OK", command=self._ok, font=('Courier', 16))
        self.ok_button.pack(side='left',padx=5,pady=5)

        # create the "Cancel" button
        self.cancel_button = Button(self.frame, text="Cancel", command=self._cancel, font=('Courier', 16))
        self.cancel_button.pack(side='right',padx=5,pady=5)

        # set the focus on the Entry widget
        self.entry.focus_set()

        self.popup.bind('<Escape>', self._cancel)
        self.popup.bind('<Return>', self._ok)

        # sugar coating
        self.popup.configure(bg='#002B36')
        self.label.configure(bg='#eee8d5', fg='#002b66')
        self.frame.configure(bg='#eee8d5')
        self.entry.configure(fg='#002b66')

        self.show()

    def _ok(self, event=''):
        evaluate = self._evaluate()
        if evaluate:
            self.result = int(self.entry.get())
            self.popup.destroy()
        else:
            self.show()

    def _cancel(self, event=''):
        # set the result to None and destroy the popup window
        self.result = None
        self.popup.destroy()

    def _evaluate(self):
        # evaluate
        value = self.entry.get()
        try: 
            value = int(value)
        except: return False
        return True

    def show(self):
        # display the popup window and wait for it to be destroyed
        self.parent.wait_window(self.popup)




class AskYesNoCancel:
    def __init__(self, parent, title, prompt, initialvalue=''):
        self.parent = parent
        self.title = title
        self.prompt = prompt
        self.initialvalue = initialvalue
        self.result = None

        # create the popup window
        self.popup = Toplevel(self.parent)
        self.popup.title(self.title)
        self.popup.wm_attributes("-topmost", 1)

        # create frame
        self.frame = Frame(self.popup)
        self.frame.pack(padx=10, pady=10, fill='both')

        # create the Label widget
        self.label = Label(self.frame, text=self.prompt, font=('Courier', 16))
        self.label.pack(padx=5,pady=5)
        self.label.update()
        self.label.configure(wraplength=self.label.winfo_width(), justify='left')

        # create the "Yes" button
        self.yes_button = Button(self.frame, text="Yes", command=self._yes, font=('Courier', 16))
        self.yes_button.pack(side='left',padx=5,pady=5)

        # create the "No" button
        self.no_button = Button(self.frame, text="No", command=self._no, font=('Courier', 16))
        self.no_button.pack(side='left',padx=5,pady=5)

        # create the "Cancel" button
        self.cancel_button = Button(self.frame, text="Cancel", command=self._cancel, font=('Courier', 16))
        self.cancel_button.pack(side='left',padx=5,pady=5)

        self.popup.bind('<Escape>', self._cancel)
        self.popup.bind('<Return>', self._yes)

        # sugar coating
        self.popup.configure(bg='#002B36')
        self.label.configure(bg='#eee8d5', fg='#002b66')
        self.frame.configure(bg='#eee8d5')

        self.show()

    def _yes(self, event=''):
        self.result = True
        self.popup.destroy()

    def _no(self, event=''):
        # set the result to None and destroy the popup window
        self.result = False
        self.popup.destroy()

    def _cancel(self, event=''):
        # set the result to None and destroy the popup window
        self.result = None
        self.popup.destroy()

    def show(self):
        # display the popup window and wait for it to be destroyed
        self.parent.wait_window(self.popup)


class QuantizeDialog:
    def __init__(self, parent, title, prompt):
        self.parent = parent
        self.title = title
        self.prompt = prompt
        self.result = None

        # create the popup window
        self.popup = Toplevel(self.parent)
        self.popup.title(self.title)
        self.popup.wm_attributes("-topmost", 1)
        self.popup.resizable(0,0)

        # create frame
        self.frame = Frame(self.popup)
        self.frame.pack(padx=10, pady=10, fill='both')

        # create the Label widget
        self.label = Label(self.frame, text=self.prompt, font=('Courier', 16))
        self.label.pack(padx=5,pady=5)
        self.label.update()
        self.label.configure(wraplength=self.label.winfo_width(), justify='left')

        # create the "Yes" button
        self.yes_button = Button(self.frame, text="Note start", command=self._yes, font=('Courier', 16))
        self.yes_button.pack(side='left',padx=5,pady=5)

        # create the "No" button
        self.no_button = Button(self.frame, text="Note duration", command=self._no, font=('Courier', 16))
        self.no_button.pack(side='left',padx=5,pady=5)

        # create the "Cancel" button
        self.cancel_button = Button(self.frame, text="Cancel", command=self._cancel, font=('Courier', 16))
        self.cancel_button.pack(side='left',padx=5,pady=5)

        self.popup.bind('<Escape>', self._cancel)
        self.popup.bind('<Return>', self._yes)

        # sugar coating
        self.popup.configure(bg='#002B36')
        self.label.configure(bg='#eee8d5', fg='#002b66')
        self.frame.configure(bg='#eee8d5')

        self.show()

    def _yes(self, event=''):
        self.result = True
        self.popup.destroy()

    def _no(self, event=''):
        # set the result to None and destroy the popup window
        self.result = False
        self.popup.destroy()

    def _cancel(self, event=''):
        # set the result to None and destroy the popup window
        self.result = None
        self.popup.destroy()

    def show(self):
        # display the popup window and wait for it to be destroyed
        self.parent.wait_window(self.popup)


class GreyscalePicker:
    def __init__(self, parent, prompt, initialvalue=200):
        self.parent = parent
        self.title = 'Shade of grey picker'
        self.prompt = prompt
        self.initialvalue = initialvalue
        self.color = '#' + hex(self.initialvalue)[2:].zfill(2) * 3

        # create the popup window
        self.popup = Toplevel(self.parent)
        self.popup.title(self.title)
        self.popup.wm_attributes("-topmost", 1)

        # create frame
        self.frame = Frame(self.popup, bg=self.color)
        self.frame.pack(padx=10, pady=10, fill='both')

        # create the Label widget
        self.label = Label(self.frame, text=self.prompt, font=('Courier', 16), bg=self.color)
        self.label.pack(padx=5,pady=5)
        self.label.update()
        self.label.configure(wraplength=self.label.winfo_width(), justify='left')

        # create the "Ok" button
        self.yes_button = Button(self.frame, text="OK", command=self._ok, font=('Courier', 16))
        self.yes_button.pack(side='left',padx=5,pady=5)

        # create the "Cancel" button
        self.cancel_button = Button(self.frame, text="Cancel", command=self._cancel, font=('Courier', 16))
        self.cancel_button.pack(side='left',padx=5,pady=5)

        # grey slider
        self.slider = Scale(self.frame, from_=0, to=255, orient='h', relief='flat', command=self._edit, bg=self.color)
        self.slider.pack(side='left',padx=5,pady=5, fill='x', expand=True)

        self.popup.bind('<Escape>', self._cancel)
        self.popup.bind('<Return>', self._ok)

        # sugar coating
        self.popup.configure(bg='#002B36')
        self.label.configure(fg='#002b66')

        self.slider.set(self.initialvalue)

        self.show()

    def _ok(self, event=''):
        self.popup.destroy()

    def _cancel(self, event=''):
        # set the result to None and destroy the popup window
        self.color = None
        self.popup.destroy()

    def _edit(self, event=''):

        hex_val = hex(self.slider.get())[2:].zfill(2)
        self.color = "#" + hex_val*3
        self.frame.configure(bg=self.color)
        self.label.configure(bg=self.color)
        self.slider.configure(bg=self.color)

    def show(self):
        # display the popup window and wait for it to be destroyed
        self.parent.wait_window(self.popup)


class AskTextEditor:
    def __init__(self, parent, title, prompt, initialtext='', initialcheck=0):
        self.parent = parent
        self.title = title
        self.prompt = prompt
        self.initialtext = initialtext
        self.initialcheck = initialcheck
        self.result = None

        # create the popup window
        self.popup = Toplevel(self.parent)
        self.popup.title(self.title)
        self.popup.wm_attributes("-topmost", 1)

        # create frame
        self.frame = Frame(self.popup)
        self.frame.pack(padx=10, pady=10, fill='both')

        # create the Label widget
        self.label = Label(self.frame, text=self.prompt, font=('Courier', 16))
        self.label.pack(padx=5,pady=5)
        self.label.update()
        self.label.configure(wraplength=self.label.winfo_width(), justify='left')

        # create the Entry widget
        self.entry = Entry(self.frame, font=('Courier', 16),bg='white')
        self.entry.pack(fill='x',padx=5,pady=5)
        self.entry.insert(0, self.initialtext)
        self.entry.select_range(0, 'end')
        self.entry.icursor('end')

        # create the "OK" button
        self.ok_button = Button(self.frame, text="OK", command=self._ok, font=('Courier', 16))
        self.ok_button.pack(side='left',padx=5,pady=5)

        # create the "Cancel" button
        self.cancel_button = Button(self.frame, text="Cancel", command=self._cancel, font=('Courier', 16))
        self.cancel_button.pack(side='left',padx=5,pady=5)

        # create checkbutton
        self.vert = IntVar()
        self.vert.set(self.initialcheck)
        self.checkbutton = Checkbutton(self.frame, text='place text vertical(in relation to staff)', font=('Courier', 16), variable=self.vert)
        self.checkbutton.pack(side='left',padx=5,pady=5)

        # set the focus on the Entry widget
        self.entry.focus_set()

        self.popup.bind('<Escape>', self._cancel)
        self.popup.bind('<Return>', self._ok)

        # sugar coating
        self.popup.configure(bg='#002B36')
        self.label.configure(bg='#eee8d5', fg='#002b66')
        self.frame.configure(bg='#eee8d5')
        self.entry.configure(fg='#002b66')
        self.checkbutton.configure(bg='#eee8d5',fg='#002b66')


        self.show()

    def _ok(self, event=''):
        # save the entered value and destroy the popup window
        self.result = self.entry.get()
        self.vert = self.vert.get()
        self.popup.destroy()

    def _cancel(self, event=''):
        # set the result to None and destroy the popup window
        self.result = None
        self.popup.destroy()

    def show(self):
        # display the popup window and wait for it to be destroyed
        self.parent.wait_window(self.popup)

class OptionsDialog:
    def __init__(self, parent, Score):
        self.parent = parent
        self.close = False
        self.score = Score

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
        self.title_label = Label(self.tab1, text='Title:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.title_label.grid(row=0, column=0, sticky='e')
        self.title_entry = Entry(self.tab1, font=('Courier', 16), bg='white', fg='black')
        self.title_entry.grid(row=0, column=1)
        self.composer_label = Label(self.tab1, text='Composer:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.composer_label.grid(row=1, column=0, sticky='e')
        self.composer_entry = Entry(self.tab1, font=('Courier', 16), bg='white', fg='black')
        self.composer_entry.grid(row=1, column=1)
        self.copyright_label = Label(self.tab1, text='Copyright:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.copyright_label.grid(row=2, column=0, sticky='e')
        self.copyright_entry = Entry(self.tab1, font=('Courier', 16), bg='white', fg='black')
        self.copyright_entry.grid(row=2, column=1)

        #tab 2; layout
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Layout')
        self.drawscale_label = Label(self.tab2, text='Draw scale:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.drawscale_label.grid(row=0, column=0, ipadx=10, sticky='e')
        self.drawscale_entry = Entry(self.tab2, font=('Courier', 16), bg='white', fg='black')
        self.drawscale_entry.grid(row=0, column=1, ipadx=10)
        self.pagewidth_label = Label(self.tab2, text='Page width(mm):', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.pagewidth_label.grid(row=1, column=0, ipadx=10, sticky='e')
        self.pagewidth_entry = Entry(self.tab2, font=('Courier', 16), bg='white', fg='black')
        self.pagewidth_entry.grid(row=1, column=1, ipadx=10)
        self.pageheight_label = Label(self.tab2, text='Page height(mm):', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.pageheight_label.grid(row=2, column=0, ipadx=10, sticky='e')
        self.pageheight_entry = Entry(self.tab2, font=('Courier', 16), bg='white', fg='black')
        self.pageheight_entry.grid(row=2, column=1, ipadx=10)
        self.headerheight_label = Label(self.tab2, text='Header height(mm):', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.headerheight_label.grid(row=3, column=0, ipadx=10, sticky='e')
        self.headerheight_entry = Entry(self.tab2, font=('Courier', 16), bg='white', fg='black')
        self.headerheight_entry.grid(row=3, column=1, ipadx=10)
        self.footerheight_label = Label(self.tab2, text='Footer height(mm):', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.footerheight_label.grid(row=4, column=0, ipadx=10, sticky='e')
        self.footerheight_entry = Entry(self.tab2, font=('Courier', 16), bg='white', fg='black')
        self.footerheight_entry.grid(row=4, column=1, ipadx=10)
        self.pagemargl_label = Label(self.tab2, text='Page margin left(mm):', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.pagemargl_label.grid(row=5, column=0, ipadx=10, sticky='e')
        self.pagemargl_entry = Entry(self.tab2, font=('Courier', 16), bg='white', fg='black')
        self.pagemargl_entry.grid(row=5, column=1, ipadx=10)
        self.pagemargr_label = Label(self.tab2, text='Page margin right(mm):', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.pagemargr_label.grid(row=6, column=0, ipadx=10, sticky='e')
        self.pagemargr_entry = Entry(self.tab2, font=('Courier', 16), bg='white', fg='black')
        self.pagemargr_entry.grid(row=6, column=1, ipadx=10)
        self.pagemargu_label = Label(self.tab2, text='Page margin up(mm):', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.pagemargu_label.grid(row=7, column=0, ipadx=10, sticky='e')
        self.pagemargu_entry = Entry(self.tab2, font=('Courier', 16), bg='white', fg='black')
        self.pagemargu_entry.grid(row=7, column=1, ipadx=10)
        self.pagemargd_label = Label(self.tab2, text='Page margin down(mm):', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.pagemargd_label.grid(row=8, column=0, ipadx=10, sticky='e')
        self.pagemargd_entry = Entry(self.tab2, font=('Courier', 16), bg='white', fg='black')
        self.pagemargd_entry.grid(row=8, column=1, ipadx=10)
        self.leftcolor_label = Label(self.tab2, text='left hand midinote color:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.leftcolor_label.grid(row=10, column=0, ipadx=10, sticky='e')
        self.leftcolor_entry = Entry(self.tab2, font=('Courier', 16), bg='white', fg='black')
        self.leftcolor_entry.grid(row=10, column=1, ipadx=10)
        self.rightcolor_label = Label(self.tab2, text='right hand midinote color:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.rightcolor_label.grid(row=11, column=0, ipadx=10, sticky='e')
        self.rightcolor_entry = Entry(self.tab2, font=('Courier', 16), bg='white', fg='black')
        self.rightcolor_entry.grid(row=11, column=1, ipadx=10)

        # tab 3; elements on/off
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Elements on/off')
        self.minipiano_variable = IntVar()
        self.minipiano_label = Label(self.tab3, text='Piano-keyboard:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.minipiano_label.grid(row=0, column=0, ipadx=10, sticky='e')
        self.minipiano_checkbutton = Checkbutton(self.tab3, bg='#eee8d5', variable=self.minipiano_variable)
        self.minipiano_checkbutton.grid(row=0, column=1, ipadx=10)
        
        self.staff_variable = IntVar()
        self.staff_label = Label(self.tab3, text='Staff:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.staff_label.grid(row=1, column=0, ipadx=10, sticky='e')
        self.staff_checkbutton = Checkbutton(self.tab3, bg='#eee8d5', variable=self.staff_variable)
        self.staff_checkbutton.grid(row=1, column=1, ipadx=10, sticky='e')

        self.stem_variable = IntVar()
        self.stem_label = Label(self.tab3, text='Stem:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.stem_label.grid(row=2, column=0, ipadx=10, sticky='e')
        self.stem_checkbutton = Checkbutton(self.tab3, bg='#eee8d5', variable=self.stem_variable)
        self.stem_checkbutton.grid(row=2, column=1, ipadx=10, sticky='e')

        self.beam_variable = IntVar()
        self.beam_label = Label(self.tab3, text='Beam:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.beam_label.grid(row=3, column=0, ipadx=10, sticky='e')
        self.beam_checkbutton = Checkbutton(self.tab3, bg='#eee8d5', variable=self.beam_variable)
        self.beam_checkbutton.grid(row=3, column=1, ipadx=10, sticky='e')

        self.note_variable = IntVar()
        self.note_label = Label(self.tab3, text='Note-head:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.note_label.grid(row=4, column=0, ipadx=10, sticky='e')
        self.note_checkbutton = Checkbutton(self.tab3, bg='#eee8d5', variable=self.note_variable)
        self.note_checkbutton.grid(row=4, column=1, ipadx=10, sticky='e')

        self.midinote_variable = IntVar()
        self.midinote_label = Label(self.tab3, text='Midi-note:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.midinote_label.grid(row=5, column=0, ipadx=10, sticky='e')
        self.midinote_checkbutton = Checkbutton(self.tab3, bg='#eee8d5', variable=self.midinote_variable)
        self.midinote_checkbutton.grid(row=5, column=1, ipadx=10, sticky='e')

        self.notestop_variable = IntVar()
        self.notestop_label = Label(self.tab3, text='Note-stop:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.notestop_label.grid(row=6, column=0, ipadx=10, sticky='e')
        self.notestop_checkbutton = Checkbutton(self.tab3, bg='#eee8d5', variable=self.notestop_variable)
        self.notestop_checkbutton.grid(row=6, column=1, ipadx=10, sticky='e')

        self.pagenumbering_variable = IntVar()
        self.pagenumbering_label = Label(self.tab3, text='Page-numbering:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.pagenumbering_label.grid(row=7, column=0, ipadx=10, sticky='e')
        self.pagenumbering_checkbutton = Checkbutton(self.tab3, bg='#eee8d5', variable=self.pagenumbering_variable)
        self.pagenumbering_checkbutton.grid(row=7, column=1, ipadx=10, sticky='e')

        self.barlines_variable = IntVar()
        self.barlines_label = Label(self.tab3, text='Barlines:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.barlines_label.grid(row=8, column=0, ipadx=10, sticky='e')
        self.barlines_checkbutton = Checkbutton(self.tab3, bg='#eee8d5', variable=self.barlines_variable)
        self.barlines_checkbutton.grid(row=8, column=1, ipadx=10, sticky='e')

        self.basegrid_variable = IntVar()
        self.basegrid_label = Label(self.tab3, text='Base-grid:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.basegrid_label.grid(row=9, column=0, ipadx=10, sticky='e')
        self.basegrid_checkbutton = Checkbutton(self.tab3, bg='#eee8d5', variable=self.basegrid_variable)
        self.basegrid_checkbutton.grid(row=9, column=1, ipadx=10, sticky='e')

        self.countline_variable = IntVar()
        self.countline_label = Label(self.tab3, text='Count-line:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.countline_label.grid(row=10, column=0, ipadx=10, sticky='e')
        self.countline_checkbutton = Checkbutton(self.tab3, bg='#eee8d5', variable=self.countline_variable)
        self.countline_checkbutton.grid(row=10, column=1, ipadx=10, sticky='e')

        self.measurenumbering_variable = IntVar()
        self.measurenumbering_label = Label(self.tab3, text='Measure-numbering:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.measurenumbering_label.grid(row=11, column=0, ipadx=10, sticky='e')
        self.measurenumbering_checkbutton = Checkbutton(self.tab3, bg='#eee8d5', variable=self.measurenumbering_variable)
        self.measurenumbering_checkbutton.grid(row=11, column=1, ipadx=10, sticky='e')

        self.accidental_variable = IntVar()
        self.accidental_label = Label(self.tab3, text='Accidentals:', font=('Courier', 16), bg='#eee8d5', fg='black')
        self.accidental_label.grid(row=12, column=0, ipadx=10, sticky='e')
        self.accidental_checkbutton = Checkbutton(self.tab3, bg='#eee8d5', variable=self.accidental_variable)
        self.accidental_checkbutton.grid(row=12, column=1, ipadx=10, sticky='e')


        # Apply and Close buttons:
        self.applycloseframe = Frame(self.popup)
        self.applycloseframe.pack(padx=10, pady=10, fill='both')
        # create the "Close" button
        self.close_button = Button(self.applycloseframe, text="Close", command=self._close, font=('Courier', 16))
        self.close_button.pack(side='left',padx=5,pady=5)
        # create the "apply" button
        self.apply_button = Button(self.applycloseframe, text="Apply", font=('Courier', 16))
        self.apply_button.pack(side='left',padx=5,pady=5)
        self.apply_button.configure(command=lambda: self._evaluate(self.score))

        self.popup.bind('<Return>', lambda e: self._evaluate(self.score))

        # sugar coating
        self.popup.configure(bg='#002B36')
        self.applycloseframe.configure(bg='#eee8d5')

        # insert Score values in Entry's
        # tab 1
        self.title_entry.insert(0,Score['header']['title']['text'])
        self.composer_entry.insert(0,Score['header']['composer']['text'])
        self.copyright_entry.insert(0,Score['header']['copyright']['text'])
        
        # tab 2
        self.drawscale_entry.insert(0,Score['properties']['draw-scale'])
        self.pagewidth_entry.insert(0,Score['properties']['page-width'])
        self.pageheight_entry.insert(0,Score['properties']['page-height'])
        self.headerheight_entry.insert(0,Score['properties']['header-height'])
        self.footerheight_entry.insert(0,Score['properties']['footer-height'])
        self.pagemargl_entry.insert(0,Score['properties']['page-margin-left'])
        self.pagemargr_entry.insert(0,Score['properties']['page-margin-right'])
        self.pagemargu_entry.insert(0,Score['properties']['page-margin-up'])
        self.pagemargd_entry.insert(0,Score['properties']['page-margin-down'])
        self.leftcolor_entry.insert(0,Score['properties']['color-left-hand-midinote'])
        self.rightcolor_entry.insert(0,Score['properties']['color-right-hand-midinote'])

        # tab 3
        if Score['properties']['minipiano'] == True: self.minipiano_checkbutton.select()
        if Score['properties']['staffonoff'] == True: self.staff_checkbutton.select()
        if Score['properties']['stemonoff'] == True: self.stem_checkbutton.select()
        if Score['properties']['beamonoff'] == True: self.beam_checkbutton.select()
        if Score['properties']['noteonoff'] == True: self.note_checkbutton.select()
        if Score['properties']['midinoteonoff'] == True: self.midinote_checkbutton.select()
        if Score['properties']['notestoponoff'] == True: self.notestop_checkbutton.select()
        if Score['properties']['pagenumberingonoff'] == True: self.pagenumbering_checkbutton.select()
        if Score['properties']['barlinesonoff'] == True: self.barlines_checkbutton.select()
        if Score['properties']['basegridonoff'] == True: self.basegrid_checkbutton.select()
        if Score['properties']['countlineonoff'] == True: self.countline_checkbutton.select()
        if Score['properties']['measurenumberingonoff'] == True: self.measurenumbering_checkbutton.select()
        if Score['properties']['accidentalonoff'] == True: self.accidental_checkbutton.select()

        self.show()

    def _close(self, event=''):
        self.close = True
        self.popup.destroy()

    def _evaluate(self, Score, event=''):
        Score['header']['title']['text'] = self.title_entry.get()
        Score['header']['composer']['text'] = self.composer_entry.get()
        Score['header']['copyright']['text'] = self.copyright_entry.get()

        try:
            Score['properties']['draw-scale'] = float(self.drawscale_entry.get())
            Score['properties']['page-width'] = float(self.pagewidth_entry.get())
            Score['properties']['page-height'] = float(self.pageheight_entry.get())
            Score['properties']['header-height'] = float(self.headerheight_entry.get())
            Score['properties']['footer-height'] = float(self.footerheight_entry.get())
            Score['properties']['page-margin-left'] = float(self.pagemargl_entry.get())
            Score['properties']['page-margin-right'] = float(self.pagemargr_entry.get())
            Score['properties']['page-margin-up'] = float(self.pagemargu_entry.get())
            Score['properties']['page-margin-down'] = float(self.pagemargd_entry.get())
            Score['properties']['color-left-hand-midinote'] = self.leftcolor_entry.get()
            Score['properties']['color-right-hand-midinote'] = self.rightcolor_entry.get()
        except:
            return

        Score['properties']['minipiano'] = self.minipiano_variable.get()
        Score['properties']['staffonoff'] = self.staff_variable.get()
        Score['properties']['stemonoff'] = self.stem_variable.get()
        Score['properties']['beamonoff'] = self.beam_variable.get()
        Score['properties']['noteonoff'] = self.note_variable.get()
        Score['properties']['midinoteonoff'] = self.midinote_variable.get()
        Score['properties']['notestoponoff'] = self.notestop_variable.get()
        Score['properties']['pagenumberingonoff'] = self.pagenumbering_variable.get()
        Score['properties']['barlinesonoff'] = self.barlines_variable.get()
        Score['properties']['basegridonoff'] = self.basegrid_variable.get()
        Score['properties']['countlineonoff'] = self.countline_variable.get()
        Score['properties']['measurenumberingonoff'] = self.measurenumbering_variable.get()
        Score['properties']['accidentalonoff'] = self.accidental_variable.get()

        self.score = Score
        self.popup.destroy()

    def show(self):
        # display the popup window and wait for it to be destroyed
        self.parent.wait_window(self.popup)


class TextEngraver():
    
    def __init__(self,parent,Score):
        
        self.parent = parent
        self.close = False
        self.score = Score

        self.result = ''

        # create the popup window
        self.popup = Toplevel(self.parent)
        self.popup.title('PianoScript - Text Engraver')
        self.popup.wm_attributes("-topmost", 1)

        # Text widget
        self.textframe = Frame(self.popup)
        self.textframe.pack()
        self.text = Text(self.textframe, font=('Courier', 16))
        self.text.pack()

        # Buttons
        self.button_frame = Frame(self.popup)
        self.button_frame.pack(fill='x')
        self.generate_button = Button(self.button_frame, text='Generate...', command=lambda: self._generate(Score))
        self.generate_button.pack(side='left')

        self.show()

    def _generate(self, Score):
        
        '''This function parses a text version of pianoscript which you can copy and email to someone :)'''
        ...


    def show(self):
        # display the popup window and wait for it to be destroyed
        self.parent.wait_window(self.popup)


# Example usage
if __name__ == "__main__":
    root = Tk()
    
    # # AskString
    # dialog = AskString(root, "Enter a string", "Question for input:", 'initialtext')
    # result = dialog.result
    # if result is not None:
    #     print(result)
    # else:
    #     print("Dialog was cancelled")
    
    # # AskFloat
    # dialog = AskFloat(root, "Enter a float", "Question for input:", 7.77)
    # result = dialog.result
    # if result is not None:
    #     print(result)
    # else:
    #     print("Dialog was cancelled")

    # # AskInt
    # dialog = AskInt(root, "Enter a int", "Question for input:", 777)
    # result = dialog.result
    # if result is not None:
    #     print(result)
    # else:
    #     print("Dialog was cancelled")

    # # AskYesNoCancel
    # dialog = AskYesNoCancel(root, "Wish to save?", "Do you wish to save the current Score?")
    # result = dialog.result
    # if result:
    #     print('yes')
    # elif result == False:
    #     print('no')
    # else:
    #     print("Dialog was cancelled")

    # # GreyscalePicker
    # dialog = GreyscalePicker(root, "Every printer prints a different shade of grey. \nSo you can set a custom greyscale color here \nthat looks readable on your printouts.")
    # color = dialog.color
    # if color:
    #     print(color)
    # elif color == None:
    #     print("Dialog was cancelled")

    # # OptionsDialog
    # dialog = OptionsDialog(root)
    # result = dialog.result
    # if result is not None:
    #     print(result)
    # else:
    #     print("Dialog was cancelled")

    # # TextEngraver
    # dialog = TextEngraver(root, '')
    # result = dialog.result
    # if result is not None:
    #     print(result)
    # else:
    #     print("Dialog was cancelled")

