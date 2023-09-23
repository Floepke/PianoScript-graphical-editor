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

# imports
from tkinter.messagebox import askyesnocancel
from tkinter import filedialog
from imports.savefilestructure import BluePrint
import os, mido

class Midi():
    def __init__(self, io):
        self.io = io

    def load_midi(self):
        print('load_midi()')
        # check if user wants to save, not save or cancel the task.
        if self.io['savefile_system']['filechanged']:
            ask = askyesnocancel('Wish to save?', 'Do you wish to save the current Score?')
            if ask == True:
                self.io['main_editor'].save()
            elif ask == False:
                ...
            elif ask == None:
                return
        else:
            ...

        midifile = filedialog.askopenfile(parent=self.io['root'],
                                            mode='r',
                                            title='Open midi...',
                                            filetypes=[("MIDI files", "*.mid")])

        if midifile:
            midifile = midifile.name

            # as starting point we load the source Blueprint/template
            self.io['score'] = BluePrint

            # set title to name of the midi file
            self.io['score']['header']['title']['text'] = os.path.splitext(os.path.basename(midifile))[0]

            # clear grid
            self.io['score']['events']['grid'] = []

            # ---------------------------------------------
            # translate midi data to note messages with
            # the right start and stop (piano)ticks.
            # ---------------------------------------------
            mesgs = []
            mid = mido.MidiFile(midifile)
            tpb = mid.ticks_per_beat
            msperbeat = 1
            for i in mid:
                mesgs.append(i.dict())
            ''' convert time to pianotick '''
            for i in mesgs:
                i['time'] = tpb * (1 / msperbeat) * 1000000 * i['time'] * (256 / tpb)
                if i['type'] == 'set_tempo':
                    msperbeat = i['tempo']
            ''' change time values from delta to relative time. '''
            memory = 0
            for i in mesgs:
                i['time'] += memory
                memory = i['time']
                # change every note_on with 0 velocity to note_off.
                if i['type'] == 'note_on' and i['velocity'] == 0:
                    i['type'] = 'note_off'
            ''' get note_on, note_off, time_signature durations. '''
            index = 0
            for i in mesgs:
                if i['type'] == 'note_on':
                    for n in mesgs[index:]:         
                        if n['type'] == 'note_off' and i['note'] == n['note']:
                            print(n['time'], ' - ', i['time'], ' = ', n['time']-i['time'])
                            i['duration'] = n['time'] - i['time']
                            break

                if i['type'] == 'time_signature':
                    for t in mesgs[index + 1:]:
                        if t['type'] == 'time_signature' or t['type'] == 'end_of_track':
                            i['duration'] = t['time'] - i['time']
                            break
                index += 1

            # check for messages without duration:
            for i in mesgs:
                if i['type'] == 'note_on':
                    if not 'duration' in i:
                        i['duration'] = 0

            # write time_signatures:
            count = 0
            for i in mesgs:
                if i['type'] == 'time_signature':
                    tsig = (i['numerator'], i['denominator'])
                    amount = int(round(i['duration'] / int(i['numerator'] * (1024 / i['denominator']))))
                    gridno = i['numerator']
                    if tsig == '6/8':
                        gridno = 2
                    if tsig == '12/8':
                        gridno = 4
                    self.io['score']['events']['grid'].append(
                        {'amount': amount, 'numerator': i['numerator'], 'denominator': i['denominator'],
                         'grid': gridno, 'visible': 1})
                    count += 1

            # write notes
            # we calculate the average of the notes, if we have more than 2 channels, the lowest is called p(edal), the 2nd lowest l(eft), the 
            # 3rd r(ight). If there are more than 3 channels, they are directed to 'l' and 'r' 
            channelsum={}
            notes_in_channel={}
            channelmax={}
            channelmin={}
            channelmean={}
            for i in mesgs:
                if i['type'] == 'note_on':
                    c=i['channel']
                    if c not in channelsum:
                        channelsum[c]=0
                        notes_in_channel[c]=0
                        channelmax[c]=-128
                        channelmin[c]=128

                    channelsum[c]+=i['note']
                    notes_in_channel[c]+=1
                    if i['note'] < channelmin[c]:
                        channelmin[c]=i['note']
                    if i['note'] > channelmax[c]:
                        channelmax[c]=i['note']

            for c in channelsum:
                channelmean[c]=channelsum[c]/notes_in_channel[c]

            xx=dict(sorted(channelmean.items(), key=lambda item: item[1]))
            hand={}
            name=['r','l','r','l','r','l','r','l','r','l','r','l','r','l','r','l','r','l','r','l']
            if len(xx) > 2:
                for i,x in enumerate(xx):
                    hand[x]=name[i]
            else:
                for i,x in enumerate(xx):
                    hand[x]=name[i+1]

            for i in mesgs:
                if i['type'] == 'note_on':
                    print(i)
                    self.io['score']['events']['note'].append({'time': i['time'], 
                                                    'duration': i['duration'], 
                                                    'pitch': i['note'] - 20, 
                                                    'hand': hand[i['channel']], 
                                                    'tag':self.io['new_tag'],
                                                    'stem-visible':True,
                                                    'accidental':0,
                                                    'staff':0,
                                                    'notestop':True})
                    self.io['new_tag'] += 1

    def export_midi(self):
        ...
