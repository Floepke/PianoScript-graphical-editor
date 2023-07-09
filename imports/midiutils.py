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
from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo, second2tick, open_output, get_output_names
import midiutil as mt
import time


def midiexport(root,Score):

    f = filedialog.asksaveasfile(parent=root,
         title='Save midi...',
         filetypes=[("midi files", "*.mid")])

    # configure channels and names
    longname={'l':'left','r':'right','p':'pedal'}
    trackname={}
    channel={}
    nrchannels=0
    for note in Score['events']['note']:
        if note['hand'] not in channel:
            channel[note['hand']]=nrchannels
            trackname[nrchannels]=longname[note['hand']]
            nrchannels+=1

    # some info for the midifile
    clocks_per_tick=24
    denominator_dict = {
        1:0,
        2:1,
        4:2,
        8:3,
        16:4,
        32:5,
        64:6,
        128:7,
        256:8
    }
    ticks_per_quarternote = 2048

    # preparing the midi file
    MyMIDI = MIDIFile(numTracks=nrchannels, removeDuplicates=True, deinterleave=True, adjust_origin=False, file_format=1, ticks_per_quarternote=ticks_per_quarternote, eventtime_is_ticks=True) 
    for ts in Score['events']['grid']:
        for c in range(nrchannels):
            MyMIDI.addTimeSignature(track=c,time=0, numerator=int(ts['numerator']), denominator=denominator_dict[int(ts['denominator'])], clocks_per_tick=clocks_per_tick, notes_per_quarter=8)
            MyMIDI.addTempo(track=c,time=0, tempo=120)
            MyMIDI.addTrackName(track=c,time=0, trackName=trackname[c])

    # adding the notes
    for note in Score['events']['note']:
        t = int(note['time']/256*ticks_per_quarternote)
        d = int(note['duration']/256*ticks_per_quarternote)
        MyMIDI.addNote(track=channel[note['hand']], channel=channel[note['hand']], pitch=int(note['pitch']+20), time=t, duration=d,volume=100,annotation=None) # pitch - 20 ???

    # saving the midi file
    with open(f.name, "wb") as output_file:
        MyMIDI.writeFile(output_file)


# TODO
# * I want to build a play midi function that sends midi data trough a midi port so you can use an external synth or sampled piano to hear the music in the file.

# # play the song trough a midi port that can be selected by external synth
# MIDIplayerSwitch = False
# def play_midi(event, Score, midi_file_path, root):
    
#     '''Playing the midi-file trough midi port'''

#     mf = MIDIFile(1)
#     mf.addTempo(0,0, 120)

#     for note in Score['events']['note']:
#         if note['hand'] == 'l':
#             mf.addNote(0, 0, note['pitch']+20, note['time']/256, note['duration'], 80)
#         else:
#             mf.addNote(0, 1, note['pitch']+20, note['time']/256, note['duration'], 80)

#     with open("PLAYER.mid", "wb") as output_file:
#         mf.writeFile(output_file)

#     mf = MidiFile('PLAYER.mid')
#     names = get_output_names()
#     port = open_output(names[0])
#     for msg in mf.play():
#         port.send(msg)

#     # for msg in MidiFile('PLAYER.mid'):
#     #     time.sleep(msg.time)
#     #     port = open_output('Port Name')
#     #     if not msg.is_meta:
#     #         port.send(msg)


