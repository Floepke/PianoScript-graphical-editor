# ------------------
# RENDER MANAGEMENT
# ------------------
'''
    This section takes care for auto rendering
    the score in a thread.
'''
import threading

def do_engrave(event='dummy'):
    with thread_auto_render.condition:
        thread_auto_render.needs_to_render = True
        thread_auto_render.condition.notify()


class QuitThread(Exception):
    pass


class AutoRender(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.program_is_running = True
        self.needs_to_render = False
        self.condition = threading.Condition()

    def run(self):
        try:
            while True:
                self.wait_and_render()
        except QuitThread:
            pass

    def wait_and_render(self):
        with self.condition:
            if not self.program_is_running:
                raise QuitThread
            while not self.needs_to_render:
                self.condition.wait()
                if not self.program_is_running:
                    raise QuitThread
            self.needs_to_render = False
        try:
            engrave()
        except Exception:
            traceback.print_exc()