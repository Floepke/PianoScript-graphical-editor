#!python3.11
# coding: utf-8

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

# imports   
import copy

class CtlZ:
    def __init__(self, io):
        self.io = io

        self.buffer = [copy.deepcopy(self.io['score'])]
        self.index = 0
        self.max_ctlz_num = 16

        self.io['root'].bind('<z>', lambda e: self.undo())
        self.io['root'].bind('<Z>', lambda e: self.redo())

    def reset_ctlz(self):
        # use this if we load a new or existing project
        self.buffer = [copy.deepcopy(self.io['score'])]
        self.index = 0

    def add_ctlz(self, score):
        
        # if we are in the past(undo/redo):
        if not self.index == len(self.buffer) - 1:    
            self.buffer = self.buffer[:self.index + 1]

        # Add a new version of the score to the buffer
        self.buffer.append(copy.deepcopy(score))
        self.index = len(self.buffer) - 1

        # undo limit
        if len(self.buffer) > self.max_ctlz_num:
            self.buffer.pop(0)

    def undo(self): 
        print('undo...')
        

        # load undo version
        self.index -= 1
        if self.index < 0:
            self.index = 0
        self.io['score'] = copy.deepcopy(self.buffer[self.index])

        # update editor and engraver
        self.io['main_editor'].redraw_editor(self.io)
        self.io['engraver'].trigger_render()

    def redo(self):
        print('redo...')

        # load redo version
        self.index += 1
        if self.index > len(self.buffer) - 1:
            self.index = len(self.buffer) - 1
        self.io['score'] = copy.deepcopy(self.buffer[self.index])

        # update editor and engraver
        self.io['main_editor'].redraw_editor(self.io)
        self.io['engraver'].trigger_render()
