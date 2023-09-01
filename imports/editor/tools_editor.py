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

from imports.tools import interpolation, baseround

class ToolsEditor():
    '''
        In this class are only static methods that are
        solving small parts of the puzzle and are related
        to the editor part of the App.
    '''

    @staticmethod
    def time2y(time, io):
        '''
            time2y converts pianoticks into pixels
            based on the io preferences.
        '''
        return time * io['ticksizepx']

    @staticmethod
    def pitch2x(pitch, io):
        '''
            pitch2x converts pitch into pixels
            based on the io preferences.
        '''
        # calculating dimensions ...
        sbar_width = io['sbar'].winfo_width()
        editor_width = io['editor_width'] - sbar_width
        staff_width = editor_width * io['xscale']
        staff_margin = (editor_width - staff_width) / 2
        factor = staff_width / 490

        # calculate x position ...
        pxlist = [-5, 0, 5, 
        15, 20, 25, 30, 35, 45, 50, 55, 60, 65, 70, 75,
        85, 90, 95, 100, 105, 115, 120, 125, 130, 135, 140, 145,
        155, 160, 165, 170, 175, 185, 190, 195, 200, 205, 210, 215,
        225, 230, 235, 240, 245, 255, 260, 265, 270, 275, 280, 285,
        295, 300, 305, 310, 315, 325, 330, 335, 340, 345, 350, 355,
        365, 370, 375, 380, 385, 395, 400, 405, 410, 415, 420, 425,
        435, 440, 445, 450, 455, 465, 470, 475, 480, 485, 490, 495,
        505]
        if pitch > 88:
            pitch = 88
        x = sbar_width+staff_margin + ((pxlist[pitch-1]) * factor)
        return x

    @staticmethod
    def y2time(y, io):
        '''
            calculates time in pianoticks 
            closest to mouse y position.
        '''
        # unpacking parameters...
        grid = io['snap_grid']
        ticksize = io['ticksizepx']
        last_tick = io['last_pianotick']

        # calculating...
        startpx = 0
        endpx = last_tick * ticksize
        time = baseround(interpolation(startpx, endpx, y) * last_tick, grid)
        if time < 0: time = 0
        return time

    @staticmethod
    def x2pitch(x, io):
        '''
            calculates the pitch which is 
            closest to mouse x position.
        '''

        # calculating dimensions...
        sbar_width = io['sbar'].winfo_width()
        editor_width = io['editor_width'] - sbar_width
        staff_width = editor_width * io['xscale']
        staff_margin = (editor_width - staff_width) / 2
        factor = staff_width / 490
        x -= staff_margin + sbar_width

        cf = [4, 9, 16, 21, 28, 33, 40, 45, 52, 57, 64, 69, 76, 81, 88]
        be = [3, 8, 15, 20, 27, 32, 39, 44, 51, 56, 63, 68, 75, 80, 87]

        xlist = [505, 500, 490, 485, 480, 475, 470, 460, 455, 450, 445, 440, 
        435, 430, 420, 415, 410, 405, 400, 390, 385, 380, 375, 370, 365, 360, 350, 
        345, 340, 335, 330, 320, 315, 310, 305, 300, 295, 290, 280, 275, 270, 265, 
        260, 250, 245, 240, 235, 230, 225, 220, 210, 205, 200, 195, 190, 180, 175, 
        170, 165, 160, 155, 150, 140, 135, 130, 125, 120, 110, 105, 100, 95, 90, 
        85, 80, 70, 65, 60, 55, 50, 40, 35, 30, 25, 20, 15, 10, 0, -5]

        closest = min(xlist, key=lambda m:abs(m-(x/factor)))

        for idx, xx in enumerate(reversed(xlist)):
            if xx == closest:
                return idx + 1

    @staticmethod
    def measure_length(numerator, denominator):
        '''
        returns the length in pianoticks (quarter == 256)
        '''
        return int(numerator * (1024 / denominator))

    @staticmethod
    def update_last_pianotick(io):
        '''
            Updates the property last_pianotick in self.io.
            It counts the entire length of the music.
        '''

        score = io['score']
        grid = score['events']['grid']

        time = 0

        for gr in grid:

            length = ToolsEditor.measure_length(gr['numerator'], gr['denominator'])
            
            for a in range(gr['amount']):

                time += length
        
        io['last_pianotick'] = time

    @staticmethod
    def set_scroll_region(io):
        '''
            updates the scroll region and returns the bounding box
        '''
        x1, y1, x2, y2 = io['editor'].bbox('all')
        margin = (io['editor_width'] - (io['editor_width'] * io['xscale'])) / 2
        y1 -= margin
        y2 += margin
        scrollregion = (0, y1, x2, y2)
        io['editor']['scrollregion'] = scrollregion

    @staticmethod
    def update_tick_range(io):
        '''
            updates the tick range that are in 
            the current viewport.
        '''
        # calculating dimensions...
        sbar_width = io['sbar'].winfo_width()
        editor_width = io['editor'].winfo_width() - sbar_width
        editor_height = io['editor'].winfo_height()
        staff_width = editor_width * io['xscale']
        staff_margin = (editor_width - staff_width) / 2

        # calculating ticks...
        start, end = io['sbar'].get()
        start_tick = start * io['last_pianotick'] - (staff_margin / io['ticksizepx']) - 1024 # 1024 it draws a little outside the view
        end_tick = start_tick + (editor_height / io['ticksizepx']) + 2048 # 2048 it draws a little outside the view (1024 ticks)
        
        # writing ticks to io...
        io['view_start_tick'] = start_tick
        io['view_end_tick'] = end_tick

    @staticmethod
    def update_drawing_order(io):
        io['editor'].tag_raise('staffline')
        io['editor'].tag_raise('barline')
        io['editor'].tag_raise('gridline')
        io['editor'].tag_raise('barnumbering')
        io['editor'].tag_raise('note')
        io['editor'].tag_raise('stem')
        io['editor'].tag_raise('leftdot')
        io['editor'].tag_raise('notecursor')

    @staticmethod
    def add_tag(io):
        tag = io['new_tag']
        io['new_tag'] += 1
        return tag

    @staticmethod
    def renumber_tags(io):
        '''
            This function takes the score and
            renumbers the event tags starting
            from zero again. It's needed if we
            load a new or existing project.
        '''
        for k in io['score']['events'].keys():
            for obj in io['score']['events'][k]:
                if obj['tag'] == 'linebreak': continue
                obj['tag'] = f"{k}{io['new_tag']}"
                io['new_tag'] += 1
