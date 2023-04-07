import customtkinter

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')

# root
root = customtkinter.CTk()
root.title('PianoScript')
scrwidth = root.winfo_screenwidth()
scrheight = root.winfo_screenheight()
root.geometry("%sx%s+0+0" % (int(scrwidth), int(scrheight)))

# master
panedmaster = CTkPanedWindow(root, orient='h', sashwidth=0, relief='flat', bg=color1)
panedmaster.place(relwidth=1, relheight=1)
leftpanel = PanedWindow(panedmaster, relief='flat', bg=color1, width=50)
panedmaster.add(leftpanel)
midpanel = PanedWindow(panedmaster, relief='flat', bg=color1, orient='h', sashwidth=10, width=scrwidth * 0.8)
panedmaster.add(midpanel)
rightpanel = PanedWindow(midpanel, relief='flat', bg=color1)
midpanel.add(rightpanel)



root.mainloop()