from tkinter import *
from tkinter import simpledialog

ws = Tk()
ws.title("Python Guides")

answer1 = simpledialog.askstring("Input", "What is your first name?",
                                parent=ws)
if answer1 is not None:
    print("Your first name is ", answer1)
else:
    print("You don't have a first name?")

answer1 = simpledialog.askinteger("Input", "What is your age?",
                                 parent=ws,
                                 minvalue=0, maxvalue=100)
if answer1 is not None:
    print("Your age is ", answer1)
else:
    print("You don't have an age?")

answer1 = simpledialog.askfloat("Input", "What is your salary?",
                               parent=ws,
                               minvalue=0.0, maxvalue=100000.0)
if answer1 is not None:
    print("Your salary is ", answer1)
else:
    print("You don't have a salary?")
ws.mainloop()