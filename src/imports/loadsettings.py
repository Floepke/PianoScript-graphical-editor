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
# which contains all editor settings. (editor_settings.json)
# The TEMPLATE in the source code is used to create a template.pianoscript
# file in the same folder as editor_settings.json
Settings = {
"editor-x-zoom":35,
"editor-y-zoom":80,
"default-page-margin-left":10,
"default-page-margin-right":10,
"default-page-margin-up":10,
"default-page-margin-down":10,
"default-draw-scale":0.75,
"default-margin-up-left":10,
"default-margin-down-right":10
}
try:
    with open('editor_settings.json', 'r') as f:
        Settings = json.load(f)
except:
    with open('editor_settings.json', 'w') as f:
        f.write(json.dumps(Settings, separators=(',', ':'), indent=2))