# ------------------
# FILE management
# ------------------
import json, threading
from tkinter import filedialog












file_changed = False
file_path = ''


def test_file():
    print('loading test file...')
    with open('pianoscript_newfile.pianoscript', 'r') as f:
        global FILE
        FILE = json.load(f)

        # run the piano-roll and print-view
        threading.Thread(target=draw_pianoroll).start()
        do_engrave('')
        root.title('PianoScript - %s' % f.name)

def new_file():
    print('new_file')
    
    # Check if user wants to save or cancel the task.
    if file_changed == True:
        ask = messagebox.askyesnocancel('Wish to save?', 'Do you wish to save the current FILE?')
        if ask == True:
            save_as()
        elif ask == False:
            ...
        else:
            return
    else:
        ...

    # Create new FILE
    print('creating new file...')
    global FILE
    FILE = {"header":{"title":{"text":"Untitled","x-offset":0,"y-offset":0,"visible":True},"composer":{"text":"PianoScript","x-offset":0,"y-offset":0,"visible":True},"copyright":{"text":"\u00a9 PianoScript 2023","x-offset":0,"y-offset":0,"visible":True},"app-name":"pianoscript","app-version":1.0},"properties":{"page-width":210,"page-height":297,"page-margin-left":50,"page-margin-right":50,"page-margin-up":50,"page-margin-down":50,"draw-scale":0.85,"measure-line-division":[4],"line-margin":[50],"grid":[{"amount":8,"numerator":4,"denominator":4,"grid":4,"visible":True}]},"events":{"note":[],"text":[],"bpm":[],"slur":[],"pedal":[]}}

    # Set window title
    root.title('PianoScript - New')
    file_path = 'New'


def load_file(root):
    print('load_file')

    # Check if user wants to save or cancel the task.
    if file_changed == True:
        ask = messagebox.askyesnocancel('Wish to save?', 'Do you wish to save the current FILE?')
        if ask == True:
            save_file()
        elif ask == False:
            ...
        else:
            return
    else:
        ...

    # open FILE
    f = filedialog.askopenfile(parent=root, 
        mode='Ur', 
        title='Open', 
        filetypes=[("PianoScript files", "*.pianoscript")])
    if f:
        with open(f.name, 'r') as f:
            fjson = json.load(f)
            try:
                if fjson['header']['app-name'] == 'pianoscript':
                    global FILE
                    FILE = fjson
                else:
                    print('ERROR: file is not a pianoscript file.')
            except:
                print('ERROR: file is not a pianoscript file or is damaged.')

        # update file_path
        global file_path
        file_path = f.name
        root.title('PianoScript - %s' % f.name)

        # run the piano-roll and print-view
        threading.Thread(target=draw_pianoroll).start()
        do_engrave('')
    
    return


def save():
    print('save')

    if file_changed == True or file_path == 'New':
        save_as()
        return
    else:
        f = open(file_path, 'w')
        f.write(json.dumps(FILE, separators=(',', ':')))
        f.close()


def save_as():
    print('save_as')

    # save FILE
    f = filedialog.asksaveasfile(parent=root, 
        mode='w', 
        filetypes=[("PianoScript files", "*.pianoscript")],
        title='Save as...',
        initialdir='~/Desktop/')
    if f:
        root.title('PianoScript - %s' % f.name)
        f = open(f.name, 'w')
        f.write(json.dumps(FILE, separators=(',', ':'), indent=2))
        f.close()

        # update file_path
        global file_path
        file_path = f.name

def quit_editor(event, thread_auto_render):
    # close thread
    #global program_is_running
    #with thread_auto_render.condition:
    thread_auto_render.program_is_running = False
    #thread_auto_render.condition.notify()
    thread_auto_render.join()

    # close program
    root.destroy()