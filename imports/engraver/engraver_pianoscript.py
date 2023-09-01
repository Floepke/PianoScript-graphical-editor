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


from imports.tools import *
from imports.colors import color_dark, color_light
from imports.constants import BLACK







def engrave_pianoscript_vertical(io):
    '''
        auto_scaling == the drawing gets scaled to the width of the printview.
        renderer == 'pianoscript' or 'klavarskribo'.
    '''

    def draw_staff(x_cursor,
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
        global_scale,
        color_black,
        io,
        st_width,
        staff_scale,
        line_scale,
        minipiano=True):

        print_height = page_height - p_marg_u - p_marg_d

        def two(x):
            if minipiano:
                y2 = page_height - p_marg_d - footer_h - (40 * global_scale)
                io['pview'].create_line(
                    x,
                    y2,
                    x,
                    page_height - p_marg_d - footer_h - (20 * global_scale),
                    fill=color_black,
                    width=5*global_scale*staff_scale,
                    capstyle='round')
                io['pview'].create_line(
                    x+(10*global_scale*staff_scale),
                    y2,
                    x+(10*global_scale*staff_scale),
                    page_height - p_marg_d - footer_h - (20 * global_scale),
                    fill=color_black,
                    width=5*global_scale*staff_scale,
                    capstyle='round')
            else:
                y2 = page_height - p_marg_d - footer_h
            io['pview'].create_line(
                x,
                p_marg_u + header_h,
                x,
                y2,
                fill=color_black,
                width=1*global_scale*staff_scale,
                capstyle='round')
            io['pview'].create_line(
                x+(10*global_scale*staff_scale),
                p_marg_u + header_h,
                x+(10*global_scale*staff_scale),
                y2,
                fill=color_black,
                width=1*global_scale*staff_scale,
                capstyle='round')

        def three(x):
            if minipiano:
                y2 = page_height - p_marg_d - footer_h - (40 * global_scale)
                io['pview'].create_line(
                    x,
                    y2,
                    x,
                    page_height - p_marg_d - footer_h - (20 * global_scale),
                    fill=color_black,
                    width=5*global_scale*staff_scale,
                    capstyle='round')
                io['pview'].create_line(
                    x+(10*global_scale*staff_scale),
                    y2,
                    x+(10*global_scale*staff_scale),
                    page_height - p_marg_d - footer_h - (20 * global_scale),
                    fill=color_black,
                    width=5*global_scale*staff_scale,
                    capstyle='round')
                io['pview'].create_line(
                    x+(20*global_scale*staff_scale),
                    y2,
                    x+(20*global_scale*staff_scale),
                    page_height - p_marg_d - footer_h - (20 * global_scale),
                    fill=color_black,
                    width=5*global_scale*staff_scale,
                    capstyle='round')
            else:
                y2 = page_height - p_marg_d - footer_h
            io['pview'].create_line(
                x,
                p_marg_u + header_h,
                x,
                y2,
                fill=color_black,
                width=1.5*global_scale*staff_scale*line_scale,
                capstyle='round')
            io['pview'].create_line(
                x+(10*global_scale*staff_scale),
                p_marg_u + header_h,
                x+(10*global_scale*staff_scale),
                y2,
                fill=color_black,
                width=1.5*global_scale*staff_scale*line_scale,
                capstyle='round')
            io['pview'].create_line(
                x+(20*global_scale*staff_scale),
                p_marg_u + header_h,
                x+(20*global_scale*staff_scale),
                y2,
                fill=color_black,
                width=1.5*global_scale*staff_scale*line_scale,
                capstyle='round')

        def clef(x):
            if minipiano:
                y2 = page_height - p_marg_d - footer_h - (40 * global_scale)
                io['pview'].create_line(
                    x,
                    y2,
                    x,
                    page_height - p_marg_d - footer_h - (20 * global_scale),
                    fill=color_black,
                    width=5*global_scale*staff_scale,
                    capstyle='round')
                io['pview'].create_line(
                    x+(10*global_scale*staff_scale),
                    y2,
                    x+(10*global_scale*staff_scale),
                    page_height - p_marg_d - footer_h - (20 * global_scale),
                    fill=color_black,
                    width=5*global_scale*staff_scale,
                    capstyle='round')
            else:
                y2 = page_height - p_marg_d - footer_h
            io['pview'].create_line(
                x,
                p_marg_u + header_h,
                x,
                y2,
                fill=color_black,
                width=1*global_scale*staff_scale,
                capstyle='round',
                dash=(6,6))
            io['pview'].create_line(
                x+(10*global_scale*staff_scale),
                p_marg_u + header_h,
                x+(10*global_scale*staff_scale),
                y2,
                fill=color_black,
                width=1*global_scale*staff_scale,
                capstyle='round',
                dash=(6,6))

        # control flow for engraving the right composition of staff-lines
        clefline = 0
        if mn <= 3:
            if not minipiano:
                io['pview'].create_line(x_cursor,
                    p_marg_u + header_h,
                    x_cursor,
                    page_height - p_marg_d - footer_h,
                    width=2*global_scale*staff_scale,
                    fill=color_black,
                    capstyle='round')
            else:
                io['pview'].create_line(x_cursor,
                    p_marg_u + header_h,
                    x_cursor,
                    page_height - p_marg_d - footer_h - (40 * global_scale),
                    width=2*global_scale,
                    fill=color_black,
                    capstyle='round')
                io['pview'].create_line(x_cursor,
                    page_height - p_marg_d - footer_h - (20 * global_scale),
                    x_cursor,
                    page_height - p_marg_d - footer_h - (40 * global_scale),
                    width=5*global_scale,
                    fill=color_black,
                    capstyle='round')
            two(x_cursor + (20*global_scale*staff_scale))
            three(x_cursor + (50*global_scale*staff_scale))
            two(x_cursor + (90*global_scale*staff_scale))
            three(x_cursor + (120*global_scale*staff_scale))
            two(x_cursor + (160*global_scale*staff_scale))
            three(x_cursor + (190*global_scale*staff_scale))
            clefline = 230 * global_scale*staff_scale
        if mn >= 4 and mn <= 8:
            two(x_cursor)
            three(x_cursor + (30*global_scale*staff_scale))
            two(x_cursor + (70*global_scale*staff_scale))
            three(x_cursor + (100*global_scale*staff_scale))
            two(x_cursor + (140*global_scale*staff_scale))
            three(x_cursor + (170*global_scale*staff_scale))
            clefline = 210 * global_scale*staff_scale
        if mn >= 9 and mn <= 15:
            three(x_cursor)
            two(x_cursor + (40*global_scale*staff_scale))
            three(x_cursor + (70*global_scale*staff_scale))
            two(x_cursor + (110*global_scale*staff_scale))
            three(x_cursor + (140*global_scale*staff_scale))
            clefline = 180 * global_scale*staff_scale
        if mn >= 16 and mn <= 20:
            two(x_cursor)
            three(x_cursor + (30*global_scale*staff_scale))
            two(x_cursor + (70*global_scale*staff_scale))
            three(x_cursor + (100*global_scale*staff_scale))
            clefline = 140 * global_scale*staff_scale
        if mn >= 21 and mn <= 27:
            three(x_cursor)
            two(x_cursor + (40*global_scale*staff_scale))
            three(x_cursor + (70*global_scale*staff_scale))
            clefline = 110 * global_scale*staff_scale
        if mn >= 28 and mn <= 32:
            two(x_cursor)
            three(x_cursor + (30*global_scale*staff_scale))
            clefline = 70 * global_scale*staff_scale
        if mn >= 33 and mn <= 39:
            three(x_cursor)
            clefline = 40 * global_scale*staff_scale
        clef(x_cursor + (clefline))
        if mx >= 45 and mx <= 51:
            three(x_cursor + clefline + (30*global_scale*staff_scale))
        if mx >= 52 and mx <= 56:
            three(x_cursor + clefline + (30*global_scale*staff_scale))
            two(x_cursor + clefline + (70*global_scale*staff_scale))
        if mx >= 57 and mx <= 63:
            three(x_cursor + clefline + (30*global_scale*staff_scale))
            two(x_cursor + clefline + (70*global_scale*staff_scale))
            three(x_cursor + clefline + (100*global_scale*staff_scale))
        if mx >= 64 and mx <= 68:
            three(x_cursor + clefline + (30*global_scale*staff_scale))
            two(x_cursor + clefline + (70*global_scale*staff_scale))
            three(x_cursor + clefline + (100*global_scale*staff_scale))
            two(x_cursor + clefline + (140*global_scale*staff_scale))
        if mx >= 69 and mx <= 75:
            three(x_cursor + clefline + (30*global_scale*staff_scale))
            two(x_cursor + clefline + (70*global_scale*staff_scale))
            three(x_cursor + clefline + (100*global_scale*staff_scale))
            two(x_cursor + clefline + (140*global_scale*staff_scale))
            three(x_cursor + clefline + (170*global_scale*staff_scale))
        if mx >= 76 and mx <= 80:
            three(x_cursor + clefline + (30*global_scale*staff_scale))
            two(x_cursor + clefline + (70*global_scale*staff_scale))
            three(x_cursor + clefline + (100*global_scale*staff_scale))
            two(x_cursor + clefline + (140*global_scale*staff_scale))
            three(x_cursor + clefline + (170*global_scale*staff_scale))
            two(x_cursor + clefline + (210*global_scale*staff_scale))
        if mx >= 81:
            three(x_cursor + clefline + (30*global_scale*staff_scale))
            two(x_cursor + clefline + (70*global_scale*staff_scale))
            three(x_cursor + clefline + (100*global_scale*staff_scale))
            two(x_cursor + clefline + (140*global_scale*staff_scale))
            three(x_cursor + clefline + (170*global_scale*staff_scale))
            two(x_cursor + clefline + (210*global_scale*staff_scale))
            three(x_cursor + clefline + (240*global_scale*staff_scale))

        # draw minipiano border
        if minipiano:
            io['pview'].create_line(x_cursor+st_width,
                page_height - p_marg_d - footer_h - (40*global_scale),
                x_cursor+st_width+(20*global_scale),
                page_height - p_marg_d - footer_h - (40*global_scale),
                fill=color_black,
                width=1*global_scale*staff_scale)
            io['pview'].create_line(x_cursor,
                page_height - p_marg_d - footer_h - (40*global_scale),
                x_cursor-(20*global_scale),
                page_height - p_marg_d - footer_h - (40*global_scale),
                fill=color_black,
                width=1*global_scale*staff_scale)
            io['pview'].create_line(x_cursor-(20*global_scale),
                page_height - p_marg_d - footer_h - (40*global_scale),
                x_cursor-(20*global_scale),
                page_height - p_marg_d - footer_h,
                fill=color_black,
                width=1*global_scale*staff_scale)
            io['pview'].create_line(x_cursor+st_width+(20*global_scale),
                page_height - p_marg_d - footer_h - (40*global_scale),
                x_cursor+st_width+(20*global_scale),
                page_height - p_marg_d - footer_h,
                fill=color_black,
                width=1*global_scale*staff_scale)
            io['pview'].create_line(x_cursor-(20*global_scale),
                page_height - p_marg_d - footer_h,
                x_cursor+st_width+(20*global_scale),
                page_height - p_marg_d - footer_h,
                fill=color_black,
                width=1*global_scale*staff_scale)

    

    # check if there is a time_signature in the io['score']
    if not io['score']['events']['grid']:
        print('ERROR: There is no time signature in the io["score"]!')
        return

    MM = io['mm']
    pageno = io['pageno']
    render_type = io['render_type']
    last_pianotick = io['last_pianotick']

    if render_type == 'export':
        pageno = 0

    # place all data in variables from io['score'] for cleaner code
    page_width = io['score']['properties']['page-width'] * MM
    page_height = io['score']['properties']['page-height'] * MM
    p_marg_l = io['score']['properties']['page-margin-left'] * MM
    p_marg_r = io['score']['properties']['page-margin-right'] * MM
    p_marg_u = io['score']['properties']['page-margin-up'] * MM
    p_marg_d = io['score']['properties']['page-margin-down'] * MM
    header_h = io['score']['properties']['header-height'] * MM
    footer_h = io['score']['properties']['footer-height'] * MM
    global_scale = io['score']['properties']['draw-scale']
    line_break = io['score']['events']['linebreak']
    count_line = io['score']['events']['countline']
    staff_sizer = io['score']['events']['staffsizer']
    start_repeat = io['score']['events']['startrepeat']
    end_repeat = io['score']['events']['endrepeat']
    beam = io['score']['events']['beam']
    color_right_midinote = io['score']['properties']['color-right-hand-midinote']
    color_left_midinote = io['score']['properties']['color-left-hand-midinote']
    grid = io['score']['events']['grid']
    note = io['score']['events']['note']
    text = io['score']['events']['text']
    bpm = io['score']['events']['bpm']
    slur = io['score']['events']['slur']
    pedal = io['score']['events']['pedal']
    title = io['score']['header']['title']
    composer = io['score']['header']['composer']
    copyright = io['score']['header']['copyright']

    # elements on/off
    minipiano = io['score']['properties']['minipiano']
    staffonoff = io['score']['properties']['staffonoff']
    stemonoff = io['score']['properties']['stemonoff']
    beamonoff = io['score']['properties']['beamonoff']
    noteonoff = io['score']['properties']['noteonoff']
    midinoteonoff = io['score']['properties']['midinoteonoff']
    notestoponoff = io['score']['properties']['notestoponoff']
    pagenumberingonoff = io['score']['properties']['pagenumberingonoff']
    barlinesonoff = io['score']['properties']['barlinesonoff']
    basegridonoff = io['score']['properties']['basegridonoff']
    countlineonoff = io['score']['properties']['countlineonoff']
    measurenumberingonoff = io['score']['properties']['measurenumberingonoff']
    accidentalonoff = io['score']['properties']['accidentalonoff']
    continuationdotonoff = io['score']['properties']['soundingdotonoff']
    three_line_scale = io['score']['properties']['threelinescale']
    leftdotonoff = io['score']['properties']['leftdotonoff']

    # staffs
    staff1properties = io['score']['properties']['staff'][0]
    staff2properties = io['score']['properties']['staff'][1]
    staff3properties = io['score']['properties']['staff'][2]
    staff4properties = io['score']['properties']['staff'][3]

    def read():
        '''
            read the music from io['score'] an place in the DOC list.
            DOC is an structured list with all events in it.
            structure: [pages[line[events]lines]pages]
            In the draw function we can easily loop over it
            to engrave the document.
        '''
        # data to collect:
        DOC = []
        page_spacing = []
        staff_widths = []
        t_sig_map = []

        # time_signature
        bln_time = 0
        grd_time = 0
        for idx,g in enumerate(io['score']['events']['grid']):
            t_sig_map.append(g)
            # barline and grid messages
            meas_len = measure_length(g['numerator'], g['denominator'])
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
        DOC.append({'type': 'endbarline', 'time': last_pianotick-0.0000001})

        # we add all events from io['score'] to the DOC list
        for e in note:
            e['type'] = 'note'
            e = note_split_processor(e, io['score'])
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
            e['type'] = 'staffsizer'
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

        # we first need to get the split times from io['score']
        bl_times = barline_times(io['score']['events']['grid'])

        split_times = [0]
        for spl in io['score']['events']['linebreak']:
            if spl['time'] > 0 and not spl['time'] > last_pianotick:
                split_times.append(spl['time'])
        split_times.append(last_pianotick)

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

        DOC.pop(-1)

        # now we have to calculate the amount of lines
        # that will fit on every page. We need to know
        # the height of the staffs, and from linebreak objects
        # the margin around every staff.

        # we make a list that contains all staff widths inside 'staff_widths' in the following structure:
        # [[widthstaff1,widthstaff2,widthstaff3,widthstaff4],[...]]
        # every object in the staff_widths contains 4 values. If the value is zero the staff is switched off.
        for line in DOC:
            sw = []
            for staff in [staff1properties, staff2properties, staff3properties, staff4properties]:
                pitches = []
                for ev in line:
                    if ev['type'] == 'staffsizer':
                        if ev['staff'] == staff['staff-number']:
                            pitches.append(ev['pitch1'])
                            pitches.append(ev['pitch2'])
                            break
                    if ev['type'] in ['note', 'split']:
                        if ev['staff'] == staff['staff-number']:
                            pitches.append(ev['pitch'])
                if staff['onoff']:
                    try:
                        sw.append(staff_height_width(min(pitches),max(pitches),global_scale)*staff['staff-scale'])
                    except ValueError:
                        sw.append(10*staff['staff-scale']*global_scale)
                else:
                    sw.append(0)
            staff_widths.append(sw)

        # in this part we calculate how many systems fit on each page
        # also we gather the free space in the printarea in a list
        # called 'page_spacing'.
        doc = DOC
        DOC = []
        x_cursor = 0
        printarea_width = (page_width - p_marg_l - p_marg_r)
        remaining_space = 0
        page = []
        total_system_width = []
        for c, line, lbreak, staffw in zip(range(len(doc)),doc,line_break,staff_widths):
            # organize margins data; if zero there is no staff
            if staff1properties['onoff']: ml1 = lbreak['margin-staff1-left'] * MM
            else: ml1 = 0
            if staff1properties['onoff']: mr1 = lbreak['margin-staff1-right'] * MM
            else: mr1 = 0
            if staff2properties['onoff']: ml2 = lbreak['margin-staff2-left'] * MM
            else: ml2 = 0
            if staff2properties['onoff']: mr2 = lbreak['margin-staff2-right'] * MM
            else: mr2 = 0
            if staff3properties['onoff']: ml3 = lbreak['margin-staff3-left'] * MM
            else: ml3 = 0
            if staff3properties['onoff']: mr3 = lbreak['margin-staff3-right'] * MM
            else: mr3 = 0
            if staff4properties['onoff']: ml4 = lbreak['margin-staff4-left'] * MM
            else: ml4 = 0
            if staff4properties['onoff']: mr4 = lbreak['margin-staff4-right'] * MM
            else: mr4 = 0

            # this is the width of the system including all staffs:
            total_sys_width = ml1 + mr1 + ml2 + mr2 + ml3 + mr3 + ml4 + mr4 + staffw[0] + staffw[1] + staffw[2] + staffw[3]
            total_system_width.append(total_sys_width)

            x_cursor += total_sys_width

            # if the line fits on paper:
            if x_cursor <= printarea_width:
                page.append(line)
                remaining_space = printarea_width - x_cursor
            # if the line does NOT fit on paper:
            else:
                x_cursor = total_sys_width
                DOC.append(page)
                page = []
                page.append(line)
                page_spacing.append(remaining_space)
                remaining_space = printarea_width - x_cursor
            # if this is the last line:
            if c == len(doc)-1:
                DOC.append(page)
                page_spacing.append(remaining_space)

        return DOC, page_spacing, staff_widths, split_times, bl_times, total_system_width

    DOC, page_spacing, staff_widths, split_times, bl_times, total_system_width = read()

    #------------------
    # debugging prints
    # print('page_spacing: ', page_spacing, '\nstaff_widths: ', staff_widths)

    # idxl = 0
    # print('new render...')
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
            return p_marg_u + hh + ((page_height - p_marg_u - p_marg_d - footer_h - (40 * global_scale) - hh) * factor)

    def note_x_pos(note, mn, mx, x_cursor, scale, staffscale):
        '''
        returns the position of the given note relative to 'x_cursor'(the xx axis staff cursor).
        '''
        xlist = [-5,0,5,15,20,25,30,35,45,50,55,60,65,70,75,
        85,90,95,100,105,115,120,125,130,135,140,145,
        155,160,165,170,175,185,190,195,200,205,210,215,
        225,230,235,240,245,255,260,265,270,275,280,285,
        295,300,305,310,315,325,330,335,340,345,350,355,
        365,370,375,380,385,395,400,405,410,415,420,425,
        435,440,445,450,455,465,470,475,480,485,490,495,
        505]
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
        return x_cursor + (xlist[int(note) - 1] * scale * staffscale) - (sub * scale * staffscale)

    def draw():
        '''
            I try to draw everything as efficient as possible from
            the ordered DOC list using many nested if/else flow.
            I found it the best way to draw.

            things we need to know/keep track on:
                - x_cursor
                - page_spacings
                - staff widths
        '''
        # set colors
        if render_type == 'export':
            color_black = 'black'
            color_white = 'white'
        else:
            color_black = color_dark
            color_white = color_light

        x_cursor = 0
        idx_l = 0
        len_doc = len(DOC)
        b_counter = update_bcounter(DOC,pageno % len_doc)
        draw_barline_and_numbering = True

        #find out where a continuation dot and/or an end-of-note symbol has to be placed
        if io['score']['properties']['stop-sign-style'] == 'Klavarskribo':
            timelist=[]
            handlist=[]
            stafflist=[]
            epsilon=0.01
            #store for every not the staff, the hand and the (start)time:
            for page in DOC:
                for line in page:
                    for obj in line:
                        if obj['type'] == 'note':
                            stafflist.append(obj['staff'])
                            timelist.append(obj['time'])
                            handlist.append(obj['hand'])

            #number of notes:
            nn=len(timelist)
            n=0
            for page in DOC:
                for line in page:
                    for obj in line:
                        if obj['type'] == 'note':
                            endtime=obj['time']+obj['duration']
                            #continuation_dot:
                            #loop over all later notes; if the staff and hand are similar to the current note, but
                            # the endtime of the current note is larger than the starttime of the later note: add a continuation dot
                            obj['continuation_dot']=""
                            for i in range(n,nn):
                                if stafflist[i] == obj['staff'] and handlist[i] == obj['hand'] and endtime > float(timelist[i]) and obj['time'] < float(timelist[i]):
                                    obj['continuation_dot']=f"{obj['continuation_dot']} {timelist[i]}"

                            #end-of-note:
                            #start with 'True', set to False if a new note starts on the same moment as the old one ends (within a difference of epsilon):
                            #(conditional on the same staff and the same hand)
                            obj['end-of-note']=True
                            for i in range(n,nn):
                                if stafflist[i] == obj['staff'] and handlist[i] == obj['hand']:
                                    if abs(endtime - float(timelist[i])) < epsilon:
                                        obj['end-of-note']=False
                                        break
                            n+=1

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
            if render_type == 'normal':
                io['pview'].create_line(0,
                    x_cursor,
                    page_width,
                    x_cursor,
                    fill='black',
                    width=2,
                    dash=(6,4,5,2,3))

            # draw footer (page numbering, title and copyright notice
            if pagenumberingonoff: io['pview'].create_text(x_cursor + p_marg_l,
                                    page_height - p_marg_d,
                                    text='page ' + str(idx_p+1) + ' of ' + str(len_doc) + ' | ' + title['text'] + ' | ' + copyright['text'],
                                    anchor='sw',
                                    fill=color_black,
                                    font=('courier', 12, "normal"))

            if not idx_p: # if on the first page
                # draw header (title & composer text)
                io['pview'].create_text(x_cursor + p_marg_l,
                    p_marg_u,
                    text=io['score']['header']['title']['text'],
                    anchor='nw',
                    font=('courier', 18, "bold"),
                    fill=color_black)
                io['pview'].create_text(x_cursor + page_width - p_marg_r,
                    p_marg_u,
                    text=io['score']['header']['composer']['text'],
                    anchor='ne',
                    font=('courier', 12, "normal"),
                    fill=color_black)

            x_cursor += p_marg_l

            for idx_ll, line in enumerate(page):

                x_cursor += (page_spacing[idx_p] / (len(DOC[idx_p]) + 1))

                # calculate for every enabled staff the highest and lowest note for drawing the needed stafflines
                for idx_st, sw in enumerate(staff_widths[idx_l]):

                    # True on the first enabled staff:
                    if idx_st == get_first_available_staff(io['score']): draw_barline_and_numbering = True
                    else: draw_barline_and_numbering = False

                    # staff scale from current staff
                    staff_scale = io['score']['properties']['staff'][idx_st]['staff-scale']

                    # check if staff is active; otherwise continue
                    if not io['score']['properties']['staff'][idx_st]['onoff']:
                        continue

                    # read staff margins in linebreak properties
                    st_marg = [
                        (line_break[idx_ll]['margin-staff1-left'],line_break[idx_ll]['margin-staff1-right']),
                        (line_break[idx_ll]['margin-staff2-left'],line_break[idx_ll]['margin-staff2-right']),
                        (line_break[idx_ll]['margin-staff3-left'],line_break[idx_ll]['margin-staff3-right']),
                        (line_break[idx_ll]['margin-staff4-left'],line_break[idx_ll]['margin-staff4-right'])
                    ]
                    st_marg_l = st_marg[idx_st][0] * MM
                    st_marg_r = st_marg[idx_st][1] * MM

                    x_cursor += st_marg_l

                    # getting lowest and highest note in line from the current staff
                    mn, mx = 42, 42
                    if not sw:
                        mn, mx = 0, 0
                        continue
                    for obj in line:
                        if obj['type'] in ['note', 'split']:
                            if obj['staff'] == idx_st:
                                if mn >= obj['pitch']:
                                    mn = obj['pitch']
                                if mx <= obj['pitch']:
                                    mx = obj['pitch']

                    # overwriting mn mx in case of a staff sizer
                    for obj in line:
                        if obj['type'] == 'staffsizer':
                            if obj['staff'] == idx_st:
                                if obj['pitch1'] >= obj['pitch2']:
                                    mn = obj['pitch2']
                                    mx = obj['pitch1']
                                else:
                                    mn = obj['pitch1']
                                    mx = obj['pitch2']

                    # making choices for drawing the staff
                    if not idx_l and minipiano: mp = True
                    else: mp = False
                    if not idx_p: hh = header_h
                    else: hh = 0
                    if staffonoff:
                        draw_staff(x_cursor,
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
                            global_scale,
                            color_black,
                            io,
                            sw,
                            staff_scale,
                            three_line_scale,
                            mp)

                    sys_width = 0
                    if idx_st == get_first_available_staff(io['score']):
                        # calculate the width of the whole system for drawing the correct bar lines:

                        def get_system_width(st_marg,staff_width, scale, staffscale, mm):

                            out = 0
                            struct = []
                            for idx, marg, sw in zip(range(len(st_marg)),st_marg,staff_width):
                                if sw:
                                    new = {
                                        'leftmargin':marg[0]*mm,
                                        'sw':sw,
                                        'rightmargin':marg[1]*mm
                                    }
                                    struct.append(new)
                                else:
                                    ...
                            for idx, sys in enumerate(struct):
                                if not idx:
                                    out += sys['sw']
                                    if idx + 1 == len(struct):
                                        out += sys['rightmargin']
                                        return out
                                    else:
                                        out += sys['rightmargin']
                                if idx >= 1 and idx < len(struct):
                                    out +=  sys['leftmargin'] + sys['sw'] + sys['rightmargin']
                                if idx == len(struct):
                                    out += sys['leftmargin'] + sys['sw'] + sys['rightmargin']

                            return out

                        sys_width = get_system_width(st_marg,staff_widths[idx_l], global_scale, staff_scale, MM)

                    for idx_o, obj in enumerate(line):

                        if idx_st == get_first_available_staff(io['score']):

                            # barline and numbering
                            if obj['type'] == 'barline' and draw_barline_and_numbering:
                                if not idx_l and not idx_p:
                                    yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                                elif not idx_p:
                                    yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                                else:
                                    yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                                if barlinesonoff:
                                    io['pview'].create_line(x_cursor,
                                                  yy,
                                                  x_cursor+sys_width, #+ (35 * global_scale * staff_scale),
                                                  yy,
                                                  width=.75 * global_scale,
                                                  capstyle='round',
                                                  tag='grid',
                                                  fill=color_black)
                                if measurenumberingonoff and draw_barline_and_numbering:
                                    io['pview'].create_text(x_cursor+sys_width+(10*global_scale * staff_scale),
                                                  yy+(3*global_scale),
                                                  text=b_counter,
                                                  tag='grid',
                                                  fill=color_black,
                                                  font=('courier', round(14 * global_scale * staff_scale), "normal"),
                                                  anchor='nw')
                                b_counter += 1

                            # draw barline at end of the system/line:
                            if obj['type'] == 'endoflinebarline':
                                if not idx_l and not idx_p:
                                    yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                                elif not idx_p:
                                    yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                                else:
                                    yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                                if barlinesonoff:
                                    io['pview'].create_line(x_cursor,
                                                  yy,
                                                  x_cursor+sys_width,
                                                  yy,
                                                  width=.75 * global_scale*staff_scale,
                                                  capstyle='round',
                                                  tag='grid',
                                                  fill=color_black)

                            # draw the last barline that's more thick
                            if obj['type'] == 'endbarline':
                                if not idx_l and not idx_p:
                                    yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                                elif not idx_p:
                                    yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                                else:
                                    yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                                if barlinesonoff: io['pview'].create_line(x_cursor,
                                                  yy,
                                                  x_cursor+sys_width,
                                                  yy,
                                                  width=4 * global_scale*staff_scale,
                                                  capstyle='round',
                                                  tag='grid',
                                                  fill=color_black)

                        # grid
                        if obj['type'] == 'gridline':
                            if not idx_l and not idx_p:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                            elif not idx_p:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                            else:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                            if basegridonoff: io['pview'].create_line(x_cursor,
                                              yy,
                                              x_cursor+sw,
                                              yy,
                                              width=1 * global_scale*staff_scale,
                                              capstyle='round',
                                              tag='grid',
                                              fill=color_black,
                                              dash=(6, 6))

                        # draw notes left and right; TODO:
                        #       * based on black-note-style property draw black notes above or under the stem.
                        #       * based on continuationdotonoff property draw soundingdot
                        if obj['type'] in ['note', 'split'] and obj['staff'] == idx_st:
                            if not idx_l and not idx_p:
                                y0 = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                                y1 = event_y_pos_engrave(obj['time'] + obj['duration'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                            elif not idx_p:
                                y0 = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                                y1 = event_y_pos_engrave(obj['time'] + obj['duration'], split_times[idx_l], split_times[idx_l + 1],True,False)
                            else:
                                y0 = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                                y1 = event_y_pos_engrave(obj['time'] + obj['duration'], split_times[idx_l],split_times[idx_l + 1],False,False)
                            xx = note_x_pos(obj['pitch'], mn, mx, x_cursor, global_scale,staff_scale)
                            x0 = xx - (5 * global_scale*staff_scale)
                            x1 = xx + (5 * global_scale*staff_scale)

                            # helpline; if the note is outside range we draw a help staff line:
                            if 1: #????????????
                                ...

                            # notestop
                            if obj['notestop']:
                                if notestoponoff:
                                    if io['score']['properties']['stop-sign-style'] == 'PianoScript':
                                        io['pview'].create_line(x0,
                                                  y1,
                                                  x1,
                                                  y1,
                                                  width=1.5 * global_scale*staff_scale,
                                                  fill=color_black,
                                                  tag=('midi_note','notestop'))
                                    elif io['score']['properties']['stop-sign-style'] == 'Klavarskribo':
                                        # end-of-note symbol:
                                        try:
                                            if obj['end-of-note']:
                                                io['pview'].create_line(x0,y1 - (10 * global_scale * staff_scale),
                                                      xx,y1,
                                                      x1,y1 - (10 * global_scale * staff_scale),
                                                      width=2 * global_scale*staff_scale,
                                                      fill=color_black,
                                                      tag=('end-of-note'))
                                        except:
                                            ...
                                        # continuation dot:
                                        if continuationdotonoff:
                                          try:
                                              times=obj['continuation_dot'].split()
                                          except:
                                              times="".split()
                                          if len(times) > 0:
                                              for time in times:
                                                  if not idx_l and not idx_p:
                                                      y2 = event_y_pos_engrave(float(time), split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                                                  elif not idx_p:
                                                      y2 = event_y_pos_engrave(float(time), split_times[idx_l], split_times[idx_l + 1],True,False)
                                                  else:
                                                      y2 = event_y_pos_engrave(float(time), split_times[idx_l],split_times[idx_l + 1],False,False)
                                                  io['pview'].create_oval(xx-(2*global_scale*staff_scale),
                                                              y2 + (3 * global_scale*staff_scale),
                                                              xx+(2*global_scale*staff_scale),
                                                              y2 + (7 * global_scale*staff_scale),
                                                              tag='continuation_dot',
                                                              fill=color_black,
                                                              outline=color_black,
                                                              width=2 * global_scale*staff_scale)

                            # accidental
                            if obj['accidental'] == 1:
                                if accidentalonoff: io['pview'].create_line(xx,y0+(10*global_scale*staff_scale), x0,y0+(15*global_scale*staff_scale),
                                width=2*global_scale*staff_scale,
                                tag='accidental',
                                fill=color_black,
                                capstyle='round')
                            if obj['accidental'] == -1:
                                if accidentalonoff: io['pview'].create_line(xx,y0+(10*global_scale*staff_scale), x1,y0+(15*global_scale*staff_scale),
                                width=2*global_scale*staff_scale,
                                tag='accidental',
                                fill=color_black,
                                capstyle='round')

                            # left hand
                            if obj['hand'] == 'l':
                                # midinote
                                if midinoteonoff: io['pview'].create_rectangle(
                                    x0,y0,
                                    x1,y1,
                                    fill=io['score']['properties']['color-left-hand-midinote'],
                                    tag='midi_note',
                                    outline='')

                                if obj['type'] == 'split':
                                    if midinoteonoff: io['pview'].create_oval(xx+(2.5*global_scale*staff_scale),y0+(2.5*global_scale*staff_scale),
                                        xx-(2.5*global_scale*staff_scale),y0+(7.5*global_scale*staff_scale),
                                        fill=color_black,
                                        outline='')

                                if obj['type'] == 'note':
                                    if stemonoff:
                                        # left stem and white space if on barline
                                        io['pview'].create_line(xx,
                                                          y0,
                                                          xx - (25 * global_scale*staff_scale),
                                                          y0,
                                                          width=3 * global_scale*staff_scale,
                                                          tag='stem',
                                                          fill=color_black,
                                                          capstyle='round')
                                        # for bl in bl_times:
                                        #     if diff(obj['time'], bl) < 1:
                                        #         io['pview'].create_line(xx + (10 * global_scale),
                                        #                           y0,
                                        #                           xx - (30 * global_scale),
                                        #                           y0,
                                        #                           width=2 * global_scale,
                                        #                           tag='white_space',
                                        #                           fill=color_white)

                                    # note head
                                    if obj['pitch'] in BLACK:

                                        if noteonoff and io['score']['properties']['black-note-style'] == 'PianoScript' or io['score']['properties']['black-note-style'] == 'PianoScript' and noteonoff and not obj['stem-visible']:
                                            io['pview'].create_oval(xx-(2.5*global_scale*staff_scale),
                                                          y0,
                                                          xx+(2.5*global_scale*staff_scale),
                                                          y0 + (10 * global_scale*staff_scale),
                                                          tag='black_notestart',
                                                          fill=color_black,
                                                          outline=color_black,
                                                          width=2 * global_scale*staff_scale)
                                            # left dot black
                                            if leftdotonoff: io['pview'].create_oval(xx - (1*global_scale*staff_scale),
                                                          y0 + (4 * global_scale*staff_scale),
                                                          xx + (1*global_scale*staff_scale),
                                                          y0 + (6 * global_scale*staff_scale),
                                                          tag='left_dot',
                                                          fill=color_white,
                                                          outline='')
                                        if noteonoff and io['score']['properties']['black-note-style'] == 'Klavarskribo':
                                            io['pview'].create_oval(xx-(5*global_scale*staff_scale),
                                                          y0,
                                                          xx+(5*global_scale*staff_scale),
                                                          y0 - (10 * global_scale*staff_scale),
                                                          tag='black_notestart',
                                                          fill=color_black,
                                                          outline=color_black,
                                                          width=2 * global_scale*staff_scale)
                                            # left dot black
                                            if leftdotonoff: io['pview'].create_oval(xx + (1*global_scale*staff_scale),
                                                          y0 - (4 * global_scale*staff_scale),
                                                          xx - (1*global_scale*staff_scale),
                                                          y0 - (6 * global_scale*staff_scale),
                                                          tag='left_dot',
                                                          fill=color_white,
                                                          outline='')
                                    else:
                                        if noteonoff: io['pview'].create_oval(x0,
                                                          y0,
                                                          x1,
                                                          y0 + (10 * global_scale*staff_scale),
                                                          tag='white_notestart',
                                                          fill=color_white,
                                                          outline=color_black,
                                                          width=2 * global_scale*staff_scale)
                                        # left dot white
                                        if noteonoff and leftdotonoff: io['pview'].create_oval(xx + (1*global_scale*staff_scale),
                                                          y0 + (((10 / 2) - 1) * global_scale*staff_scale),
                                                          xx - (1*global_scale),
                                                          y0 + (((10 / 2) + 1) * global_scale*staff_scale),
                                                          tag='left_dot',
                                                          fill=color_black,
                                                          outline='')

                            # right hand
                            else:
                                # midinote
                                if midinoteonoff: io['pview'].create_rectangle(x0,y0,x1,y1,
                                    fill=io['score']['properties']['color-right-hand-midinote'],
                                    tag='midi_note',
                                    outline='')

                                if obj['type'] == 'split':
                                    if midinoteonoff: io['pview'].create_oval(xx+(2.5*global_scale),y0+(2.5*global_scale),
                                        xx-(2.5*global_scale),y0+(7.5*global_scale),
                                        fill=color_black,
                                        outline='')

                                if obj['type'] == 'note':
                                    if stemonoff:
                                        # right stem and white space if on barline
                                        io['pview'].create_line(xx,
                                                          y0,
                                                          xx + (25 * global_scale*staff_scale),
                                                          y0,
                                                          width=3 * global_scale*staff_scale,
                                                          tag='stem',
                                                          fill=color_black,
                                                          capstyle='round')
                                        # for bl in bl_times:
                                        #     if diff(obj['time'], bl) < 1:
                                        #         io['pview'].create_line(xx - (10 * global_scale),
                                        #                           y0,
                                        #                           xx + (30 * global_scale),
                                        #                           y0,
                                        #                           width=2 * global_scale,
                                        #                           tag='white_space',
                                        #                           fill=color_white)
                                    # notehead
                                    if obj['pitch'] in BLACK:
                                        if noteonoff and io['score']['properties']['black-note-style'] == 'PianoScript':
                                            io['pview'].create_oval(xx-(2.5*global_scale*staff_scale),
                                                          y0,
                                                          xx+(2.5*global_scale*staff_scale),
                                                          y0 + (10 * global_scale*staff_scale),
                                                          tag='black_notestart',
                                                          fill=color_black,
                                                          outline=color_black,
                                                          width=2 * global_scale*staff_scale)
                                        if noteonoff and io['score']['properties']['black-note-style'] == 'Klavarskribo':
                                            io['pview'].create_oval(xx-(5*global_scale*staff_scale),
                                                          y0,
                                                          xx+(5*global_scale*staff_scale),
                                                          y0 - (10 * global_scale*staff_scale),
                                                          tag='black_notestart',
                                                          fill=color_black,
                                                          outline=color_black,
                                                          width=2 * global_scale*staff_scale)
                                    else:
                                        if noteonoff: io['pview'].create_oval(x0,
                                                          y0,
                                                          x1,
                                                          y0 + (10 * global_scale*staff_scale),
                                                          tag='white_notestart',
                                                          fill=color_white,
                                                          outline=color_black,
                                                          width=2 * global_scale*staff_scale)

                            # if obj['stem-visible'] and stemonoff:
                            #     # connect stems; abs(evt['time'] - note['time']) <= 1
                            #     for stem in line:
                            #         if abs(stem['time'] - obj['time']) <= 1 and stem['type'] == 'note' and stem['pitch'] != obj['pitch'] and stem['staff'] == idx_st:
                            #             if abs(stem['time'] - obj['time']) <= 1 and stem['hand'] == obj['hand']:
                            #                 stem_x = note_x_pos(stem['pitch'], mn, mx, x_cursor, global_scale,io['score']['properties']['staff'][idx_st]['staff-scale'])
                            #                 if not idx_l and not idx_p:
                            #                     stem_y = event_y_pos_engrave(stem['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                            #                 elif not idx_p:
                            #                     stem_y = event_y_pos_engrave(stem['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                            #                 else:
                            #                     stem_y = event_y_pos_engrave(stem['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                            #                 io['pview'].create_line(stem_x,
                            #                                   stem_y,
                            #                                   xx,
                            #                                   y0,
                            #                                   width=3 * global_scale*staff_scale,
                            #                                   capstyle='round',
                            #                                   tag='connect_stem',
                            #                                   fill=color_black)

                        # time signature text
                        if obj['type'] == 'time_signature_text' and draw_barline_and_numbering:
                            if not idx_l and not idx_p:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                            elif not idx_p:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                            else:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                            io['pview'].create_text(x_cursor - (20 * global_scale*staff_scale),
                                              yy + (3 * global_scale*staff_scale),
                                              text=obj['text'],
                                              tag='tsigtext',
                                              anchor='e',
                                              font=('courier', 14, 'bold'),
                                              fill=color_black,
                                              angle=90)

                        # text
                        if obj['type'] == 'text':
                            if not idx_l and not idx_p:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                            elif not idx_p:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                            else:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                            xx = note_x_pos(obj['pitch'], mn, mx, x_cursor, global_scale,staff_scale)
                            io['pview'].create_text(xx,
                                                  yy,
                                                  text=obj['text'],
                                                  tag='text',
                                                  anchor='c',
                                                  angle=obj['angle'],
                                                  font=('Courier', 10, 'normal'),
                                                  fill=color_black)
                            # round_rectangle(io['pview'], io['pview'].bbox(t)[0]-(1*global_scale),
                            #                 io['pview'].bbox(t)[1]-(1*global_scale),
                            #                 io['pview'].bbox(t)[2]+(5*global_scale),
                            #                 io['pview'].bbox(t)[3]-(1*global_scale),
                            #                 fill=color_white,
                            #                 outline='',
                            #                 width=.5,
                            #                 tag='textbg')

                        # count_line
                        if obj['type'] == 'countline' and obj['staff'] == idx_st:
                            if not idx_l and not idx_p:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                            elif not idx_p:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                            else:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                            x1 = note_x_pos(obj['pitch1'], mn, mx, x_cursor, global_scale,staff_scale)
                            x2 = note_x_pos(obj['pitch2'], mn, mx, x_cursor, global_scale,staff_scale)

                            if countlineonoff: io['pview'].create_line(x1,
                                              yy,
                                              x2,
                                              yy,
                                              dash=(2, 2),
                                              tag='countline',
                                              fill=color_black,
                                              width=1*global_scale*staff_scale)

                        # start repeat
                        if obj['type'] == 'startrepeat':
                            if not idx_l and not idx_p:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                            elif not idx_p:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                            else:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                            io['pview'].create_line(x_cursor,yy,
                                x_cursor+sw+(50*global_scale*staff_scale),yy,
                                width=2*global_scale*staff_scale,
                                capstyle='round',
                                fill=color_black,
                                dash=(1,2))
                            io['pview'].create_oval(x_cursor+sw+(40*global_scale*staff_scale),yy+(5*global_scale*staff_scale),
                                x_cursor+sw+(45*global_scale*staff_scale),yy+(10*global_scale*staff_scale),
                                fill=color_black,
                                width=2*global_scale,
                                outline=color_black)
                            io['pview'].create_oval(x_cursor+sw+(30*global_scale*staff_scale),yy+(5*global_scale*staff_scale),
                                x_cursor+sw+(35*global_scale*staff_scale),yy+(10*global_scale*staff_scale),
                                fill=color_black,
                                width=2*global_scale*staff_scale,
                                outline=color_black)

                        # end repeat
                        if obj['type'] == 'endrepeat':
                            if not idx_l and not idx_p:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                            elif not idx_p:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                            else:
                                yy = event_y_pos_engrave(obj['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                            io['pview'].create_line(x_cursor+sw,yy,
                                x_cursor+sw+(50*global_scale*staff_scale),yy,
                                width=2*global_scale*staff_scale,
                                capstyle='round',
                                fill=color_black,
                                dash=(1,2))
                            io['pview'].create_oval(x_cursor+sw+(40*global_scale*staff_scale),yy-(5*global_scale*staff_scale),
                                x_cursor+sw+(45*global_scale*staff_scale),yy-(10*global_scale*staff_scale),
                                fill=color_black,
                                width=2*global_scale*staff_scale,
                                outline=color_black)
                            io['pview'].create_oval(x_cursor+sw+(30*global_scale*staff_scale),yy-(5*global_scale*staff_scale),
                                x_cursor+sw+(35*global_scale*staff_scale),yy-(10*global_scale*staff_scale),
                                fill=color_black,
                                width=2*global_scale*staff_scale,
                                outline=color_black)

                        # # beam grouping
                        # if obj['type'] == 'beam' and beamonoff and obj['staff'] == idx_st:

                        #     # beam right hand
                        #     if obj['hand'] == 'r' and obj['staff'] == idx_st:
                        #         beamnotelist = []
                        #         # right beam
                        #         for n in line:
                        #             if n['type'] == 'note' and n['time'] >= obj['time']+obj['duration']:
                        #                 break
                        #             elif n['type'] == 'note' and n['time'] >= obj['time'] and n['time'] < obj['time']+obj['duration'] and obj['hand'] == n['hand'] and n['stem-visible'] and n['staff'] == idx_st:
                        #                 beamnotelist.append(n)
                        #         # beamnotelist contains now all notes that need to be grouped using a beam.
                        #         # We check if we have to draw a beam; only if there are two or more notes in the beam:
                        #         if len(beamnotelist) < 2:
                        #             continue
                        #         # first we detect the highest and lowest note from the beam
                        #         h_note = {"pitch":1}
                        #         for bm in beamnotelist:
                        #             if bm['pitch'] >= h_note['pitch']:
                        #                 h_note = bm
                        #         h_notex = note_x_pos(h_note['pitch'],mn,mx,x_cursor,global_scale,staff_scale)
                        #         # now we have the highest beamnote position, we can draw this simple implementation
                        #         # for a beam. We draw from the highest position to a small portion higher to the end
                        #         # of the beam.
                        #         f_note = beamnotelist[0]
                        #         l_note = beamnotelist[-1]
                        #         if not idx_l and not idx_p:
                        #             f_notey = event_y_pos_engrave(f_note['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                        #         elif not idx_p:
                        #             f_notey = event_y_pos_engrave(f_note['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        #         else:
                        #             f_notey = event_y_pos_engrave(f_note['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                        #         if not idx_l and not idx_p:
                        #             l_notey = event_y_pos_engrave(l_note['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                        #         elif not idx_p:
                        #             l_notey = event_y_pos_engrave(l_note['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        #         else:
                        #             l_notey = event_y_pos_engrave(l_note['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                        #         if f_notey == l_notey:
                        #             continue
                        #         # drawing the beam:
                        #         io['pview'].create_line(h_notex+(25*global_scale*staff_scale),f_notey,
                        #                           h_notex+(30*global_scale*staff_scale),l_notey,
                        #                           tag='beam',
                        #                           width=5*global_scale*staff_scale,
                        #                           capstyle='round',
                        #                           fill=color_black)
                        #         # now we only have to connect the stems to the beam:
                        #         for bm in beamnotelist:
                        #             if not idx_l and not idx_p:
                        #                 yy = event_y_pos_engrave(bm['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                        #             elif not idx_p:
                        #                 yy = event_y_pos_engrave(bm['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        #             else:
                        #                 yy = event_y_pos_engrave(bm['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                        #             x = note_x_pos(bm['pitch'], mn, mx, x_cursor, global_scale,staff_scale)
                        #             stem_length = (5*interpolation(f_notey,l_notey,yy)*global_scale*staff_scale)
                        #             io['pview'].create_line(x+(25*global_scale*staff_scale),yy,
                        #                                 h_notex+(25*global_scale*staff_scale)+stem_length,yy,
                        #                                 tag='beam',
                        #                                 width=3*global_scale*staff_scale,
                        #                                 capstyle='round',
                        #                                 fill=color_black)
                        #     # beam left hand
                        #     if obj['hand'] == 'l' and obj['staff'] == idx_st:
                        #         beamnotelist = []
                        #         # left beam
                        #         for n in line:
                        #             if n['type'] == 'note' and n['time'] >= obj['time']+obj['duration']:
                        #                 break
                        #             elif n['type'] == 'note' and n['time'] >= obj['time'] and n['time'] < obj['time']+obj['duration'] and obj['hand'] == n['hand'] and n['stem-visible'] and n['staff'] == idx_st:
                        #                 beamnotelist.append(n)
                        #         # beamnotelist contains now all notes that need to be grouped using a beam.
                        #         # We check if we have to draw a beam; only if there are two or more notes in the beam:
                        #         if len(beamnotelist) < 2:
                        #             continue
                        #         # first we detect the highest and lowest note from the beam
                        #         lw_note = {"pitch":88}
                        #         for bm in beamnotelist:
                        #             if bm['pitch'] <= lw_note['pitch']:
                        #                 lw_note = bm
                        #         lw_notex = note_x_pos(lw_note['pitch'],mn,mx,x_cursor,global_scale,staff_scale)
                        #         # now we have the highest beamnote position, we can draw this simple implementation
                        #         # for a beam. We draw from the highest position to a small portion higher to the end
                        #         # of the beam.
                        #         f_note = beamnotelist[0]
                        #         l_note = beamnotelist[-1]
                        #         if not idx_l and not idx_p:
                        #             f_notey = event_y_pos_engrave(f_note['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                        #         elif not idx_p:
                        #             f_notey = event_y_pos_engrave(f_note['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        #         else:
                        #             f_notey = event_y_pos_engrave(f_note['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                        #         if not idx_l and not idx_p:
                        #             l_notey = event_y_pos_engrave(l_note['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                        #         elif not idx_p:
                        #             l_notey = event_y_pos_engrave(l_note['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        #         else:
                        #             l_notey = event_y_pos_engrave(l_note['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                        #         if f_notey == l_notey:
                        #             continue
                        #         # drawing the beam:
                        #         io['pview'].create_line(lw_notex-(25*global_scale*staff_scale),f_notey,
                        #                           lw_notex-(30*global_scale*staff_scale),l_notey,
                        #                           tag='beam',
                        #                           width=5*global_scale*staff_scale,
                        #                           capstyle='round',
                        #                           fill=color_black)
                        #         # now we only have to connect the stems to the beam:
                        #         for bm in beamnotelist:
                        #             if not idx_l and not idx_p:
                        #                 yy = event_y_pos_engrave(bm['time'], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                        #             elif not idx_p:
                        #                 yy = event_y_pos_engrave(bm['time'], split_times[idx_l], split_times[idx_l + 1],True,False)
                        #             else:
                        #                 yy = event_y_pos_engrave(bm['time'], split_times[idx_l], split_times[idx_l + 1],False,False)
                        #             x = note_x_pos(bm['pitch'], mn, mx, x_cursor, global_scale,io['score']['properties']['staff'][idx_st]['staff-scale'])
                        #             stem_length = (5*interpolation(f_notey,l_notey,yy)*global_scale*staff_scale)
                        #             io['pview'].create_line(x-(25*global_scale*staff_scale),yy,
                        #                                 lw_notex-(25*global_scale*staff_scale)-stem_length,yy,
                        #                                 tag='beam',
                        #                                 width=3*global_scale*staff_scale,
                        #                                 capstyle='round',
                        #                                 fill=color_black)

                        # slur
                        if obj['type'] == 'slur':
                            if not idx_l and not idx_p:
                                p1 = event_y_pos_engrave(obj['points'][0][0], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                                p2 = event_y_pos_engrave(obj['points'][1][0], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                                p3 = event_y_pos_engrave(obj['points'][2][0], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                                p4 = event_y_pos_engrave(obj['points'][3][0], split_times[idx_l], split_times[idx_l + 1],True,minipiano)
                            elif not idx_p:
                                p1 = event_y_pos_engrave(obj['points'][0][0], split_times[idx_l], split_times[idx_l + 1],True,False)
                                p2 = event_y_pos_engrave(obj['points'][1][0], split_times[idx_l], split_times[idx_l + 1],True,False)
                                p3 = event_y_pos_engrave(obj['points'][2][0], split_times[idx_l], split_times[idx_l + 1],True,False)
                                p4 = event_y_pos_engrave(obj['points'][3][0], split_times[idx_l], split_times[idx_l + 1],True,False)
                            else:
                                p1 = event_y_pos_engrave(obj['points'][0][0], split_times[idx_l], split_times[idx_l + 1],False,False)
                                p2 = event_y_pos_engrave(obj['points'][1][0], split_times[idx_l], split_times[idx_l + 1],False,False)
                                p3 = event_y_pos_engrave(obj['points'][2][0], split_times[idx_l], split_times[idx_l + 1],False,False)
                                p4 = event_y_pos_engrave(obj['points'][3][0], split_times[idx_l], split_times[idx_l + 1],False,False)
                            t1 = note_x_pos(obj['points'][0][1], mn, mx, x_cursor, global_scale,staff_scale)
                            t2 = note_x_pos(obj['points'][1][1], mn, mx, x_cursor, global_scale,staff_scale)
                            t3 = note_x_pos(obj['points'][2][1], mn, mx, x_cursor, global_scale,staff_scale)
                            t4 = note_x_pos(obj['points'][3][1], mn, mx, x_cursor, global_scale,staff_scale)

                            # calculate slur
                            slur_points = []
                            for t in range(100):
                                x, y = evaluate_cubic_bezier(t / 100, [[t1,p1],[t2,p2],[t3,p3],[t4,p4]])
                                slur_points.append([x, y])
                            for t in reversed(range(100)):
                                x, y = evaluate_cubic_bezier(t / 100, [[t1,p1],[t2+5,p2],[t3+5,p3],[t4,p4]])
                                slur_points.append([x, y])
                            # draw slur
                            io['pview'].create_polygon(slur_points, fill='black', tag='slur')
                            # io['pview'].create_line(slur_points, fill='black', tag='slur', width=4*global_scale*staff_scale,capstyle='round')

                        # end for obj ----------------------------------------

                    # update x_cursor and divide the systems equal:
                    x_cursor += sw + st_marg_r

                idx_l += 1

                # end for line ---------------------------------------

            x_cursor = page_width * (idx_p + 1)


        # draw bottom line page
        if render_type == 'normal':
            io['pview'].create_line(0,
                page_height,
                page_width,
                page_height,
                fill=color_black,
                width=2,
                dash=(6,4,5,2,3,1))

        # drawing order
        io['pview'].tag_raise('countline')
        io['pview'].tag_raise('staff')
        io['pview'].tag_raise('grid')
        io['pview'].tag_raise('white_space')
        io['pview'].tag_raise('notestop')
        io['pview'].tag_raise('stem')
        io['pview'].tag_raise('white_notestart')
        io['pview'].tag_raise('black_notestart')
        io['pview'].tag_raise('accidental')
        io['pview'].tag_raise('connect_stem')
        io['pview'].tag_raise('titles')
        io['pview'].tag_raise('cursor')
        io['pview'].tag_raise('endpaper')
        io['pview'].tag_raise('left_dot')
        io['pview'].tag_raise('tie_dot')
        io['pview'].tag_raise('textbg')
        io['pview'].tag_raise('text')
        io['pview'].tag_raise('continuation_dot')
        io['pview'].tag_raise('end-of-note')
        io['pview'].tag_lower('midi_note')

        # make the new render update fluently(without blinking) and scale
        if not render_type == 'export':
            io['root'].update()
            s = io['pview'].winfo_width() / page_width
            io['pview'].scale("all", 0, 0, s, s)
        io['pview'].move('all', 0, 10000)
        io['pview'].delete('old')
        if not render_type == 'export':
            io['pview'].configure(scrollregion=io['pview'].bbox("all"))
        io['pview'].addtag_all('old')

    draw()

    return len(DOC)
