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

from tkinter import Tk, Button, Label, Toplevel, Entry, Frame

class AskString:
    def __init__(self, parent, title, prompt, initialvalue=''):
        self.parent = parent
        self.title = title
        self.prompt = prompt
        self.result = None  # initialize result to None
        self.initialvalue = initialvalue

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
        self.entry.configure(bg='#eee8d5', fg='#002b66')


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
        self.result = None  # initialize result to None
        self.initialvalue = initialvalue

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
        self.entry.configure(bg='#eee8d5', fg='#002b66')

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
        self.result = None  # initialize result to None
        self.initialvalue = initialvalue

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
        self.entry.configure(bg='#eee8d5', fg='#002b66')

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
        self.result = None  # initialize result to None
        self.initialvalue = initialvalue

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

    # AskYesNoCancel
    dialog = AskYesNoCancel(root, "Wish to save?", "Do you wish to save the current Score?")
    result = dialog.result
    if result:
        print('yes')
    elif result == False:
        print('no')
    else:
        print("Dialog was cancelled")