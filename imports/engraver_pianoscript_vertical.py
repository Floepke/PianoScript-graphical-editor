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


def draw_staff_vert(x_cursor,
    mn,
    mx,
    p_marg_u,
    p_marg_d,
    p_marg_l,
    p_marg_r,
    page_height,
    page_width,
    header_h,
    footer_h,
    draw_scale,
    color_black,
    pview,
    st_width,
    minipiano=True):

    print_height = page_height - p_marg_u - p_marg_d
    
    def two(x):
        if minipiano:
            y2 = page_height - p_marg_d - footer_h - (40 * draw_scale)
            pview.create_line(
                x,
                y2,
                x,
                page_height - p_marg_d - footer_h - (20 * draw_scale),
                fill=color_black,
                width=5*draw_scale,
                capstyle='round')
            pview.create_line(
                x+(10*draw_scale),
                y2,
                x+(10*draw_scale),
                page_height - p_marg_d - footer_h - (20 * draw_scale),
                fill=color_black,
                width=5*draw_scale,
                capstyle='round')
        else:
            y2 = page_height - p_marg_d - footer_h
        pview.create_line(
            x,
            p_marg_u + header_h,
            x,
            y2,
            fill=color_black,
            width=1*draw_scale,
            capstyle='round')
        pview.create_line(
            x+(10*draw_scale),
            p_marg_u + header_h,
            x+(10*draw_scale),
            y2,
            fill=color_black,
            width=1*draw_scale,
            capstyle='round')
    
    def three(x):
        if minipiano:
            y2 = page_height - p_marg_d - footer_h - (40 * draw_scale)
            pview.create_line(
                x,
                y2,
                x,
                page_height - p_marg_d - footer_h - (20 * draw_scale),
                fill=color_black,
                width=5*draw_scale,
                capstyle='round')
            pview.create_line(
                x+(10*draw_scale),
                y2,
                x+(10*draw_scale),
                page_height - p_marg_d - footer_h - (20 * draw_scale),
                fill=color_black,
                width=5*draw_scale,
                capstyle='round')
            pview.create_line(
                x+(20*draw_scale),
                y2,
                x+(20*draw_scale),
                page_height - p_marg_d - footer_h - (20 * draw_scale),
                fill=color_black,
                width=5*draw_scale,
                capstyle='round')
        else:
            y2 = page_height - p_marg_d - footer_h
        pview.create_line(
            x,
            p_marg_u + header_h,
            x,
            y2,
            fill=color_black,
            width=1.5*draw_scale,
            capstyle='round')
        pview.create_line(
            x+(10*draw_scale),
            p_marg_u + header_h,
            x+(10*draw_scale),
            y2,
            fill=color_black,
            width=1.5*draw_scale,
            capstyle='round')
        pview.create_line(
            x+(20*draw_scale),
            p_marg_u + header_h,
            x+(20*draw_scale),
            y2,
            fill=color_black,
            width=1.5*draw_scale,
            capstyle='round')
        
    def clef(x):
        if minipiano:
            y2 = page_height - p_marg_d - footer_h - (40 * draw_scale)
            pview.create_line(
                x,
                y2,
                x,
                page_height - p_marg_d - footer_h - (20 * draw_scale),
                fill=color_black,
                width=5*draw_scale,
                capstyle='round')
            pview.create_line(
                x+(10*draw_scale),
                y2,
                x+(10*draw_scale),
                page_height - p_marg_d - footer_h - (20 * draw_scale),
                fill=color_black,
                width=5*draw_scale,
                capstyle='round')
        else:
            y2 = page_height - p_marg_d - footer_h
        pview.create_line(
            x,
            p_marg_u + header_h,
            x,
            y2,
            fill=color_black,
            width=1*draw_scale,
            capstyle='round',
            dash=(6,6))
        pview.create_line(
            x+(10*draw_scale),
            p_marg_u + header_h,
            x+(10*draw_scale),
            y2,
            fill=color_black,
            width=1*draw_scale,
            capstyle='round',
            dash=(6,6))

    # control flow for engraving the right composition of staff-lines
    clefline = 0
    if mn <= 3:
        if not minipiano:
            pview.create_line(x_cursor,
                p_marg_u + header_h,
                x_cursor,
                page_height - p_marg_d - footer_h,
                width=2*draw_scale,
                fill=color_black,
                capstyle='round')
        else:
            pview.create_line(x_cursor,
                p_marg_u + header_h,
                x_cursor,
                page_height - p_marg_d - footer_h - (40 * draw_scale),
                width=2*draw_scale,
                fill=color_black,
                capstyle='round')
            pview.create_line(x_cursor,
                page_height - p_marg_d - footer_h - (20 * draw_scale),
                x_cursor,
                page_height - p_marg_d - footer_h - (40 * draw_scale),
                width=5*draw_scale,
                fill=color_black,
                capstyle='round')
        two(x_cursor + (20*draw_scale))
        three(x_cursor + (50*draw_scale))
        two(x_cursor + (90*draw_scale))
        three(x_cursor + (120*draw_scale))
        two(x_cursor + (160*draw_scale))
        three(x_cursor + (190*draw_scale))
        clefline = 230 * draw_scale
    if mn >= 4 and mn <= 8:
        two(x_cursor)
        three(x_cursor + (30*draw_scale))
        two(x_cursor + (70*draw_scale))
        three(x_cursor + (100*draw_scale))
        two(x_cursor + (140*draw_scale))
        three(x_cursor + (170*draw_scale))
        clefline = 210 * draw_scale
    if mn >= 9 and mn <= 15:
        three(x_cursor)
        two(x_cursor + (40*draw_scale))
        three(x_cursor + (70*draw_scale))
        two(x_cursor + (110*draw_scale))
        three(x_cursor + (140*draw_scale))
        clefline = 180 * draw_scale
    if mn >= 16 and mn <= 20:
        two(x_cursor)
        three(x_cursor + (30*draw_scale))
        two(x_cursor + (70*draw_scale))
        three(x_cursor + (100*draw_scale))
        clefline = 140 * draw_scale
    if mn >= 21 and mn <= 27:
        three(x_cursor)
        two(x_cursor + (40*draw_scale))
        three(x_cursor + (70*draw_scale))
        clefline = 110 * draw_scale
    if mn >= 28 and mn <= 32:
        two(x_cursor)
        three(x_cursor + (30*draw_scale))
        clefline = 70 * draw_scale
    if mn >= 33 and mn <= 39:
        three(x_cursor)
        clefline = 40 * draw_scale
    clef(x_cursor + (clefline))
    if mx >= 45 and mx <= 51:
        three(x_cursor + clefline + (30*draw_scale))
    if mx >= 52 and mx <= 56:
        three(x_cursor + clefline + (30*draw_scale))
        two(x_cursor + clefline + (70*draw_scale))
    if mx >= 57 and mx <= 63:
        three(x_cursor + clefline + (30*draw_scale))
        two(x_cursor + clefline + (70*draw_scale))
        three(x_cursor + clefline + (100*draw_scale))
    if mx >= 64 and mx <= 68:
        three(x_cursor + clefline + (30*draw_scale))
        two(x_cursor + clefline + (70*draw_scale))
        three(x_cursor + clefline + (100*draw_scale))
        two(x_cursor + clefline + (140*draw_scale))
    if mx >= 69 and mx <= 75:
        three(x_cursor + clefline + (30*draw_scale))
        two(x_cursor + clefline + (70*draw_scale))
        three(x_cursor + clefline + (100*draw_scale))
        two(x_cursor + clefline + (140*draw_scale))
        three(x_cursor + clefline + (170*draw_scale))
    if mx >= 76 and mx <= 80:
        three(x_cursor + clefline + (30*draw_scale))
        two(x_cursor + clefline + (70*draw_scale))
        three(x_cursor + clefline + (100*draw_scale))
        two(x_cursor + clefline + (140*draw_scale))
        three(x_cursor + clefline + (170*draw_scale))
        two(x_cursor + clefline + (210*draw_scale))
    if mx >= 81:
        three(x_cursor + clefline + (30*draw_scale))
        two(x_cursor + clefline + (70*draw_scale))
        three(x_cursor + clefline + (100*draw_scale))
        two(x_cursor + clefline + (140*draw_scale))
        three(x_cursor + clefline + (170*draw_scale))
        two(x_cursor + clefline + (210*draw_scale))
        three(x_cursor + clefline + (240*draw_scale))

    # draw minipiano border
    if minipiano:
        pview.create_line(x_cursor+st_width,
            page_height - p_marg_d - footer_h - (40*draw_scale),
            x_cursor+st_width+(20*draw_scale),
            page_height - p_marg_d - footer_h - (40*draw_scale),
            fill=color_black,
            width=1*draw_scale)
        pview.create_line(x_cursor,
            page_height - p_marg_d - footer_h - (40*draw_scale),
            x_cursor-(20*draw_scale),
            page_height - p_marg_d - footer_h - (40*draw_scale),
            fill=color_black,
            width=1*draw_scale)
        pview.create_line(x_cursor-(20*draw_scale),
            page_height - p_marg_d - footer_h - (40*draw_scale),
            x_cursor-(20*draw_scale),
            page_height - p_marg_d - footer_h,
            fill=color_black,
            width=1*draw_scale)
        pview.create_line(x_cursor+st_width+(20*draw_scale),
            page_height - p_marg_d - footer_h - (40*draw_scale),
            x_cursor+st_width+(20*draw_scale),
            page_height - p_marg_d - footer_h,
            fill=color_black,
            width=1*draw_scale)
        pview.create_line(x_cursor-(20*draw_scale),
            page_height - p_marg_d - footer_h,
            x_cursor+st_width+(20*draw_scale),
            page_height - p_marg_d - footer_h,
            fill=color_black,
            width=1*draw_scale)





























