import tkinter
import tkinter.ttk as ttk

class MessageBox(object):

    def __init__(self, parent, title, msg, b1, b2):

        root = self.root = tkinter.Toplevel(parent)

        root.title('Grid editor')
        root.resizable(False, False)
        root.grab_set() # modal

        self.msg = str(msg)
        self.b1_return = True
        # if b1 or b2 is a tuple unpack into the button text & return value
        if isinstance(b1, tuple): b1, self.b1_return = b1
        # main frame
        frm_1 = tkinter.Frame(root)
        frm_1.pack(ipadx=2, ipady=2)
        # the message
        message = tkinter.Label(frm_1, font=('Courier', 16), text=self.msg)
        message.pack(padx=8, pady=8)
        # text editor
        text = tkinter.Text(frm_1, font=('Courier', 16))
        text.pack(padx=8, pady=8)
        # buttons
        btn_1 = tkinter.Button(frm_1, width=8, text=b1)
        btn_1['command'] = self.b1_action
        btn_1.pack(padx=4, pady=4, side='right')
        # the enter button will trigger the focused button's action
        btn_1.bind('<KeyPress-Return>', func=self.b1_action)
        btn_2 = tkinter.Button(frm_1, width=8, text=b1)
        btn_2['command'] = self.b1_action
        btn_2.pack(padx=4, pady=4, side='left')
        # the enter button will trigger the focused button's action
        btn_1.bind('<KeyPress-Return>', func=self.b1_action)
        root.bind('<Escape>', func=self.close_mod)
        # roughly center the box on screen
        # for accuracy see: https://stackoverflow.com/a/10018670/1217270
        root.update_idletasks()
        scrwidth = root.winfo_screenwidth()
        scrheight = root.winfo_screenheight()
        root.geometry("%sx%s+0+0" % (int(scrwidth), int(scrheight)))

        root.protocol("WM_DELETE_WINDOW", self.close_mod)

        # a trick to activate the window (on windows 7)
        root.deiconify()

        self.root.mainloop()

    def b1_action(self, event=None):
        try: x = self.cbo.get()
        except AttributeError:
            self.returning = self.b1_return
            self.root.quit()
        else:
            if x:
                self.returning = x
                self.root.quit()
                self.root.destroy()


    def close_mod(self, event=None):
        # top right corner cross click: return value ;`x`;
        # we need to send it a value, otherwise there will be an exception when closing parent window
        self.returning = None
        self.root.quit()
        self.root.destroy()


root = tkinter.Tk()
root.geometry("210x297+%d+%d" % (0,0))
prompt = MessageBox(root, 'title', 'msg', ('b1','b1'), ('b2','b2')).returning
print(prompt)