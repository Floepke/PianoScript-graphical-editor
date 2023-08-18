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

import threading
import time
import traceback

class ThreadEngraver(threading.Thread):
    def __init__(self, process, io):
        threading.Thread.__init__(self)
        self.active = True
        self.render_event = threading.Event()
        self.process = process
        self.lock = threading.Lock()
        self.io = io

    def run(self):
        while True:
            self.render_event.wait()

            if not self.active:
                break

            with self.lock:
                try:
                    self.process(self.io)
                except Exception:
                    traceback.print_exc()

            self.render_event.clear()

    def trigger_render(self):
        if self.active:
            self.render_event.set()

    def end_render(self):
        self.active = False
        self.render_event.set()