def engrave_pianoscript_vertical(render_type,
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
    header_h = Score['properties']['header-height'] * MM
    footer_h = Score['properties']['footer-height'] * MM
    draw_scale = Score['properties']['draw-scale']
    line_break = Score['events']['line-break']
    count_line = Score['events']['count-line']
    staff_sizer = Score['events']['staff-sizer']
    start_repeat = Score['events']['start-repeat']
    end_repeat = Score['events']['end-repeat']
    beam = Score['events']['beam']
    color_right_midinote = Score['properties']['color-right-hand-midinote']
    color_left_midinote = Score['properties']['color-left-hand-midinote']
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
        staff_width = []
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
        for e in note:
            e['type'] = 'note'
            e = note_split_processor(e, Score)
            for ev in e:
                DOC.append(ev)
        for e in text:
            e['type'] = 'text'
            DOC.append(e)
        for e in bpm:
            e['type'] = 'bpm'
            DOC.append(e)
        for e in slur:
            e['type'] = 'slur'
            DOC.append(e)
        for e in pedal:
            e['type'] = 'pedal'
            DOC.append(e)
        for e in count_line:
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
        for e in beam:
            e['type'] = 'beam'
            DOC.append(e)

        # now we sort the events on time-key
        DOC = sorted(DOC, key=lambda y: y['time'])

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

        # we make a list that contains all staff widths
        for l in DOC:
            pitches = []
            for e in l:
                if e['type'] in ['note', 'split', 'invis']:
                    pitches.append(e['pitch'])
            try:
                staff_width.append(staff_height_width(min(pitches),max(pitches),draw_scale))
            except ValueError:
                staff_width.append(10*draw_scale)

        DOC.pop(-1)
        staff_width.pop(-1)

        # in this part we calculate how many systems fit on each page
        # also we gather the free space in the printarea in a list
        # called 'page_spacing'.
        doc = DOC
        DOC = []
        x_cursor = 0
        printarea_width = (page_width - p_marg_l - p_marg_r)
        remaining_space = 0
        page = []
        for line, sw, c in zip(doc,staff_width, range(len(doc))):
            lmu = line_break[c]['margin-up-left'] * MM
            lmd = line_break[c]['margin-down-right'] * MM
            x_cursor += lmu + sw + lmd
            # if the line fits on paper:
            if x_cursor <= printarea_width:
                page.append(line)
                remaining_space = printarea_width - x_cursor
            # if the line does NOT fit on paper:
            else:
                x_cursor = lmu + sw + lmd
                DOC.append(page)
                page = []
                page.append(line)
                page_spacing.append(remaining_space)
                remaining_space = printarea_width - x_cursor
            # if this is the last line:
            if c+1 == len(doc):
                DOC.append(page)
                page_spacing.append(remaining_space)
                    
        return DOC, page_spacing, staff_width, split_times, bl_times

    DOC, page_spacing, staff_width, split_times, bl_times = read()

    #------------------
    # debugging prints
    # print('page_spacing: ', page_spacing, '\nstaff_heights: ', len(staff_width))

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
    
























    
    def event_y_pos_engrave(pos,start_line_tick,end_line_tick, include_header=False, minipiano=False):
        '''
        returns the yy position on the paper.
        '''
        factor = interpolation(start_line_tick, end_line_tick, pos)
        if include_header:
            hh = header_h
        else:
            hh = 0
        if not minipiano:
            return p_marg_u + hh + ((page_height - p_marg_u - p_marg_d - footer_h - hh) * factor)
        else:
            return p_marg_u + hh + ((page_height - p_marg_u - p_marg_d - footer_h - (40 * draw_scale) - hh) * factor)

    def note_x_pos(note, mn, mx, x_cursor, scale):
        '''
        returns the position of the given note relative to 'x_cursor'(the xx axis staff cursor).
        '''
        xlist = [-5,0,5,15,20,25,30,35,45,50,55,60,65,70,75,
        85,90,95,100,105,115,120,125,130,135,140,145,
        155,160,165,170,175,185,190,195,200,205,210,215,
        225,230,235,240,245,255,260,265,270,275,280,285,
        295,300,305,310,315,325,330,335,340,345,350,355, 
        365,370,375,380,385,395,400,405,410,415,420,425,
        435,440,445,450,455,465,470,475,480,485,490,495]
        sub = 0
        if mn >= 4 and mn <= 8:
            sub = 20
        if mn >= 9 and mn <= 15:
            sub = 50
        if mn >= 16 and mn <= 20:
            sub = 90
        if mn >= 21 and mn <= 27:
            sub = 120
        if mn >= 28 and mn <= 32:
            sub = 160
        if mn >= 33 and mn <= 39:
            sub = 190
        if mn >= 40:
            sub = 230
        return x_cursor + (xlist[note - 1] * scale) - (sub * scale)

    def draw():
        '''
            I try to draw everything as efficient as possible from
            the ordered DOC list using many nested if/else flow.
            I found it the best way to draw.

            things we need to know/keep track on:
                - x_cursor
                - page_spacings
                - staff_heights
        '''
        # set colors
        if render_type == 'export':
            color_black = 'black'
            color_white = 'white'
        else:
            color_black = color_notation_editor
            color_white = color_editor_canvas

        x_cursor = 0
        idx_l = 0
        len_doc = len(DOC)
        b_counter = update_bcounter(DOC,pageno % len_doc)
        for idx_p, page in enumerate(DOC):

            # render only one page
            if not render_type == 'export':
                if idx_p == pageno % len_doc:
                    ...
                else:
                    for l in page:
                        idx_l += 1
                    continue
            
            # draw paper
            if not render_type:
                pview.create_line(0,
                    x_cursor,
                    page_width,
                    x_cursor,
                    fill=color_black,
                    width=2,
                    dash=(6,4,5,2,3))

            # draw footer (page numbering, title and copyright notice
            pview.create_text(x_cursor + p_marg_l,
                page_height - p_marg_d,
                text='page ' + str(idx_p+1) + ' of ' + str(len_doc) + ' | ' + title['text'] + ' | ' + copyright['text'],
                anchor='sw',
                fill=color_black,
                font=('courier', 12, "normal"))

            if not idx_p: # if on the first page
                # draw header (title & composer text)
                pview.create_text(x_cursor + p_marg_l,
                    p_marg_u,
                    text=Score['header']['title']['text'],
                    anchor='nw',
                    font=('courier', 18, "bold"),
                    fill=color_black)
                pview.create_text(x_cursor + page_width - p_marg_r,
                    p_marg_u,
                    text=Score['header']['composer']['text'],
                    anchor='ne',
                    font=('courier', 12, "normal"),
                    fill=color_black)

            x_cursor += p_marg_l
            
            for idx_ll, line in enumerate(page):

                sw = staff_width[idx_l]
                lmu = line_break[idx_l]['margin-up-left'] * MM
                lmd = line_break[idx_l]['margin-down-right'] * MM
                
                x_cursor += lmu + (page_spacing[idx_p] / (len(DOC[idx_p])) / 2)

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
                    ...
                    # barline and numbering
                    if obj['type'] == 'barline':
                        if not idx_l and not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                        elif not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        else:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                        pview.create_line(x_cursor,
                                          yy,
                                          x_cursor+sw,
                                          yy,
                                          width=.75 * draw_scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill=color_black)
                        pview.create_text(x_cursor+sw+(20*draw_scale),
                                          yy+(3*draw_scale),
                                          text=b_counter,
                                          tag='grid',
                                          fill=color_black,
                                          font=('courier', round(14 * draw_scale), "normal"),
                                          anchor='nw')
                        b_counter += 1

                    # draw barline at end of the system/line:
                    if obj['type'] == 'endoflinebarline':
                        if not idx_l and not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                        elif not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        else:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                        pview.create_line(x_cursor,
                                          yy,
                                          x_cursor+sw,
                                          yy,
                                          width=.75 * draw_scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill=color_black)

                    # draw the last barline that's more thick
                    if obj['type'] == 'endbarline':
                        if not idx_l and not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                        elif not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        else:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                        pview.create_line(x_cursor,
                                          yy,
                                          x_cursor+sw,
                                          yy,
                                          width=4 * draw_scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill=color_black)

                    # grid
                    if obj['type'] == 'gridline':
                        if not idx_l and not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                        elif not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        else:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                        pview.create_line(x_cursor,
                                          yy,
                                          x_cursor+sw,
                                          yy,
                                          width=1 * draw_scale,
                                          capstyle='round',
                                          tag='grid',
                                          fill=color_black,
                                          dash=(6, 6))

                    # note start
                    if obj['type'] in ['note', 'split']:
                        if not idx_l and not idx_p:
                            y0 = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                            y1 = event_y_pos_engrave(obj['time'] + obj['duration'], split_times[idx_l], split_times[idx_l + 1],True,True)
                        elif not idx_p:
                            y0 = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                            y1 = event_y_pos_engrave(obj['time'] + obj['duration'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        else:
                            y0 = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                            y1 = event_y_pos_engrave(obj['time'] + obj['duration'], split_times[idx_l],split_times[idx_l + 1],False,False)
                        xx = note_x_pos(obj['pitch'], mn, mx, x_cursor, draw_scale)
                        x0 = xx - (5 * draw_scale)
                        x1 = xx + (5 * draw_scale)

                        # notestop
                        if obj['notestop']:
                            pview.create_line(x0,
                                              y1, 
                                              x1,
                                              y1,
                                              width=1.5 * draw_scale,
                                              fill=color_black,
                                              tag=('midi_note','notestop'))

                        # left hand
                        if obj['hand'] == 'l':
                            # midinote
                            pview.create_line(
                                xx,y0,
                                xx,y1,
                                fill=Score['properties']['color-left-hand-midinote'],
                                tag='midi_note',
                                width=10 * draw_scale)

                            if obj['type'] == 'split':
                                pview.create_oval(xx+(2.5*draw_scale),y0+(2.5*draw_scale),
                                    xx-(2.5*draw_scale),y0+(7.5*draw_scale),
                                    fill=color_black,
                                    outline='')

                            if obj['type'] == 'note':
                                if obj['stem-visible']:
                                    # left stem and white space if on barline
                                    pview.create_line(xx,
                                                      y0,
                                                      xx - (25 * draw_scale),
                                                      y0,
                                                      width=3 * draw_scale,
                                                      tag='stem',
                                                      fill=color_black,
                                                      capstyle='round')
                                    # for bl in bl_times:
                                    #     if diff(obj['time'], bl) < 1:
                                    #         pview.create_line(xx + (10 * draw_scale),
                                    #                           y0,
                                    #                           xx - (30 * draw_scale),
                                    #                           y0,
                                    #                           width=2 * draw_scale,
                                    #                           tag='white_space',
                                    #                           fill=color_white)
                                # notehead
                                if obj['pitch'] in BLACK:

                                    pview.create_oval(xx-(2.5*draw_scale),
                                                      y0,
                                                      xx+(2.5*draw_scale),
                                                      y0 + (10 * draw_scale),
                                                      tag='black_notestart',
                                                      fill=color_black,
                                                      outline=color_black,
                                                      width=2 * draw_scale)
                                    # left dot black
                                    pview.create_oval(xx - (1*draw_scale),
                                                      y0 + (4 * draw_scale),
                                                      xx + (1*draw_scale),
                                                      y0 + (6 * draw_scale),
                                                      tag='left_dot',
                                                      fill=color_white,
                                                      outline='')
                                else:
                                    pview.create_oval(x0,
                                                      y0,
                                                      x1,
                                                      y0 + (10 * draw_scale),
                                                      tag='white_notestart',
                                                      fill=color_white,
                                                      outline=color_black,
                                                      width=2 * draw_scale)
                                    # left dot white
                                    pview.create_oval(xx + (1*draw_scale),
                                                      y0 + (((10 / 2) - 1) * draw_scale),
                                                      xx - (1*draw_scale),
                                                      y0 + (((10 / 2) + 1) * draw_scale),
                                                      tag='left_dot',
                                                      fill=color_black,
                                                      outline='')

                        # right hand
                        else:
                            pview.create_line(xx,y0,xx,y1,
                                fill=Score['properties']['color-right-hand-midinote'],
                                tag='midi_note',
                                width=10 * draw_scale)

                            if obj['type'] == 'split':
                                pview.create_oval(xx+(2.5*draw_scale),y0+(2.5*draw_scale),
                                    xx-(2.5*draw_scale),y0+(7.5*draw_scale),
                                    fill=color_black,
                                    outline='')

                            if obj['type'] == 'note':
                                if obj['stem-visible']:
                                    # right stem and white space if on barline
                                    pview.create_line(xx,
                                                      y0,
                                                      xx + (25 * draw_scale),
                                                      y0,
                                                      width=3 * draw_scale,
                                                      tag='stem',
                                                      fill=color_black,
                                                      capstyle='round')
                                    # for bl in bl_times:
                                    #     if diff(obj['time'], bl) < 1:
                                    #         pview.create_line(xx - (10 * draw_scale),
                                    #                           y0,
                                    #                           xx + (30 * draw_scale),
                                    #                           y0,
                                    #                           width=2 * draw_scale,
                                    #                           tag='white_space',
                                    #                           fill=color_white)
                                # notehead
                                if obj['pitch'] in BLACK:
                                    pview.create_oval(xx-(2.5*draw_scale),
                                                      y0,
                                                      xx+(2.5*draw_scale),
                                                      y0 + (10 * draw_scale),
                                                      tag='black_notestart',
                                                      fill=color_black,
                                                      outline=color_black,
                                                      width=2 * draw_scale)
                                else:
                                    pview.create_oval(x0,
                                                      y0,
                                                      x1,
                                                      y0 + (10 * draw_scale),
                                                      tag='white_notestart',
                                                      fill=color_white,
                                                      outline=color_black,
                                                      width=2 * draw_scale)
                        if obj['stem-visible']:
                            # connect stems; abs(evt['time'] - note['time']) <= 1
                            for stem in line:
                                if abs(stem['time'] - obj['time']) <= 1 and stem['type'] == 'note' and stem['pitch'] != obj['pitch']:
                                    if abs(stem['time'] - obj['time']) <= 1 and stem['hand'] == obj['hand']:
                                        stem_x = note_x_pos(stem['pitch'], mn, mx, x_cursor, draw_scale)
                                        if not idx_l and not idx_p:
                                            stem_y = event_y_pos_engrave(stem['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                                        elif not idx_p:
                                            stem_y = event_y_pos_engrave(stem['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                                        else:
                                            stem_y = event_y_pos_engrave(stem['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                                        pview.create_line(stem_x,
                                                          stem_y,
                                                          xx,
                                                          y0,
                                                          width=3 * draw_scale,
                                                          capstyle='round',
                                                          tag='connect_stem',
                                                          fill=color_black)

                    # time signature text
                    if obj['type'] == 'time_signature_text':
                        if not idx_l and not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                        elif not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        else:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                        pview.create_text(x_cursor - (20 * draw_scale), 
                                          yy + (3 * draw_scale),
                                          text=obj['text'],
                                          tag='tsigtext',
                                          anchor='w',
                                          font=('courier', 14, 'bold'),
                                          fill=color_black,
                                          angle=-90)

                    # text
                    if obj['type'] == 'text':
                        if not idx_l and not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                        elif not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        else:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                        xx = note_x_pos(obj['pitch'], mn, mx, x_cursor, draw_scale)
                        if obj['vert'] == 1:
                            t = pview.create_text(xx,
                                                  yy,
                                                  text=obj['text'],
                                                  tag='text',
                                                  anchor='nw',
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
                            t = pview.create_text(xx,
                                                  yy,
                                                  text=obj['text'],
                                                  tag='text',
                                                  anchor='w',
                                                  font=('Courier', 10, 'normal'),
                                                  fill=color_black,
                                                  angle=-90)
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
                        if not idx_l and not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                        elif not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        else:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                        x1 = note_x_pos(obj['pitch1'], mn, mx, x_cursor, draw_scale)
                        x2 = note_x_pos(obj['pitch2'], mn, mx, x_cursor, draw_scale)

                        pview.create_line(x1,
                                          yy,
                                          x2,
                                          yy,
                                          dash=(2, 2),
                                          tag='countline',
                                          fill=color_black,
                                          width=1*draw_scale)

                    # start repeat
                    if obj['type'] == 'startrepeat':
                        if not idx_l and not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                        elif not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        else:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                        pview.create_line(x_cursor,yy,
                            x_cursor+sw+(50*draw_scale),yy,
                            width=2*draw_scale,
                            capstyle='round',
                            fill=color_black,
                            dash=(1,2))
                        pview.create_oval(x_cursor+sw+(40*draw_scale),yy+(5*draw_scale),
                            x_cursor+sw+(45*draw_scale),yy+(10*draw_scale),
                            fill=color_black,
                            width=2*draw_scale,
                            outline=color_black)
                        pview.create_oval(x_cursor+sw+(30*draw_scale),yy+(5*draw_scale),
                            x_cursor+sw+(35*draw_scale),yy+(10*draw_scale),
                            fill=color_black,
                            width=2*draw_scale,
                            outline=color_black)
                    # end repeat
                    if obj['type'] == 'endrepeat':
                        if not idx_l and not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                        elif not idx_p:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        else:
                            yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                        pview.create_line(x_cursor+sw,yy,
                            x_cursor+sw+(50*draw_scale),yy,
                            width=2*draw_scale,
                            capstyle='round',
                            fill=color_black,
                            dash=(1,2))
                        pview.create_oval(x_cursor+sw+(40*draw_scale),yy-(5*draw_scale),
                            x_cursor+sw+(45*draw_scale),yy-(10*draw_scale),
                            fill=color_black,
                            width=2*draw_scale,
                            outline=color_black)
                        pview.create_oval(x_cursor+sw+(30*draw_scale),yy-(5*draw_scale),
                            x_cursor+sw+(35*draw_scale),yy-(10*draw_scale),
                            fill=color_black,
                            width=2*draw_scale,
                            outline=color_black)
                    
                    # beam grouping
                    if obj['type'] == 'beam':
                        
                        # beam right hand
                        if obj['hand'] == 'r':
                            beamnotelist = []
                            # right beam
                            for n in line:
                                if n['type'] == 'note' and n['time'] >= obj['time']+obj['duration']:
                                    break
                                elif n['type'] == 'note' and n['time'] >= obj['time'] and n['time'] < obj['time']+obj['duration'] and obj['hand'] == n['hand'] and n['stem-visible']:
                                    beamnotelist.append(n)
                            # beamnotelist contains now all notes that need to be grouped using a beam.
                            # We check if we have to draw a beam; only if there are two or more notes in the beam:
                            if len(beamnotelist) < 2:
                                continue
                            # first we detect the highest and lowest note from the beam
                            h_note = {"pitch":1}
                            for bm in beamnotelist:
                                if bm['pitch'] >= h_note['pitch']:
                                    h_note = bm
                            h_notex = note_x_pos(h_note['pitch'],mn,mx,x_cursor,draw_scale)
                            # now we have the highest beamnote position, we can draw this simple implementation
                            # for a beam. We draw from the highest position to a small portion higher to the end
                            # of the beam.
                            f_note = beamnotelist[0]
                            l_note = beamnotelist[-1]
                            if not idx_l and not idx_p:
                                f_notey = event_y_pos_engrave(f_note['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                            elif not idx_p:
                                f_notey = event_y_pos_engrave(f_note['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                            else:
                                f_notey = event_y_pos_engrave(f_note['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                            if not idx_l and not idx_p:
                                l_notey = event_y_pos_engrave(l_note['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                            elif not idx_p:
                                l_notey = event_y_pos_engrave(l_note['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                            else:
                                l_notey = event_y_pos_engrave(l_note['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                            if f_notey == l_notey:
                                continue
                            # drawing the beam:
                            pview.create_line(h_notex+(25*draw_scale),f_notey,
                                              h_notex+(30*draw_scale),l_notey,
                                              tag='beam',
                                              width=5*draw_scale,
                                              capstyle='round',
                                              fill=color_black)
                            # now we only have to connect the stems to the beam:
                            for bm in beamnotelist:
                                if not idx_l and not idx_p:
                                    yy = event_y_pos_engrave(bm['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                                elif not idx_p:
                                    yy = event_y_pos_engrave(bm['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                                else:
                                    yy = event_y_pos_engrave(bm['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                                x = note_x_pos(bm['pitch'], mn, mx, x_cursor, draw_scale)
                                stem_length = (5*interpolation(f_notey,l_notey,yy)*draw_scale)
                                pview.create_line(x+(25*draw_scale),yy,
                                                    h_notex+(25*draw_scale)+stem_length,yy,
                                                    tag='beam',
                                                    width=3*draw_scale,
                                                    capstyle='round',
                                                    fill=color_black)
                        # beam left hand
                        else:
                            beamnotelist = []
                            # left beam
                            for n in line:
                                if n['type'] == 'note' and n['time'] >= obj['time']+obj['duration']:
                                    break
                                elif n['type'] == 'note' and n['time'] >= obj['time'] and n['time'] < obj['time']+obj['duration'] and obj['hand'] == n['hand'] and n['stem-visible']:
                                    beamnotelist.append(n)
                            # beamnotelist contains now all notes that need to be grouped using a beam.
                            # We check if we have to draw a beam; only if there are two or more notes in the beam:
                            if len(beamnotelist) < 2:
                                continue
                            # first we detect the highest and lowest note from the beam
                            lw_note = {"pitch":88}
                            for bm in beamnotelist:
                                if bm['pitch'] <= lw_note['pitch']:
                                    lw_note = bm
                            lw_notex = note_x_pos(lw_note['pitch'],mn,mx,x_cursor,draw_scale)
                            # now we have the highest beamnote position, we can draw this simple implementation
                            # for a beam. We draw from the highest position to a small portion higher to the end
                            # of the beam.
                            f_note = beamnotelist[0]
                            l_note = beamnotelist[-1]
                            if not idx_l and not idx_p:
                                f_notey = event_y_pos_engrave(f_note['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                            elif not idx_p:
                                f_notey = event_y_pos_engrave(f_note['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                            else:
                                f_notey = event_y_pos_engrave(f_note['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                            if not idx_l and not idx_p:
                                l_notey = event_y_pos_engrave(l_note['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                            elif not idx_p:
                                l_notey = event_y_pos_engrave(l_note['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                            else:
                                l_notey = event_y_pos_engrave(l_note['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                            if f_notey == l_notey:
                                continue
                            # drawing the beam:
                            pview.create_line(lw_notex-(25*draw_scale),f_notey,
                                              lw_notex-(30*draw_scale),l_notey,
                                              tag='beam',
                                              width=5*draw_scale,
                                              capstyle='round',
                                              fill=color_black)
                            # now we only have to connect the stems to the beam:
                            for bm in beamnotelist:
                                if not idx_l and not idx_p:
                                    yy = event_y_pos_engrave(bm['time'], split_times[idx_l], split_times[idx_l + 1],True,True)
                                elif not idx_p:
                                    yy = event_y_pos_engrave(bm['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                                else:
                                    yy = event_y_pos_engrave(bm['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                                x = note_x_pos(bm['pitch'], mn, mx, x_cursor, draw_scale)
                                stem_length = (5*interpolation(f_notey,l_notey,yy)*draw_scale)
                                pview.create_line(x-(25*draw_scale),yy,
                                                    lw_notex-(25*draw_scale)-stem_length,yy,
                                                    tag='beam',
                                                    width=3*draw_scale,
                                                    capstyle='round',
                                                    fill=color_black)

                    # end for obj ----------------------------------------

                # making choices for drawing the staff
                if not idx_l and minipiano: mp = True
                else: mp = False
                if not idx_p: hh = header_h
                else: hh = 0
                draw_staff_vert(x_cursor,
                    mn,
                    mx,
                    p_marg_u,
                    p_marg_d,
                    p_marg_l,
                    p_marg_r,
                    page_height,
                    page_width,
                    hh,
                    footer_h,
                    draw_scale,
                    color_black,
                    pview,
                    sw,
                    mp)

                # update x_cursor and divide the systems equal:
                x_cursor += sw + lmd + (page_spacing[idx_p] / (len(DOC[idx_p])) / 2)

                idx_l += 1

                # end for line ---------------------------------------

            x_cursor = page_width * (idx_p + 1)


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
        pview.tag_raise('countline')
        pview.tag_raise('staff')
        pview.tag_raise('grid')
        pview.tag_raise('white_space')
        pview.tag_raise('notestop')
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
        #pview.tag_lower('midi_note')
        
        # make the new render update fluently(without blinking) and scale
        if not render_type == 'export':   
            root.update()
            s = pview.winfo_width() / page_width
            pview.scale("all", 0, 0, s, s)
        pview.move('all', 0, 10000)
        pview.delete('old')
        if not render_type == 'export':
            pview.configure(scrollregion=pview.bbox("all"))
        pview.addtag_all('old')

    draw()

    return len(DOC)

