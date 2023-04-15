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

from midiutil.MidiFile import MIDIFile
from tkinter import filedialog
from imports.tools import *

def midiexport(root,Score):

    f = filedialog.asksaveasfile(parent=root, 
        title='Save midi...', 
        filetypes=[("midi files", "*.mid")])
    
    if f:
        # create empoty midifile
        midi = MIDIFile(1)

        # add tempo
        midi.addTempo(0, 0, 120)# track, time, tempo

        # add timesignatures
        time = 0
        for ts in Score['properties']['grid']:
            
            midi.addTimeSignature(0, time, ts['numerator'], 2, 24)

            # calculate the length of the time signature:
            for l in range(ts['amount']):
                time += measure_length((ts['numerator'],ts['denominator']))

        # add the notes:
        for note in Score['events']['note']:
            if note['hand'] == 'r':
                midi.addNote(0,0,note['pitch']+20,note['time'],.5,64)# addNote(track, channel, pitch, time, duration, volume, annotation=None)
            else:
                midi.addNote(0,1,note['pitch']+20,note['time'],.5,64)

        # save the midifile
        with open("major-scale.mid", "wb") as output_file:
            midi.writeFile(output_file)
