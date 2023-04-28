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


from imports.tools import *

def draw_staff(y_cursor, 
    mn,
    mx, 
    page_margin_left,
    page_width,
    page_margin_right,
    color_black,
    draw_scale,
    pview,
    sh,
    minipiano=True):
    
    def two(y):
        if minipiano:
            x2 = page_width - page_margin_right - (40 * draw_scale)
            pview.create_line(x2,
                y,
                page_width - page_margin_right - (20 * draw_scale),
                y,
                fill=color_black,
                width=5*draw_scale,
                capstyle='round')
            pview.create_line(x2,
                y+(10*draw_scale),
                page_width - page_margin_right - (20 * draw_scale),
                y+(10*draw_scale),
                fill=color_black,
                width=5*draw_scale,
                capstyle='round')
        else:
            x2 = page_width - page_margin_right
        pview.create_line(page_margin_left,
            y,
            x2,
            y,
            fill=color_black,
            width=1*draw_scale)
        pview.create_line(page_margin_left,
            y+(10*draw_scale),
            x2,
            y+(10*draw_scale),
            fill=color_black,
            width=1*draw_scale)
    
    def three(y):
        if minipiano:
            x2 = page_width - page_margin_right - (40 * draw_scale)
            pview.create_line(x2,
                y,
                page_width - page_margin_right - (20 * draw_scale),
                y,
                fill=color_black,
                width=5*draw_scale,
                capstyle='round')
            pview.create_line(x2,
                y+(10*draw_scale),
                page_width - page_margin_right - (20 * draw_scale),
                y+(10*draw_scale),
                fill=color_black,
                width=5*draw_scale,
                capstyle='round')
            pview.create_line(x2,
                y+(20*draw_scale),
                page_width - page_margin_right - (20 * draw_scale),
                y+(20*draw_scale),
                fill=color_black,
                width=5*draw_scale,
                capstyle='round')
        else:
            x2 = page_width - page_margin_right
        pview.create_line(page_margin_left,
            y,
            x2,
            y,
            fill=color_black,
            width=2*draw_scale)
        pview.create_line(page_margin_left,
            y+(10*draw_scale),
            x2,
            y+(10*draw_scale),
            fill=color_black,
            width=2*draw_scale)
        pview.create_line(page_margin_left,
            y+(20*draw_scale),
            x2,
            y+(20*draw_scale),
            fill=color_black,
            width=2*draw_scale)
        
    def clef(y):
        if minipiano:
            x2 = page_width - page_margin_right - (40 * draw_scale)
            pview.create_line(x2,
                y,
                page_width - page_margin_right - (20 * draw_scale),
                y,
                fill=color_black,
                width=5*draw_scale,
                capstyle='round')
            pview.create_line(x2,
                y+(10*draw_scale),
                page_width - page_margin_right - (20 * draw_scale),
                y+(10*draw_scale),
                fill=color_black,
                width=5*draw_scale,
                capstyle='round')
        else:
            x2 = page_width - page_margin_right
        pview.create_line(page_margin_left,
            y,
            x2,
            y,
            fill=color_black,
            width=1*draw_scale,
            dash=(6,6))
        pview.create_line(page_margin_left,
            y+(10*draw_scale),
            x2,
            y+(10*draw_scale),
            fill=color_black,
            width=1*draw_scale,
            dash=(6,6))

    # control flow for engraving the right composition of staff-lines
    keyline = 0
    if mx >= 81:
        three(0 + y_cursor)
        two((40 * draw_scale) + y_cursor)
        three((70 * draw_scale) + y_cursor)
        two((110 * draw_scale) + y_cursor)
        three((140 * draw_scale) + y_cursor)
        two((180 * draw_scale) + y_cursor)
        three((210 * draw_scale) + y_cursor)
        keyline = (250 * draw_scale)
    if mx >= 76 and mx <= 80:
        two(0 + y_cursor)
        three((30 * draw_scale) + y_cursor)
        two((70 * draw_scale) + y_cursor)
        three((100 * draw_scale) + y_cursor)
        two((140 * draw_scale) + y_cursor)
        three((170 * draw_scale) + y_cursor)
        keyline = (210 * draw_scale)
    if mx >= 69 and mx <= 75:
        three(0 + y_cursor)
        two((40 * draw_scale) + y_cursor)
        three((70 * draw_scale) + y_cursor)
        two((110 * draw_scale) + y_cursor)
        three((140 * draw_scale) + y_cursor)
        keyline = 180 * draw_scale
    if mx >= 64 and mx <= 68:
        two(0 + y_cursor)
        three((30 * draw_scale) + y_cursor)
        two((70 * draw_scale) + y_cursor)
        three((100 * draw_scale) + y_cursor)
        keyline = 140 * draw_scale
    if mx >= 57 and mx <= 63:
        three(0 + y_cursor)
        two((40 * draw_scale) + y_cursor)
        three((70 * draw_scale) + y_cursor)
        keyline = 110 * draw_scale
    if mx >= 52 and mx <= 56:
        two(0 + y_cursor)
        three((30 * draw_scale) + y_cursor)
        keyline = 70 * draw_scale
    if mx >= 45 and mx <= 51:
        three(0 + y_cursor)
        keyline = 40 * draw_scale

    clef(keyline + y_cursor)

    if mn >= 33 and mn <= 39:
        three(keyline + (30 * draw_scale) + y_cursor)
    if mn >= 28 and mn <= 32:
        three(keyline + (30 * draw_scale) + y_cursor)
        two(keyline + (70 * draw_scale) + y_cursor)
    if mn >= 21 and mn <= 27:
        three(keyline + (30 * draw_scale) + y_cursor)
        two(keyline + (70 * draw_scale) + y_cursor)
        three(keyline + (100 * draw_scale) + y_cursor)
    if mn >= 16 and mn <= 20:
        three(keyline + (30 * draw_scale) + y_cursor)
        two(keyline + (70 * draw_scale) + y_cursor)
        three(keyline + (100 * draw_scale) + y_cursor)
        two(keyline + (140 * draw_scale) + y_cursor)
    if mn >= 9 and mn <= 15:
        three(keyline + (30 * draw_scale) + y_cursor)
        two(keyline + (70 * draw_scale) + y_cursor)
        three(keyline + (100 * draw_scale) + y_cursor)
        two(keyline + (140 * draw_scale) + y_cursor)
        three(keyline + (170 * draw_scale) + y_cursor)
    if mn >= 4 and mn <= 8:
        three(keyline + (30 * draw_scale) + y_cursor)
        two(keyline + (70 * draw_scale) + y_cursor)
        three(keyline + (100 * draw_scale) + y_cursor)
        two(keyline + (140 * draw_scale) + y_cursor)
        three(keyline + (170 * draw_scale) + y_cursor)
        two(keyline + (210 * draw_scale) + y_cursor)
    if mn >= 1 and mn <= 3:
        three(keyline + (30 * draw_scale) + y_cursor)
        two(keyline + (70 * draw_scale) + y_cursor)
        three(keyline + (100 * draw_scale) + y_cursor)
        two(keyline + (140 * draw_scale) + y_cursor)
        three(keyline + (170 * draw_scale) + y_cursor)
        two(keyline + (210 * draw_scale) + y_cursor)
        if minipiano:
            pview.create_line(page_margin_left, 
                (keyline + (240 * draw_scale) + y_cursor), 
                page_width - page_margin_right - (40 * draw_scale),
                (keyline + (240 * draw_scale) + y_cursor), 
                width=2)
            pview.create_line(page_width - page_margin_right - (40 * draw_scale), 
                (keyline + (240 * draw_scale) + y_cursor), 
                page_width - page_margin_right - (20 * draw_scale),
                (keyline + (240 * draw_scale) + y_cursor), 
                width=5*draw_scale,
                capstyle='round',
                fill=color_black)
        else:
            pview.create_line(page_margin_left, 
                (keyline + (240 * draw_scale) + y_cursor), 
                page_width - page_margin_right,
                (keyline + (240 * draw_scale) + y_cursor), 
                width=2)


    if minipiano:
        # create border
        pview.create_line(page_width - page_margin_right - (40 * draw_scale),
            y_cursor,
            page_width - page_margin_right - (40 * draw_scale),
            y_cursor - (20 * draw_scale),
            fill=color_black)
        pview.create_line(page_width - page_margin_right - (40 * draw_scale),
            y_cursor + sh,
            page_width - page_margin_right - (40 * draw_scale),
            y_cursor + sh + (20 * draw_scale),
            fill=color_black)
        pview.create_line(page_width - page_margin_right,
            y_cursor - (20 * draw_scale),
            page_width - page_margin_right,
            y_cursor + sh + (20 * draw_scale),
            fill=color_black)
        pview.create_line(page_width - page_margin_right - (40 * draw_scale),
            y_cursor - (20 * draw_scale),
            page_width - page_margin_right,
            y_cursor - (20 * draw_scale),
            fill=color_black)
        pview.create_line(page_width - page_margin_right - (40 * draw_scale),
            y_cursor + sh + (20 * draw_scale),
            page_width - page_margin_right,
            y_cursor + sh + (20 * draw_scale),
            fill=color_black)
        # pview.create_rectangle(page_width - page_margin_right - (40 * draw_scale),
        #     y_cursor - (20 * draw_scale),
        #     page_width - page_margin_right,
        #     y_cursor + sh + (20 * draw_scale),
        #     outline=color_black)


































