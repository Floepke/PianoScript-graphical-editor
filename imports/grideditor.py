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

from tkinter import Tk, Button, Label, Toplevel, Frame, Text
if not __name__ == '__main__': 
    from imports.tools import measure_length


class GridEditor:

    '''This is the PianoScript custom Grid Editor dialog'''

    def __init__(self, parent, Score):

        self.parent = parent
        self.Score = Score
        self.processed_score = None
        self.last_pianotick = 0

        # create window
        self.window = Toplevel(self.parent, bg='#002B36')
        self.window.title('PianoScript - Grid Editor')
        self.sw = self.window.winfo_screenwidth()
        self.sh = self.window.winfo_screenheight()
        self.window.geometry("%sx%s+%s+%s" % (int(self.sw/4), int(self.sh/2), int(self.sw/4*1.5), int(self.sh/4)))
        self.window.wm_attributes("-topmost", 1)
        self.window.protocol("WM_DELETE_WINDOW", self._cancel)

        # main frame
        self.main_frame = Frame(self.window, bg='#eee8d5')
        self.main_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # buttons frame
        self.buttons_frame = Frame(self.main_frame, bg='#eee8d5')
        self.buttons_frame.pack(fill='both', padx=10,pady=10)

        # apply button
        self.apply_button = Button(self.buttons_frame, text='     Apply     ', font=('Courier', 14), command=self._apply)
        self.apply_button.pack(side='left')

        # cancel button
        self.cancel_button = Button(self.buttons_frame, text='     Cancel     ', font=('Courier', 14), command=self._cancel)
        self.cancel_button.pack(side='right')


        # example label
        self.example_frame = Frame(self.main_frame, bg='#eee8d5')
        self.example_frame.pack(fill='both', padx=10)
        self.example = Label(self.example_frame, text='1.time-signature(example: "4/4")\n2.amount of measures(Example: "22")\n3.grid-division(Example: "4")\n4.visible(set to "1" or "0")\nOn each line you can enter these \nfour values to form the grid.', font=('Courier', 14), bg='#eee8d5', justify='left')
        self.example.pack(side='left')

        # text widget
        self.text_frame = Frame(self.main_frame, bg='#eee8d5')
        self.text_frame.pack(fill='both', expand=True)
        self.text = Text(self.text_frame, font=('Courier', 14))
        self.text.pack(padx=10,pady=10,fill='both',expand=True)
        self.text.focus_set()

        self.insert_text(self.Score)
        self.show()

    def insert_text(self, Score):
        
        txt = ''
        for ts,idx in zip(self.Score['events']['grid'],range(len(self.Score['events']['grid']))):

            numerator = ts['numerator']
            denominator = ts['denominator']
            amount = ts['amount']
            grid_div = ts['grid']
            visible = ts['visible']
            if visible: visible = 1

            if not idx == len(self.Score['events']['grid'])-1:
                txt += str(numerator) + '/' + str(denominator) + ' ' + str(amount) + ' ' + str(grid_div) + ' ' + str(visible) + '\n'
            else:
                txt += str(numerator) + '/' + str(denominator) + ' ' + str(amount) + ' ' + str(grid_div) + ' ' + str(visible)
        self.text.insert('1.0', txt)

    def _apply(self):
        t = self.text.get('1.0', 'end').split('\n')
        self.Score['events']['grid'] = []
        for ts in t:
            numerator = None
            denominator = None
            amount = None
            grid = None
            visible = None
            if ts:
                try:
                    numerator = int(ts.split()[0].split('/')[0])
                    denominator = int(ts.split()[0].split('/')[1])
                    amount = int(ts.split()[1])
                    grid = int(ts.split()[2])
                    visible = int(ts.split()[3])
                except:
                    print(
                        '''Please read the documentation about how to provide the grid mapping correctly.
                        a correct gridmap:
                        4/4 16 4 1''')
                    return
            else:
                continue
            # gridmap add to Score
            self.Score['events']['grid'].append(
                {'amount': amount, 'numerator': numerator, 'denominator': denominator,
                 'grid': grid, 'visible': visible})
        
        # calculate last pianotick
        for grid in self.Score['events']['grid']:
            self.last_pianotick += (grid['amount'] * measure_length((grid['numerator'], grid['denominator'])))
        
        # remove linebreaks from Score that are >= then last_pianotick
        for lb in reversed(self.Score['events']['line-break']):
            if lb['time'] >= self.last_pianotick:
                self.Score['events']['line-break'].remove(lb)

        self.processed_score = self.Score
        self.window.destroy()

    def _cancel(self):
        self.processed_score = self.Score
        self.window.destroy()

    def show(self):
        # display the popup window and wait for it to be destroyed
        self.parent.wait_window(self.window)










# TEST
if __name__ == '__main__':
    root = tk.Tk()
    dialog = GridEditor()
    root.wait_window(dialog)
    print(f"Grid map editor string: {dialog.result}")
    root.mainloop()