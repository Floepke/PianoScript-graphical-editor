from tkinter import Tk, Canvas, Scrollbar, Frame

root=Tk()
frame=Frame(root,width=300,height=300)
frame.pack(expand=True, fill='both') #.grid(row=0,column=0)
canvas=Canvas(frame,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,500,500))
hbar=Scrollbar(frame,orient='h')
hbar.pack(side='bottom',fill='x')
hbar.config(command=canvas.xview)
vbar=Scrollbar(frame,orient='v')
vbar.pack(side='right',fill='y')
vbar.config(command=canvas.yview)
canvas.config(width=300,height=300)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side='left',expand=True,fill='both')

root.mainloop()