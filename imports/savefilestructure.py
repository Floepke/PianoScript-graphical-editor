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
from datetime import datetime

# the Settings variable is a json file the get's saves automatically to disk
# which contains all editor settings (editor_settings.json)and default file settings.
# The user can change editor_settings.json with a text editor ro change the default
# settings for new files.


# ------------------------
# save file structure
# ------------------------
Score = {}

# ------------------------
# Blueprint
# ------------------------
BluePrint = {
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
    "app-version": 1.0,
    "date":datetime.now().strftime("%d-%m-%Y"),
    "genre":"",
    "comment":""
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
    "engraver":'pianoscript vertical',
    "color-right-hand-midinote":'#c8c8c8',
    "color-left-hand-midinote":'#c8c8c8',
    "printview-width(procents-froms-creen)":33,
    "editor-x-zoom":35,
    "editor-y-zoom":80,
    "staffonoff":True,
    "stemonoff":True,
    "beamonoff":True,
    "noteonoff":True,
    "midinoteonoff":True,
    "notestoponoff":True,
    "pagenumberingonoff":True,
    "barlinesonoff":True,
    "basegridonoff":True,
    "countlineonoff":True,
    "measurenumberingonoff":True,
    "accidentalonoff":True,
    "staff":[
      {
        "onoff":True,
        "name":"Staff 1",
        "staff-number":0,
        "staff-scale":1.0
      },
      {
        "onoff":False,
        "name":"Staff 2",
        "staff-number":1,
        "staff-scale":1.0
      },
      {
        "onoff":False,
        "name":"Staff 3",
        "staff-number":2,
        "staff-scale":1.0
      },
      {
        "onoff":False,
        "name":"Staff 4",
        "staff-number":3,
        "staff-scale":1.0
      }
    ],
    "soundingdotonoff":True,
    "black-note-style":"PianoScript",
    "threelinescale":1,
    "stop-sign-style":'PianoScript',
    "leftdotonoff":True
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
    "beam": [],
    "bpm":[],
    "slur": [],
    "pedal": [],
    "line-break":[
      {
        "id":"linebreak",
        "time":0,
        "margin-staff1-left":10,
        "margin-staff1-right":10,
        "margin-staff2-left":10,
        "margin-staff2-right":10,
        "margin-staff3-left":10,
        "margin-staff3-right":10,
        "margin-staff4-left":10,
        "margin-staff4-right":10,
        "staff":0
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

# template system:
try: # to load template.pianoscript
    with open('template.pianoscript', 'r') as f:
        Score = json.load(f)
except: # if template.pianoscript does not exists; create a new template from BluePrint
    with open('template.pianoscript', 'w') as f:
        f.write(json.dumps(BluePrint, separators=(',', ':'), indent=2))

def compatibility_checker(Score):
    '''Correct any missing parameter in the .pianoscript file'''
  
    # header
    if not 'header' in Score: Score['header'] = BluePrint['header']
    if not 'title' in Score['header']: Score['header']['title'] = BluePrint['header']['title']
    if not 'composer' in Score['header']: Score['header']['composer'] = BluePrint['header']['composer']
    if not 'copyright' in Score['header']: Score['header']['copyright'] = BluePrint['header']['copyright']
    if not 'app-name' in Score['header']: Score['header']['app-name'] = BluePrint['header']['app-name']
    if not 'app-version' in Score['header']: Score['header']['app-version'] = BluePrint['header']['app-version']
    if not 'date' in Score['header']: Score['header']['date'] = BluePrint['header']['date']
    if not 'genre' in Score['header']: Score['header']['genre'] = BluePrint['header']['genre']
    if not 'comment' in Score['header']: Score['header']['comment'] = BluePrint['header']['comment']

    # properties
    if not 'properties' in Score: Score['properties'] = BluePrint['properties']
    Score['properties']['page-width'] = Score['properties'].get('page-width', BluePrint['properties']['page-width'])
    Score['properties']['page-height'] = Score['properties'].get('page-height', BluePrint['properties']['page-height'])
    Score['properties']['page-margin-left'] = Score['properties'].get('page-margin-left', BluePrint['properties']['page-margin-left'])
    Score['properties']['page-margin-right'] = Score['properties'].get('page-margin-right', BluePrint['properties']['page-margin-right'])
    Score['properties']['page-margin-up'] = Score['properties'].get('page-margin-up', BluePrint['properties']['page-margin-up'])
    Score['properties']['page-margin-down'] = Score['properties'].get('page-margin-down', BluePrint['properties']['page-margin-down'])
    Score['properties']['draw-scale'] = Score['properties'].get('draw-scale', BluePrint['properties']['draw-scale'])
    Score['properties']['header-height'] = Score['properties'].get('header-height', BluePrint['properties']['header-height'])
    Score['properties']['footer-height'] = Score['properties'].get('footer-height', BluePrint['properties']['footer-height'])
    Score['properties']['minipiano'] = Score['properties'].get('minipiano', BluePrint['properties']['minipiano'])
    Score['properties']['engraver'] = Score['properties'].get('engraver', BluePrint['properties']['engraver'])
    Score['properties']['color-right-hand-midinote'] = Score['properties'].get('color-right-hand-midinote', BluePrint['properties']['color-right-hand-midinote'])
    Score['properties']['color-left-hand-midinote'] = Score['properties'].get('color-left-hand-midinote', BluePrint['properties']['color-left-hand-midinote'])
    Score['properties']['printview-width(procents-froms-creen)'] = Score['properties'].get('printview-width(procents-froms-creen)', BluePrint['properties']['printview-width(procents-froms-creen)'])
    Score['properties']['editor-x-zoom'] = Score['properties'].get('editor-x-zoom', BluePrint['properties']['editor-x-zoom'])
    Score['properties']['editor-y-zoom'] = Score['properties'].get('editor-y-zoom', BluePrint['properties']['editor-y-zoom'])
    Score['properties']['staffonoff'] = Score['properties'].get('staffonoff', BluePrint['properties']['staffonoff'])
    Score['properties']['stemonoff'] = Score['properties'].get('stemonoff', BluePrint['properties']['stemonoff'])
    Score['properties']['beamonoff'] = Score['properties'].get('beamonoff', BluePrint['properties']['beamonoff'])
    Score['properties']['noteonoff'] = Score['properties'].get('noteonoff', BluePrint['properties']['noteonoff'])
    Score['properties']['midinoteonoff'] = Score['properties'].get('midinoteonoff', BluePrint['properties']['midinoteonoff'])
    Score['properties']['notestoponoff'] = Score['properties'].get('notestoponoff', BluePrint['properties']['notestoponoff'])
    Score['properties']['pagenumberingonoff'] = Score['properties'].get('pagenumberingonoff', BluePrint['properties']['pagenumberingonoff'])
    Score['properties']['barlinesonoff'] = Score['properties'].get('barlinesonoff', BluePrint['properties']['barlinesonoff'])
    Score['properties']['basegridonoff'] = Score['properties'].get('basegridonoff', BluePrint['properties']['basegridonoff'])
    Score['properties']['countlineonoff'] = Score['properties'].get('countlineonoff', BluePrint['properties']['countlineonoff'])
    Score['properties']['measurenumberingonoff'] = Score['properties'].get('measurenumberingonoff', BluePrint['properties']['measurenumberingonoff'])
    Score['properties']['accidentalonoff'] = Score['properties'].get('accidentalonoff', BluePrint['properties']['accidentalonoff'])
    if not 'staff' in Score['properties']: Score['properties']['staff'] = BluePrint['properties']['staff']
    Score['properties']['soundingdotonoff'] = Score['properties'].get('soundingdotonoff', BluePrint['properties']['soundingdotonoff'])
    Score['properties']['black-note-style'] = Score['properties'].get('black-note-style', BluePrint['properties']['black-note-style'])
    Score['properties']['threelinescale'] = Score['properties'].get('threelinescale', BluePrint['properties']['threelinescale'])
    Score['properties']['stop-sign-style'] = Score['properties'].get('stop-sign-style', BluePrint['properties']['stop-sign-style'])
    Score['properties']['leftdotonoff'] = Score['properties'].get('leftdotonoff', BluePrint['properties']['leftdotonoff'])


    # events
    # note
    for e in Score['events']['note']:
        e['id'] = e.get('id','note')
        e['time'] = e.get('time',0)
        e['duration'] = e.get('duration',256)
        e['pitch'] = e.get('pitch',40)
        e['hand'] = e.get('hand','r')
        e['stem-visible'] = e.get('stem-visible',True)
        e['accidental'] = e.get('accidental',0)
        e['type'] = e.get('type','note')
        e['staff'] = e.get('staff',0)
        e['notestop'] = e.get('notestop',True)

    # text
    for e in Score['events']['text']:
        e['id'] = e.get('id','text')
        e['time'] = e.get('time',0)
        e['pitch'] = e.get('pitch',40)
        e['text'] = e.get('text','text...')
        e['angle'] = e.get('angle',0)
        e['staff'] = e.get('staff',0)
        e['type'] = e.get('type','text')

    # beam
    for e in Score['events']['beam']:
        e['id'] = e.get('id','beam')
        e['time'] = e.get('time',0)
        e['duration'] = e.get('duration',256)
        e['hand'] = e.get('hand','r')
        e['staff'] = e.get('staff',0)
        e['type'] = e.get('type','beam')

    # bpm
    ...# not yet implemented

    # slur
    for e in Score['events']['slur']:
        e['id'] = e.get('id','slur')
        e['time'] = e.get('time',0)
        e['points'] = e.get('points',[[0,40],[0,40],[0,40],[0,40]])
        e['hand'] = e.get('hand','r')
        e['staff'] = e.get('staff',0)
        e['type'] = e.get('type','slur')

    # pedal
    ...# not yet implemented

    # linebreak
    for e in Score['events']['line-break']:
        e['id'] = e.get('id','linebreak')
        e['margin-staff1-left'] = e.get('margin-staff1-left',10)
        e['margin-staff1-right'] = e.get('margin-staff1-right',10)
        e['margin-staff2-left'] = e.get('margin-staff2-left',10)
        e['margin-staff2-right'] = e.get('margin-staff2-right',10)
        e['margin-staff3-left'] = e.get('margin-staff3-left',10)
        e['margin-staff3-right'] = e.get('margin-staff3-right',10)
        e['margin-staff4-left'] = e.get('margin-staff4-left',10)
        e['margin-staff4-right'] = e.get('margin-staff4-right',10)
        e['staff'] = e.get('staff',0)
        e['type'] = e.get('type','linebreak')

    # countline
    for e in Score['events']['count-line']:
        e['id'] = e.get('id','countline')
        e['time'] = e.get('time',0)
        e['pitch1'] = e.get('pitch1',40)
        e['pitch2'] = e.get('pitch2',44)
        e['staff'] = e.get('staff',0)
        e['type'] = e.get('type','countline')

    # staffsizer
    for e in Score['events']['staff-sizer']:
        e['id'] = e.get('id','staffsizer')
        e['time'] = e.get('time',0)
        e['pitch1'] = e.get('pitch1',40)
        e['pitch2'] = e.get('pitch2',44)
        e['staff'] = e.get('staff',0)
        e['type'] = e.get('type','staffsizer')

    # start repeat
    for e in Score['events']['start-repeat']:
        e['id'] = e.get('id','startrepeat')
        e['time'] = e.get('time',0)
        e['type'] = e.get('type','startrepeat')

    # end repeat
    for e in Score['events']['end-repeat']:
        e['id'] = e.get('id','endrepeat')
        e['time'] = e.get('time',0)
        e['type'] = e.get('type','endrepeat')

    # start hook
    ...# not yet implemented

    # end hook
    ...# not yet implemented


    return Score