def engrave_pianoscript(render_type, 
    pageno,
    Score,
    MM,
    total_pianoticks,
    color_notation_editor,
    color_editor_canvas,
    pview,root,
    BLACK):
    '''
        auto_scaling == the drawing gets scaled to the width of the printview.
        renderer == 'pianoscript' or 'klavarskribo'.
    '''

    if render_type == 'export':
        pageno = 0

    # check if there is a time_signature in the Score

    if not Score['events']['grid']:
        print('ERROR: There is no time signature in the Score!')
        return

    # place all data in variables from Score for cleaner code
    page_width = Score['properties']['page-width'] * MM
    page_height = Score['properties']['page-height'] * MM
    p_marg_l = Score['properties']['page-margin-left'] * MM
    p_marg_r = Score['properties']['page-margin-right'] * MM
    p_marg_u = Score['properties']['page-margin-up'] * MM
    p_marg_d = Score['properties']['page-margin-down'] * MM
    header_height = Score['properties']['header-height'] * MM
    footer_height = Score['properties']['footer-height'] * MM
    draw_scale = Score['properties']['draw-scale']
    line_break = Score['events']['line-break']
    count_line = Score['events']['count-line']
    staff_sizer = Score['events']['staff-sizer']
    start_repeat = Score['events']['start-repeat']
    end_repeat = Score['events']['end-repeat']
    grid = Score['events']['grid']
    note = Score['events']['note']
    text = Score['events']['text']
    bpm = Score['events']['bpm']
    slur = Score['events']['slur']
    pedal = Score['events']['pedal']
    title = Score['header']['title']
    composer = Score['header']['composer']
    copyright = Score['header']['copyright']
    minipiano = Score['properties']['minipiano']

    def read():
        '''
            read the music from Score an place in the DOC list.
            DOC is an structured list with all events in it.
            structure: [pages[line[events]lines]pages]
            In the draw function we can easily loop over it
            to engrave the document.
        '''
        # data to collect:
        DOC = []
        page_spacing = []
        staff_heights = []
        t_sig_map = []

        # time_signature
        bln_time = 0
        grd_time = 0
        for idx,g in enumerate(Score['events']['grid']):
            t_sig_map.append(g)
            # barline and grid messages
            meas_len = measure_length((g['numerator'], g['denominator']))
            grid_len = meas_len / g['grid']
            for meas in range(0, g['amount']):
                DOC.append({'type': 'barline', 'time': bln_time})
                DOC.append({'type': 'endoflinebarline', 'time': bln_time-0.0000001})
                for grid in range(0, g['grid']):
                    DOC.append({'type': 'gridline', 'time': grd_time})
                    DOC.append({'type': 'gridline', 'time': grd_time-0.0000001})
                    grd_time += grid_len
                bln_time += meas_len
            if g['visible'] == 1:
                DOC.append({'type': 'time_signature_text', 'time': t_sig_start_tick(t_sig_map, idx),
                            'duration': meas_len, 'text': str(g['numerator']) + '/' + str(g['denominator'])})
            idx += 1

        # add endbarline event
        DOC.append({'type': 'endbarline', 'time': total_pianoticks-0.0000001})

        # we add all events from Score to the DOC list
        for note_evt in note:
            e = note_evt
            e['type'] = 'note'
            e = note_split_processor(e, Score)
            for ev in e:
                DOC.append(ev)
        for text_evt in text:
            e = text_evt
            e['type'] = 'text'
            DOC.append(e)
        for bpm_evt in bpm:
            e = bpm_evt
            e['type'] = 'bpm'
            DOC.append(e)
        for slur_evt in slur:
            e = slur_evt
            e['type'] = 'slur'
            DOC.append(e)
        for pedal_evt in pedal:
            e = pedal_evt
            e['type'] = 'pedal'
            DOC.append(e)
        for countline_evt in count_line:
            e = countline_evt
            e['type'] = 'countline'
            DOC.append(e)
        for e in staff_sizer:
            e['type'] = 'invis'
            DOC.append(e)
        for e in start_repeat:
            e['type'] = 'startrepeat'
            DOC.append(e)
        for e in end_repeat:
            e['type'] = 'endrepeat'
            DOC.append(e)

        # now we sort the events on time-key
        DOC = sorted(DOC, key=lambda x: x['time'])

        # for certain kinds of objects like end repeat and end section
        # we need to set the time a fraction earlier because otherwise they
        # appear at the start of a line.
        for e in DOC:
            if e['type'] in ['endrepeat', 'endsection']:
                e['time'] -= 0.0000001

        # Now we organize the DOC object into a list of lines
        # We use the measure_line_division list to do that
        
        # we first need to get the split times from Score
        bl_times = barline_times(Score['events']['grid'])
        
        split_times = [0]
        for spl in Score['events']['line-break']:
            if spl['time'] > 0 and not spl['time'] > total_pianoticks:
                split_times.append(spl['time'])
        split_times.append(total_pianoticks)
        
        # now we split the DOC list into parts of lines
        doc = DOC
        DOC = []
        for _,spl in enumerate(split_times):
            buffer = []
            try: nxt = split_times[_+1]
            except IndexError: nxt = split_times[-1]
            for e in doc:
                if e['time'] >= spl and e['time'] < nxt:
                    buffer.append(e)
            DOC.append(buffer)

        # now we have to calculate the amount of lines
        # that will fit on every page. We need to know 
        # the height of the staffs, and from layout settings
        # the margin around the staff.

        # we make a list that contains all staff heights
        for l in DOC:
            pitches = []
            for e in l:
                if e['type'] in ['note', 'split', 'invis']:
                    pitches.append(e['pitch'])
            try:
                staff_heights.append(staff_height_width(min(pitches),max(pitches),draw_scale))
            except ValueError:
                staff_heights.append(10*draw_scale)

        DOC.pop(-1)
        staff_heights.pop(-1)

        # in this part we calculate how many systems fit on each page
        # also we gather the free space in the printarea in a list
        # called 'page_spacing'.
        doc = DOC
        DOC = []
        y_cursor = header_height
        printarea_height = (page_height - p_marg_u - p_marg_d)
        remaining_space = 0
        page = []
        for line, sh, c in zip(doc,staff_heights, range(len(doc))):
            lmu = line_break[c]['margin-up-left'] * MM
            lmd = line_break[c]['margin-down-right'] * MM
            y_cursor += lmu + sh + lmd
            # if the line fits on paper:
            if y_cursor <= printarea_height - header_height - footer_height:
                page.append(line)
                remaining_space = printarea_height - header_height - footer_height - y_cursor
            # if the line does NOT fit on paper:
            else:
                y_cursor = lmu + sh + lmd
                DOC.append(page)
                page = []
                page.append(line)
                page_spacing.append(remaining_space)
            # if this is the last line:
            if c+1 == len(doc):
                DOC.append(page)
                page_spacing.append(remaining_space)
                    
        return DOC, page_spacing, staff_heights, split_times, bl_times

    DOC, page_spacing, staff_heights, split_times, bl_times = read()

    #------------------
    # debugging prints
    # print('page_spacing: ', page_spacing, '\nstaff_heights: ', len(staff_heights))

    # idxl = 0
    # for idxp, p in enumerate(DOC):
    #     print('new page:', idxp+1)
    #     for l in p:
    #         print('new line:', idxl+1)
    #         for e in l:
    #             print(e)
    #             ...
    #         idxl += 1
    #------------------
    
























    ##-------------------------##
    ## DRAW ENGINE PIANOSCRIPT ##
    ##-------------------------##
    def event_x_pos_engrave(pos,start_line_tick,end_line_tick, indent=False):
        '''
        returns the x position on the paper.
        '''
        factor = interpolation(start_line_tick, end_line_tick, pos)
        if not indent:
            return p_marg_l + ((page_width - p_marg_l - p_marg_r) * factor)
        else:
            return p_marg_l + ((page_width - p_marg_l - p_marg_r - (40 * draw_scale)) * factor)

    def note_y_pos(note, mn, mx, cursy, scale):
        '''
        returns the position of the given note relative to 'cursy'(the y axis staff cursor).
        '''

        ylist = [495, 490, 485, 475, 470, 465, 460, 455, 445, 440, 435, 430, 425, 420, 415,
                 405, 400, 395, 390, 385, 375, 370, 365, 360, 355, 350, 345, 335, 330, 325, 320, 315,
                 305, 300, 295, 290, 285, 280, 275, 265, 260, 255, 250, 245, 235, 230, 225, 220, 215,
                 210, 205, 195, 190, 185, 180, 175, 165, 160, 155, 150, 145, 140, 135, 125, 120, 115,
                 110, 105, 95, 90, 85, 80, 75, 70, 65, 55, 50, 45, 40, 35, 25, 20, 15, 10, 5, 0, -5, -15]

        sub = 0

        if mx >= 81:
            sub = 0
        if mx >= 76 and mx <= 80:
            sub = 40
        if mx >= 69 and mx <= 75:
            sub = 70
        if mx >= 64 and mx <= 68:
            sub = 110
        if mx >= 57 and mx <= 63:
            sub = 140
        if mx >= 52 and mx <= 56:
            sub = 180
        if mx >= 45 and mx <= 51:
            sub = 210
        if mx <= 44:
            sub = 250

        return cursy + (ylist[note - 1] * scale) - (sub * scale)

    def draw():
        '''
            I try to draw everything as efficient as possible from
            the ordered DOC list using many nested if/else flow.
            I found it the best way to draw.

            things we need to know/keep track on:
                - y_cursor
                - page_spacings
                - staff_heights
        '''
        # variables
        if render_type == 'export':
            color_black = 'black'
            color_white = 'white'
        else:
            color_black = color_notation_editor
            color_white = color_editor_canvas

        y_cursor = 0
        idx_l = 0
        b_counter = update_bcounter(DOC,pageno % len(DOC))
        for idx_p, page in enumerate(DOC):

            # render only one page
            if not render_type == 'export':
                if idx_p == pageno % len(DOC):
                    ...
                else:
                    for l in page:
                        idx_l += 1
                    continue
            
            # draw paper
            if not render_type:
                pview.create_line(0,
                    y_cursor,
                    page_width,
                    y_cursor,
                    fill=color_black,
                    width=2,
                    dash=(6,4,5,2,3))

            # draw footer (page numbering, title and copyright notice
            pview.create_text(p_marg_l,
                y_cursor + page_height - p_marg_d,
                text='page ' + str(idx_p+1) + ' of ' + str(len(DOC)) + ' | ' + title['text'] + ' | ' + copyright['text'],
                anchor='sw',
                fill=color_black,
                font=('courier', 12, "normal"))

            y_cursor += p_marg_u

            if not idx_p: # if on the first page
                # draw header (title & composer text)
                pview.create_text(p_marg_l,
                    p_marg_u,
                    text=Score['header']['title']['text'],
                    anchor='nw',
                    font=('courier', 18, "normal"),
                    fill=color_black)
                pview.create_text(page_width - p_marg_r,
                    p_marg_u,
                    text=Score['header']['composer']['text'],
                    anchor='ne',
                    font=('courier', 12, "normal"),
                    fill=color_black)

                y_cursor += header_height
            
            for idx_ll, line in enumerate(page):

                sh = staff_heights[idx_l]
                lmu = line_break[idx_l]['margin-up-left'] * MM
                lmd = line_break[idx_l]['margin-down-right'] * MM
                
                y_cursor += lmu + (page_spacing[idx_p] / (len(DOC[idx_p])) / 2)

                # getting lowest and highest note in line
                mn, mx = 40, 44
                for obj in line:
                    
                    if obj['type'] in ['note', 'split', 'invis']:
                        
                        # calculating the highest and lowest note in the line
                        if mn >= obj['pitch']:
                            mn = obj['pitch']
                        if mx <= obj['pitch']:
                            mx = obj['pitch']

                for idx_o, obj in enumerate(line):
                    
                    # barline and numbering
                    if obj['type'] == 'barline':
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        pview.create_line(x,
                                          y_cursor,
                                          x,
                                          y_cursor + sh,
                                          width=2 * draw_scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill=color_black)
                        pview.create_text(x,
                                          y_cursor,
                                          text=b_counter,
                                          tag='grid',
                                          fill=color_black,
                                          font=('courier', round(12 * draw_scale), "normal"),
                                          anchor='sw')
                        b_counter += 1

                    # draw barline at end of the system/line:
                    if obj['type'] == 'endoflinebarline':
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        pview.create_line(x,
                                          y_cursor,
                                          x,
                                          y_cursor + sh,
                                          width=2 * draw_scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill=color_black)

                    # draw the last barline that's more thick
                    if obj['type'] == 'endbarline':
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        pview.create_line(x,
                                          y_cursor,
                                          x,
                                          y_cursor + sh,
                                          width=6 * draw_scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill=color_black)

                    # grid
                    if obj['type'] == 'gridline':
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        pview.create_line(x,
                                          y_cursor,
                                          x,
                                          y_cursor + sh,
                                          width=.5 * draw_scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill=color_black,
                                          dash=(6, 6))

                    # note start
                    if obj['type'] in ['note', 'split']:
                        if not idx_l:
                            x0 = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                            x1 = event_x_pos_engrave(obj['time'] + obj['duration'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x0 = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                            x1 = event_x_pos_engrave(obj['time'] + obj['duration'], split_times[idx_l],split_times[idx_l + 1])
                        y = note_y_pos(obj['pitch'], mn, mx, y_cursor, draw_scale)
                        y0 = y - (5 * draw_scale)
                        y1 = y + (5 * draw_scale)

                        # notestop
                        if obj['notestop']:
                            pview.create_line(x1,
                                              y - (5 * draw_scale),
                                              x1, y + (5 * draw_scale),
                                              width=2 * draw_scale,
                                              fill=color_black,
                                              tag=('midi_note','notestop'))

                        # left hand
                        if obj['hand'] == 'l':

                            # # midinote (old design)
                            # pview.create_polygon(x0,
                            #                      y,
                            #                      x0 + (5 * draw_scale),
                            #                      y - (5 * draw_scale),
                            #                      x1 - (5 * draw_scale),
                            #                      y - (5 * draw_scale),
                            #                      x1,
                            #                      y,
                            #                      x1 - (5 * draw_scale),
                            #                      y + (5 * draw_scale),
                            #                      x0 + (5 * draw_scale),
                            #                      y + (5 * draw_scale),
                            #                      fill=Score['properties']['color-left-hand-midinote'],
                            #                      tag='midi_note',
                            #                      width=20 * draw_scale)
                            # midinote (new triangle design)
                            pview.create_polygon(x0,y,
                                x1,y0,
                                x1,y1,            
                                fill=Score['properties']['color-left-hand-midinote'],
                                tag='midi_note',
                                width=20 * draw_scale)

                            if obj['type'] == 'split':
                                pview.create_oval(x0+(2.5*draw_scale),y0+(2.5*draw_scale),
                                    x0+(7.5*draw_scale),y1-(2.5*draw_scale),
                                    fill=color_black,
                                    outline='')

                            if obj['type'] == 'note':
                                if obj['stem-visible']:
                                    # left stem and white space if on barline
                                    pview.create_line(x0,
                                                      y,
                                                      x0,
                                                      y + (25 * draw_scale),
                                                      width=2 * draw_scale,
                                                      tag='stem',
                                                      fill=color_black)
                                    for bl in bl_times:
                                        if diff(obj['time'], bl) < 1:
                                            pview.create_line(x0,
                                                              y - (10 * draw_scale),
                                                              x0,
                                                              y + (30 * draw_scale),
                                                              width=2 * draw_scale,
                                                              tag='white_space',
                                                              fill=color_white)
                                # notehead
                                if obj['pitch'] in BLACK:

                                    pview.create_oval(x0,
                                                      y0,
                                                      x0 + (5 * draw_scale),
                                                      y1,
                                                      tag='black_notestart',
                                                      fill=color_black,
                                                      outline=color_black,
                                                      width=2 * draw_scale)
                                    # left dot black
                                    pview.create_oval(x0 + (1.5 * draw_scale),
                                                      y + (1 * draw_scale),
                                                      x0 + (3.5 * draw_scale),
                                                      y - (1 * draw_scale),
                                                      tag='left_dot',
                                                      fill=color_white,
                                                      outline='')
                                else:
                                    pview.create_oval(x0,
                                                      y0,
                                                      x0 + (10 * draw_scale),
                                                      y1,
                                                      tag='white_notestart',
                                                      fill=color_white,
                                                      outline=color_black,
                                                      width=2 * draw_scale)
                                    # left dot white
                                    pview.create_oval(x0 + (((10 / 2) - 1) * draw_scale),
                                                      y + (1 * draw_scale),
                                                      x0 + (((10 / 2) + 1) * draw_scale),
                                                      y - (1 * draw_scale),
                                                      tag='left_dot',
                                                      fill=color_black,
                                                      outline='')

                        # right hand
                        else:
                            # # midinote (old design)
                            # pview.create_polygon(x0,
                            #                      y,
                            #                      x0 + (5 * draw_scale),
                            #                      y - (5 * draw_scale),
                            #                      x1 - (5 * draw_scale),
                            #                      y - (5 * draw_scale),
                            #                      x1,
                            #                      y,
                            #                      x1 - (5 * draw_scale),
                            #                      y + (5 * draw_scale),
                            #                      x0 + (5 * draw_scale),
                            #                      y + (5 * draw_scale),
                            #                      fill=Score['properties']['color-right-hand-midinote'],
                            #                      tag='midi_note',
                            #                      width=20 * draw_scale)
                            # midinote (new triangle design)
                            pview.create_polygon(x0,y,
                                x1,y0,
                                x1,y1,            
                                fill=Score['properties']['color-left-hand-midinote'],
                                tag='midi_note',
                                width=20 * draw_scale)

                            if obj['type'] == 'split':
                                pview.create_oval(x0+(2.5*draw_scale),y0+(2.5*draw_scale),
                                    x0+(7.5*draw_scale),y1-(2.5*draw_scale),
                                    fill=color_black,
                                    outline='')

                            if obj['type'] == 'note':
                                if obj['stem-visible']: 
                                    # right stem and white space if on barline
                                    pview.create_line(x0,
                                                      y,
                                                      x0,
                                                      y - (25 * draw_scale),
                                                      width=2 * draw_scale,
                                                      tag='stem',
                                                      fill=color_black)
                                    for bl in bl_times:
                                        if diff(obj['time'], bl) < 1:
                                            pview.create_line(x0,
                                                              y - (30 * draw_scale),
                                                              x0,
                                                              y + (10 * draw_scale),
                                                              width=2 * draw_scale,
                                                              tag='white_space',
                                                              fill=color_white)
                                # notehead
                                if obj['pitch'] in BLACK:
                                    pview.create_oval(x0,
                                                      y0,
                                                      x0 + (5 * draw_scale),
                                                      y1,
                                                      tag='black_notestart',
                                                      fill=color_black,
                                                      outline=color_black,
                                                      width=2 * draw_scale)
                                else:
                                    pview.create_oval(x0,
                                                      y0,
                                                      x0 + (10 * draw_scale),
                                                      y1,
                                                      tag='white_notestart',
                                                      fill=color_white,
                                                      outline=color_black,
                                                      width=2 * draw_scale)

                        # connect stems if abs(evt['time'] - note['time']) <= 1
                        for stem in line:
                            if abs(stem['time'] - obj['time']) <= 1 and stem['type'] == 'note' and stem['pitch'] != obj['pitch']:
                                if abs(stem['time'] - obj['time']) <= 1 and stem['hand'] == obj['hand']:
                                    stem_y = note_y_pos(stem['pitch'], mn, mx, y_cursor, draw_scale)
                                    if not idx_l:
                                        stem_x = event_x_pos_engrave(stem['time'], split_times[idx_l], split_times[idx_l + 1],True)
                                    else:
                                        stem_x = event_x_pos_engrave(stem['time'], split_times[idx_l], split_times[idx_l + 1])
                                    pview.create_line(stem_x,
                                                      stem_y,
                                                      x0,
                                                      y,
                                                      width=2 * draw_scale,
                                                      capstyle='round',
                                                      tag='connect_stem',
                                                      fill=color_black)

                    # time signature text
                    if obj['type'] == 'time_signature_text':
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        pview.create_text(x + (2.5 * draw_scale),
                                          y_cursor + sh + (40 * draw_scale),
                                          text=obj['text'],
                                          tag='tsigtext',
                                          anchor='sw',
                                          font=('courier', 10, 'underline'),
                                          fill=color_black)

                    # text
                    if obj['type'] == 'text':
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        y = note_y_pos(obj['pitch'], mn, mx, y_cursor, draw_scale)
                        if obj['vert'] == 0:
                            t = pview.create_text(x,
                                                  y,
                                                  text=obj['text'],
                                                  tag='text',
                                                  anchor='w',
                                                  font=('Courier', 10, 'normal'),
                                                  fill=color_black)
                            round_rectangle(pview, pview.bbox(t)[0]-(1*draw_scale),
                                            pview.bbox(t)[1]-(1*draw_scale),
                                            pview.bbox(t)[2]+(5*draw_scale),
                                            pview.bbox(t)[3]-(1*draw_scale),
                                            fill=color_white,
                                            outline='',
                                            width=.5,
                                            tag='textbg')
                        else:
                            t = pview.create_text(x,
                                                  y,
                                                  text=obj['text'],
                                                  tag='text',
                                                  anchor='n',
                                                  font=('Courier', 10, 'normal'),
                                                  fill=color_black,
                                                  angle=90)
                            round_rectangle(pview, pview.bbox(t)[0]-(1*draw_scale),
                                            pview.bbox(t)[1]-(1*draw_scale),
                                            pview.bbox(t)[2]-(1*draw_scale),
                                            pview.bbox(t)[3]+(5*draw_scale),
                                            fill=color_white,
                                            outline='',
                                            width=.5,
                                            tag='textbg')

                    # count_line
                    if obj['type'] == 'countline':
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        y1 = note_y_pos(obj['pitch1'], mn, mx, y_cursor, draw_scale)
                        y2 = note_y_pos(obj['pitch2'], mn, mx, y_cursor, draw_scale)

                        pview.create_line(x,
                                          y1,
                                          x,
                                          y2,
                                          dash=(2, 2),
                                          tag='countline',
                                          fill=color_black,
                                          width=1*draw_scale)

                    # start repeat
                    if obj['type'] == 'startrepeat':
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        pview.create_line(x,y_cursor,
                            x,y_cursor-(40*draw_scale),
                            width=2*draw_scale,
                            capstyle='round',
                            fill=color_black)
                        pview.create_line(x,y_cursor-(40*draw_scale),
                            x+(20*draw_scale),y_cursor-(40*draw_scale),
                            arrow='last',
                            fill=color_black,
                            width=2*draw_scale)
                    # end repeat
                    if obj['type'] == 'endrepeat':
                        if not idx_l:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True)
                        else:
                            x = event_x_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1])
                        pview.create_line(x,y_cursor,
                            x,y_cursor-(40*draw_scale),
                            width=2*draw_scale,
                            capstyle='round',
                            fill=color_black)
                        pview.create_line(x,y_cursor-(40*draw_scale),
                            x-(20*draw_scale),y_cursor-(40*draw_scale),
                            arrow='last',
                            fill=color_black,
                            width=2*draw_scale)

                    # end for obj ----------------------------------------

                # if this is the first line of the file:
                if not idx_l and minipiano:
                    draw_staff(y_cursor,
                        mn,
                        mx,
                        p_marg_l,
                        page_width,
                        p_marg_r,
                        color_black,
                        draw_scale,
                        pview,
                        sh,
                        True)
                else:
                    draw_staff(y_cursor,
                        mn,
                        mx,
                        p_marg_l,
                        page_width,
                        p_marg_r,
                        color_black,
                        draw_scale,
                        pview,
                        sh,
                        False)

                # update y_cursor and divide the systems equal:
                y_cursor += sh + lmd + (page_spacing[idx_p] / (len(DOC[idx_p])) / 2)

                idx_l += 1

                # end for line ---------------------------------------

            y_cursor = page_height * (idx_p + 1)


        # draw bottom line page
        if not render_type:
            pview.create_line(0,
                page_height,
                page_width,
                page_height,
                fill=color_black,
                width=2,
                dash=(6,4,5,2,3,1))

        # drawing order
        pview.tag_raise('staff')
        pview.tag_raise('notestop')
        pview.tag_raise('grid')
        pview.tag_raise('white_space')
        pview.tag_raise('stem')
        pview.tag_raise('white_notestart')
        pview.tag_raise('black_notestart')
        pview.tag_raise('connect_stem')
        pview.tag_raise('titles')
        pview.tag_raise('cursor')
        pview.tag_raise('endpaper')
        pview.tag_raise('left_dot')
        pview.tag_raise('tie_dot')
        pview.tag_raise('textbg')
        pview.tag_raise('text')
        pview.tag_raise('countline')
        #pview.tag_lower('midi_note')
        
        # make the new render update fluently(without blinking) and scale
        if not render_type == 'export':    
            root.update()
            s = pview.winfo_width() / page_width
            pview.scale("all", 0, 0, s, s)
        pview.move('all', 10000, 0)
        pview.delete('old')
        if not render_type == 'export':
            pview.configure(scrollregion=pview.bbox("all"))
        pview.addtag_all('old')

    draw()

    return len(DOC)
