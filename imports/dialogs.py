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
        self.frame.pack(padx=10, pady=10)

        # create the Label widget
        Label(self.frame, text=self.prompt).pack()

        # create the Entry widget
        self.entry = Entry(self.frame)
        self.entry.pack(fill='x')
        self.entry.insert(0, self.initialvalue)
        self.entry.select_range(0, 'end')
        self.entry.icursor('end')

        # create the "OK" button
        ok_button = Button(self.frame, text="OK", command=self._ok)
        ok_button.pack(side='left')

        # create the "Cancel" button
        cancel_button = Button(self.frame, text="Cancel", command=self._cancel)
        cancel_button.pack(side='right')

        # set the focus on the Entry widget
        self.entry.focus_set()

        self.popup.bind('<Escape>', self._cancel)
        self.popup.bind('<Return>', self._ok)

        self.show()

    def _ok(self, event):
        # save the entered value and destroy the popup window
        self.result = self.entry.get()
        self.popup.destroy()

    def _cancel(self, event):
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
        self.frame.pack(padx=10, pady=10)

        # create the Label widget
        Label(self.frame, text=self.prompt).pack()

        # create the Entry widget
        self.entry = Entry(self.frame)
        self.entry.pack(fill='x')
        self.entry.insert(0, self.initialvalue)
        self.entry.select_range(0, 'end')
        self.entry.icursor('end')

        # create the "OK" button
        ok_button = Button(self.frame, text="OK", command=self._ok)
        ok_button.pack(side='left')

        # create the "Cancel" button
        cancel_button = Button(self.frame, text="Cancel", command=self._cancel)
        cancel_button.pack(side='right')

        # set the focus on the Entry widget
        self.entry.focus_set()

        self.popup.bind('<Escape>', self._cancel)
        self.popup.bind('<Return>', self._ok)

        self.entryisfloat = False

        self.show()

    def _ok(self, event):
        evaluate = self._evaluate()
        if evaluate:
            self.result = float(self.entry.get())
            self.popup.destroy()
        else:
            self.show()

    def _cancel(self, event):
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
        self.frame.pack(padx=10, pady=10)

        # create the Label widget
        Label(self.frame, text=self.prompt).pack()

        # create the Entry widget
        self.entry = Entry(self.frame)
        self.entry.pack(fill='x')
        self.entry.insert(0, self.initialvalue)
        self.entry.select_range(0, 'end')
        self.entry.icursor('end')

        # create the "OK" button
        ok_button = Button(self.frame, text="OK", command=self._ok)
        ok_button.pack(side='left')

        # create the "Cancel" button
        cancel_button = Button(self.frame, text="Cancel", command=self._cancel)
        cancel_button.pack(side='right')

        # set the focus on the Entry widget
        self.entry.focus_set()

        self.popup.bind('<Escape>', self._cancel)
        self.popup.bind('<Return>', self._ok)

        self.show()

    def _ok(self, event):
        evaluate = self._evaluate()
        if evaluate:
            self.result = int(self.entry.get())
            self.popup.destroy()
        else:
            self.show()

    def _cancel(self, event):
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

# Example usage
if __name__ == "__main__":
    root = Tk()
    # AskString
    dialog = AskString(root, "Enter a string", "Question for input:", 'initialtext')
    result = dialog.result
    if result is not None:
        print(result)  # do something with the entered string
    else:
        print("Dialog was cancelled")
    # AskFloat
    dialog = AskFloat(root, "Enter a float", "Question for input:", 4.21)
    result = dialog.result
    if result is not None:
        print(result)  # do something with the entered string
    else:
        print("Dialog was cancelled")

    # AskInt
    dialog = AskInt(root, "Enter a int", "Question for input:", 69)
    result = dialog.result
    if result is not None:
        print(result)  # do something with the entered string
    else:
        print("Dialog was cancelled")
