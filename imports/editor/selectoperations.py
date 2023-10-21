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
from imports.editor.tools_editor import ToolsEditor
import copy

class SelectOperations:
    '''
        This class contains all functions for 
        making a selection and do cut, copy, paste
        operations with them.
    '''
    def __init__(self, io):

        # utils
        self.io = io
        self.draw_caller = {
            'note':DrawElements.draw_note,
            'beam':DrawElements.draw_beam,
            'countline':DrawElements.draw_countline,
            'slur':DrawElements.draw_slur,
            'text':DrawElements.draw_text,
            'pedal':DrawElements.draw_pedal,
            'ornament':DrawElements.draw_ornament
        }

        # binds
        self.io['root'].bind('<Control-x>', self._cut)
        self.io['root'].bind('<Control-c>', self._copy)
        self.io['root'].bind('<Control-v>', self._paste)
        self.io['root'].bind('<Right>', self._transpose_up)
        self.io['root'].bind('<Left>', self._transpose_down)
        self.io['root'].bind('<Up>', self._move_backward)
        self.io['root'].bind('<Down>', self._move_forward)
    
    


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
                for et in self.io['selection']['copy_types']:
                    for evt in self.io['selection']['selection_buffer'][et]:
                        if evt in self.io['score']['events'][et]:
                            self.draw_caller[et](evt, self.io, new=False, selected=False)

            # clear selection buffer
            self.io['selection']['selection_buffer'] = {}
            for et in self.io['selection']['copy_types']:
                self.io['selection']['selection_buffer'][et] = []

            # unset active flag
            self.io['selection']['active'] = False

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
            tags = list(dict.fromkeys(tags)) # removes duplicates

            # return if there is no selected event
            if not tags:
                self.io['selection']['active'] = False
                return
            
            # write selection to selection_buffer
            for et in self.io['selection']['copy_types']:
                for evt in self.io['score']['events'][et]:

                    # set active flag
                    self.io['selection']['active'] = True

                    if evt['tag'] in tags:
                        self.io['selection']['selection_buffer'][et].append(evt)
                        
                        # change the color of the selected event on the editor screen
                        self.draw_caller[et](evt, self.io, new=False, selected=True)

            # sort the events on the time property
            for et in self.io['selection']['copy_types']:
                self.io['selection']['selection_buffer'][et] = sorted(self.io['selection']['selection_buffer'][et], 
                    key=lambda time: time['time'])

    


    def _cut(self, event=''):
        if self.io['selection']['active']:
            print('cut...')
            # make a copy of the selection
            self.io['selection']['copycut_buffer'] = copy.deepcopy(self.io['selection']['selection_buffer'])

            # delete the selection from the editor and file bacause we cut the selection
            for et in self.io['selection']['copy_types']:
                for evt in self.io['selection']['copycut_buffer'][et]:
                    self.io['editor'].delete(evt['tag'])
                    self.io['score']['events'][et].remove(evt)

            # unset active flag
            self.io['selection']['active'] = False
            # engrave
            self.io['engraver'].trigger_render()
            # ctlz
            self.io['ctlz'].add_ctlz(self.io['score'])

    def _copy(self, event=''):
        # make a copy of the selection
        if self.io['selection']['active']:
            print('copy...')
            self.io['selection']['copycut_buffer'] = copy.deepcopy(self.io['selection']['selection_buffer'])

    def _paste(self, event=''):
        if self.io['selection']['copycut_buffer']:
            print('paste...')
            for et in self.io['selection']['copy_types']:
                for evt in self.io['selection']['copycut_buffer'][et]:
                    lowest = self.io['selection']['copycut_buffer'][et][0]['time']
                    new = copy.deepcopy(evt)
                    new['time'] = new['time'] - lowest + self.io['mouse']['ey']
                    #new['time'] += self.io['mouse']['ey']
                    new['tag'] = '#' + et + str(ToolsEditor.add_tag(self.io))
                    self.draw_caller[et](new, self.io, new=True, selected=False)
            
            # engrave
            self.io['engraver'].trigger_render()
            # ctlz
            self.io['ctlz'].add_ctlz(self.io['score'])

    def _transpose_up(self, event=''):
        # transpose the selection
        if self.io['selection']['active']:
            print('transpose up...')
            evt_types = ['note'] # here we define all types that can be transposed
            for et in self.io['selection']['transpose_types']:
                for evt in self.io['selection']['selection_buffer'][et]:
                    evt['pitch'] += 1
                    if evt['pitch'] > 88: evt['pitch'] = 88
                    self.draw_caller[et](evt, self.io, new=False, selected=True)

            # engrave
            self.io['engraver'].trigger_render()
            # ctlz
            self.io['ctlz'].add_ctlz(self.io['score'])

    def _transpose_down(self, event=''):
        # transpose the selection
        if self.io['selection']['active']:
            print('transpose down...')
            evt_types = ['note'] # here we define all types that can be transposed
            for et in self.io['selection']['transpose_types']:
                for evt in self.io['selection']['selection_buffer'][et]:
                    evt['pitch'] -= 1
                    if evt['pitch'] < 1: evt['pitch'] = 1
                    self.draw_caller[et](evt, self.io, new=False, selected=True)

            # engrave
            self.io['engraver'].trigger_render()
            # ctlz
            self.io['ctlz'].add_ctlz(self.io['score'])

    def _move_forward(self, event=''):
        # move the selection one grid-step forward
        if self.io['selection']['active']:
            print('move forward...')
            for et in self.io['selection']['move_types']:
                for evt in self.io['selection']['selection_buffer'][et]:
                    if evt['time'] + self.io['snap_grid'] < self.io['last_pianotick']:
                        evt['time'] += self.io['snap_grid']
                    self.draw_caller[et](evt, self.io, new=False, selected=True)
            # engrave
            self.io['engraver'].trigger_render()
            # ctlz
            self.io['ctlz'].add_ctlz(self.io['score'])

    def _move_backward(self, event=''):
        # move the selection one grid-step backward
        if self.io['selection']['active']:
            print('move backward...')
            for et in self.io['selection']['move_types']:
                for evt in self.io['selection']['selection_buffer'][et]:
                    if evt['time'] - self.io['snap_grid'] >= 0:
                        evt['time'] -= self.io['snap_grid']
                    self.draw_caller[et](evt, self.io, new=False, selected=True)
            # engrave
            self.io['engraver'].trigger_render()
            # ctlz
            self.io['ctlz'].add_ctlz(self.io['score'])
