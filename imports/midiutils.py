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
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo, second2tick

def midiexport(root,Score):

    f = filedialog.asksaveasfile(parent=root, 
        title='Save midi...', 
        filetypes=[("midi files", "*.mid")])
    
    if f:
        mid = MidiFile(ticks_per_beat=256*64)
        track = MidiTrack()
        track.append(MetaMessage('set_tempo', tempo=bpm2tempo(120)))

        times = 0
        for ts in Score['events']['grid']:
            track.append(MetaMessage('time_signature', numerator=ts['numerator'], denominator=ts['denominator'], time=times))
            for l in range(ts['amount']):
                times += (measure_length((ts['numerator'],ts['denominator']))*64)
        # add the notes:
        # in order to add the notes at delta time we need to create a list of note_on and note_off messages in linear time first:
        msg = []
        for note in Score['events']['note']:
            t = note['time'] / (256*64)
            d = note['duration'] / (256*64)
            if note['hand'] == 'l':
                msg.append({'type':'note_on','channel':0,'pitch':note['pitch']+20,'velocity':64,'time':t})
                msg.append({'type':'note_off','channel':0,'pitch':note['pitch']+20,'velocity':0,'time':t+d})
            else:
                msg.append({'type':'note_on','channel':1,'pitch':note['pitch']+20,'velocity':64,'time':t})
                msg.append({'type':'note_off','channel':1,'pitch':note['pitch']+20,'velocity':0,'time':t+d})
        # now we have a msg list with note_on and note_off messages in linear time and we need to convert and sort
        # the messages to delta time:
        msg = sorted(msg, key=lambda time: time['time'])
        prev_time = 0
        for m in msg:
            t = m['time']
            m['time'] = m['time'] - prev_time
            prev_time = t
        # write messages to midifile object in delta times:
        for m in msg:
            t = int(round(m['time']))
            track.append(Message(m['type'], channel=m['channel'], note=m['pitch'], velocity=m['velocity'], time=t))
        track.append(MetaMessage('end_of_track'))
        mid.tracks.append(track)
        mid.save(f.name)
