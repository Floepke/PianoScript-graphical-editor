# def slur(canvas, time, duration, control1, control2, width):
	
# 	...

'''
write a function called 'slur' with the parameters: canvas, time, duration, control1, control2, width. 'canvas' is the tkinter canvas where the function draws a slur. 'time' is the x axis startingpoint of the slur. 'duration' is the 'time+duration' x axis from the slur. so 'duration' gives the endpoint of the slur. 'control1' and 'control2' are essentially the bezier curve control points 1 and 2.
'''

import tkinter as tk

def slur(canvas, controls, width=7.5, steps=100):
    '''Draws a slur on the given tkinter canvas with the given parameters.
    controls is a list with four xy positions for drawing a bezier curve.
    this function draws two bezier curves to draw a slur'''

    def evaluate_cubic_bezier(t, control_points):
        p0, p1, p2, p3 = control_points
        x = (1 - t) ** 3 * p0[0] + 3 * t * (1 - t) ** 2 * p1[0] + 3 * t ** 2 * (1 - t) * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * t * (1 - t) ** 2 * p1[1] + 3 * t ** 2 * (1 - t) * p2[1] + t ** 3 * p3[1]
        return x, y

    # define control points
    ctl1 = controls[0]
    ctl2 = controls[1]
    ctl3 = controls[2]
    ctl4 = controls[3]

    # calculate slur
    slur_points = []
    for t in range(steps):
        x, y = evaluate_cubic_bezier(t / steps, controls)
        slur_points.append([x, y])
    for t in reversed(range(steps)):
        x, y = evaluate_cubic_bezier(t / steps, 
        	[ctl1,(ctl2[0],ctl2[1]+width),(ctl3[0],ctl3[1]+width),ctl4])
        slur_points.append([x, y])
    canvas.create_polygon(slur_points, fill='black')

    
    

if __name__ == '__main__':
	root = tk.Tk()
	canvas = tk.Canvas(root, width=400, height=400)
	canvas.pack()

	# Call the 'slur' function to draw a slur on the canvas
	slur(canvas, [(100,100),(110,50),(290,50),(300,100)],7.5)

	root.mainloop()