import tkinter as tk
from tkinter import filedialog
window = tk.Tk()
window.lift()
window.call('wm', 'attributes', '.', '-topmost', True)
window.after_idle(window.call, 'wm', 'attributes', '.', '-topmost', False)

filename = filedialog.askopenfilename(parent=window,
                              initialdir="",
                              title="Select A File",
                              filetypes = (("Text files", "*.txt"), ("All files", "*")))
window.wm_attributes('-topmost', 1) #and "parent=window" argument help open the dialog box on top of other windows
window.mainloop()