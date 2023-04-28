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

from tkinter import Tk, Button, Label, Toplevel, Entry, Frame, Text, Scale, Listbox, Checkbutton, IntVar

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
        self.entry = Entry(self.frame, font=('Courier', 16))
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

