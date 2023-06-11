# def slur(canvas, time, duration, control1, control2, width):
	
# 	...

'''
write a function called 'slur' with the parameters: canvas, time, duration, control1, control2, width. 'canvas' is the tkinter canvas where the function draws a slur. 'time' is the x axis startingpoint of the slur. 'duration' is the 'time+duration' x axis from the slur. so 'duration' gives the endpoint of the slur. 'control1' and 'control2' are essentially the bezier curve control points 1 and 2.
'''

import tkinter as tk

def slur_editor(editor, slur, scale, steps=100):
    '''
    Draws a musical slur on the given tkinter canvas with the given parameters.
    controls is a list with four xy positions for drawing a bezier curve. This 
    function draws two bezier curves to form a slur.
    '''

    editor.delete(slur['id'])

    def evaluate_cubic_bezier(t, control_points):
        p0, p1, p2, p3 = control_points
        x = (1 - t) ** 3 * p0[0] + 3 * t * (1 - t) ** 2 * p1[0] + 3 * t ** 2 * (1 - t) * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * t * (1 - t) ** 2 * p1[1] + 3 * t ** 2 * (1 - t) * p2[1] + t ** 3 * p3[1]
        return x, y
    
    # unpack data
    ctl1,ctl2,ctl3,ctl4 = slur['bezier-points']
    # scale = scale['properties']['draw-scale']


    # calculate slur
    slur_points = []
    for t in range(steps):
        x, y = evaluate_cubic_bezier(t / steps, slur['bezier-points'])
        slur_points.append([x, y])

    # draw slur
    editor.create_line(slur_points, fill='black', tag=slur['id'], width=4)
    
    # draw handles
    r = 5
    editor.create_oval(ctl1[0]-r,
    	ctl1[1]-r,
    	ctl1[0]+r,
    	ctl1[1]+r,
    	tag=slur['id'],
    	fill='yellow')
    editor.create_oval(ctl2[0]-r,
    	ctl2[1]-r,
    	ctl2[0]+r,
    	ctl2[1]+r,
    	tag=slur['id'],
    	fill='#268bd2')
    editor.create_oval(ctl3[0]-r,
    	ctl3[1]-r,
    	ctl3[0]+r,
    	ctl3[1]+r,
    	tag=slur['id'],
    	fill='#268bd2')
    editor.create_oval(ctl4[0]-r,
    	ctl4[1]-r,
    	ctl4[0]+r,
    	ctl4[1]+r,
    	tag=slur['id'],
    	fill='yellow')

    
    
# TEST
if __name__ == '__main__':
	root = tk.Tk()
	editor = tk.Canvas(root, width=400, height=400)
	editor.pack()
	# Call the 'slur' function to draw a slur on the canvas
	# 4 control points: [(x,y),(x,y),(x,y),(x,y)]
	slur_editor(editor, [(100,100),(110,50),(290,50),(300,100)],'')
	root.mainloop()