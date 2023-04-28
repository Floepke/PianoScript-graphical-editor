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

import json

# the Settings variable is a json file the get's saves automatically to disk
# which contains all editor settings (editor_settings.json)and default file settings.
# The user can change editor_settings.json with a text editor ro change the default
# settings for new files.


# ------------------------
# save file structure
# ------------------------
Score = {
  "header": {
    "title": {
      "text": "Untitled",
      "x-offset": 0,
      "y-offset": 0,
      "visible": True
    },
    "composer": {
      "text": "PianoScript",
      "x-offset": 0,
      "y-offset": 0,
      "visible": True
    },
    "copyright": {
      "text": "© PianoScript 2023",
      "x-offset": 0,
      "y-offset": 0,
      "visible": True
    },
    "app-name": "pianoscript",
    "app-version": 1.0
  },
  "properties": {
    "page-width": 210,
    "page-height": 297,
    "page-margin-left": 10,
    "page-margin-right": 10,
    "page-margin-up": 10,
    "page-margin-down": 10,
    "draw-scale": 1,
    "header-height":10,
    "footer-height":10,
    "minipiano":True,
    "engraver":'pianoscript',
    "color-right-hand-midinote":'#c8c8c8',
    "color-left-hand-midinote":'#c8c8c8',
    "printview-width(procents-froms-creen)":33,
    "editor-x-zoom":35,
    "editor-y-zoom":80
  },
  "events": {
    "grid": [
      {
        "amount": 8,
        "numerator": 4,
        "denominator": 4,
        "grid": 4,
        "visible": True
      }
    ],
    "note": [],
    "text": [],
    "bpm": [],
    "slur": [],
    "pedal": [],
    "line-break":[
      {
        "id":"linebreak",
        "time":0,
        "margin-up-left":10,
        "margin-down-right":10
      }
    ],
    "count-line":[],
    "staff-sizer":[],
    "start-repeat":[],
    "end-repeat":[],
    "start-hook":[],
    "end-hook":[]
  }
}
try:
    with open('template.pianoscript', 'r') as f:
        Score = json.load(f)
except:
    with open('template.pianoscript', 'w') as f:
        f.write(json.dumps(Score, separators=(',', ':'), indent=2))