#! python3.9.2
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

from imports.colors import color_dark, color_light, color_highlight, color_gui_light, color_gui_dark

STYLE = {
    ".": {
        "configure": {
            "background": color_light, # All except tabs
            "foreground": color_dark,
            "font": ('courier', 16)
        }
    },
    "TNotebook": {
        "configure": {
            "background": color_light, # Your margin color
            "tabmargins": [2, 5, 0, 0], # margins: left, top, right, separator
        }
    },
    "TNotebook.Tab": {
        "configure": {
            "background": color_light, # tab color when not selected
            "padding": [10, 2], # [space between text and horizontal tab-button border, space between text and vertical tab_button border]
            "font":["courier", 16]
        },
        "map": {
            "background": [("selected", color_highlight)], # Tab color when selected
            "expand": [("selected", [1, 1, 1, 0])] # text margins
        }
    },
    "Treeview": {
        "configure": {
            "background": color_light,
            "foreground": color_dark,
            "font":("courier", 16),
            "fieldbackground": color_gui_light
        },
        "map": {
            "background": [("selected", color_highlight)],
            "foreground": [("selected", color_dark)], # Tab color when selected
            "expand": [("selected", [1, 1, 1, 0])] # text margins
        }
    }
}