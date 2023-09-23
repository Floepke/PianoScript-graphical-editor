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

from imports.editor.editor_draw_elements import DrawElements

class CopyCutPaste:
    '''
        This class contains all functions for 
        making a selection and do cut, copy, paste
        operations with them.
    '''
    def __init__(self, io):
        
        # all event types that are alowed to copy, cut, paste
        self.evt_types = ['note', 'beam', 'countline', 'slur', 'text', 'pedal']

        self.io = io
        self.draw_caller = {
            'note':DrawElements.draw_note
        }
    
    def process_selection(self, event_type):
        '''
            Mouse handling for making a selection of events
        '''
        
        if event_type == 'btn1click':
            
            # start the selection rectangle
            self.io['selection']['rectangle_on'] = True
            self.io['selection']['x1'] = self.io['mouse']['x']
            self.io['selection']['y1'] = self.io['mouse']['y']

            # unselect the previous selection(change color back to normal)
            if self.io['selection']['selection_buffer']:
                for et in self.evt_types:
                    for evt in self.io['selection']['selection_buffer'][et]:
                        self.draw_caller[et](evt, self.io, new=False, selected=False)

            # clear selection buffer
            self.io['selection']['selection_buffer'] = {}
            for et in self.evt_types:
                self.io['selection']['selection_buffer'][et] = []

        if event_type == 'motion':
            
            if self.io['selection']['rectangle_on']:
                # update rectangle points
                self.io['selection']['x2'] = self.io['mouse']['x']
                self.io['selection']['y2'] = self.io['mouse']['y']

                # update rectangle
                DrawElements.draw_selection_rectangle(self.io)

        if event_type == 'btn1release':

            # update rectangle points
            self.io['selection']['x2'] = self.io['mouse']['x']
            self.io['selection']['y2'] = self.io['mouse']['y']
            
            # delete selection rectangle
            self.io['selection']['rectangle_on'] = False
            self.io['editor'].delete('selectionrectangle')

            # detect selectable events
            ftags = self.io['editor'].find_overlapping(self.io['selection']['x1'],
                                                        self.io['selection']['y1'],
                                                        self.io['selection']['x2'],
                                                        self.io['selection']['y2'])
            tags = []
            for t in ftags:
                tag = self.io['editor'].gettags(t)
                for tt in tag:
                    if tt.startswith('#'):
                        tags.append(tt)
            tags = list(dict.fromkeys(tags))
            
            # write selection to selection_buffer
            for et in self.evt_types:
                for evt in self.io['score']['events'][et]:
                    if evt['tag'] in tags:
                        self.io['selection']['selection_buffer'][et].append(evt)
                        
                        # change the color of the selected event on the editor screen
                        self.draw_caller[et](evt, self.io, new=False, selected=True)

    def cut(self):
        ...

    def copy(self):
        ...

    def paste(self):
        ...
