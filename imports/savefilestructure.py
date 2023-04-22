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

import json

# the Settings variable is a json file the get's saves automatically to disk
# which contains all editor settings (editor_settings.json)and default file settings.
# The user can change editor_settings.json with a text editor ro change the default
# settings for new files.
Settings = {
    "editor-x-zoom":35,
    "editor-y-zoom":80,
    "default-page-width":210,
    "default-page-height":297,
    "default-page-margin-left":10,
    "default-page-margin-right":10,
    "default-page-margin-up":10,
    "default-page-margin-down":10,
    "default-draw-scale":1,
    "default-margin-up-left":10,
    "default-margin-down-right":10,
    "default-engraver":"pianoscript",
    "default-color-right-hand-midinote":"#999999",
    "default-color-left-hand-midinote":"#999999",
    "default-minipiano":True,
    "default-header-height":5,
    "default-footer-height":10,
    "printview-width(procents-froms-creen)":33
}
try:
    with open('editor_settings.json', 'r') as f:
        Settings = json.load(f)
except:
    with open('editor_settings.json', 'w') as f:
        f.write(json.dumps(Settings, separators=(',', ':'), indent=2))


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
    "page-width": Settings['default-page-width'],
    "page-height": Settings['default-page-height'],
    "page-margin-left": Settings['default-page-margin-left'],
    "page-margin-right": Settings['default-page-margin-right'],
    "page-margin-up": Settings['default-page-margin-up'],
    "page-margin-down": Settings['default-page-margin-down'],
    "draw-scale": Settings['default-draw-scale'],
    "header-height":Settings['default-header-height'],
    "footer-height":Settings['default-footer-height'],
    "minipiano":Settings['default-minipiano'],
    "engraver":Settings['default-engraver'],
    "color-right-hand-midinote":Settings['default-color-right-hand-midinote'],
    "color-left-hand-midinote":Settings['default-color-left-hand-midinote'],
    "printview-width(procents-froms-creen)":Settings['printview-width(procents-froms-creen)']
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
    ]
  }
}
try:
    with open('template.pianoscript', 'r') as f:
        Score = json.load(f)
except:
    with open('template.pianoscript', 'w') as f:
        f.write(json.dumps(Score, separators=(',', ':'), indent=2))