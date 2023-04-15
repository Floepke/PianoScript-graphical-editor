'''
Copyright 2023 Philip Bergwerf

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