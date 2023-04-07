from tkinter import Canvas

canvas = Canvas(root)

def draw_line(x0,y0,x1,y1,cv=):
	cv.create_line(x0,y0,x1,y1)