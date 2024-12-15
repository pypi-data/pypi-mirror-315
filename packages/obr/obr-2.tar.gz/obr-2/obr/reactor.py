# This file is placed in the Public Domain.
# pylint: disable=C,R,W0105,W0212,W0718


"reactor"


import queue
import threading
import _thread


from .errors import later
from .thread import launch


class Reactor:

    def __init__(self):
        self.cbs      = {}
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()

    def callback(self, evt):
        func = self.cbs.get(evt.type, None)
        if func:
            try:
                evt._thr = launch(func, self, evt)
            except Exception as ex:
                evt._ex = ex
                later(ex)

    def loop(self):
        while not self.stopped.is_set():
            try:
                evt = self.poll()
                if not self.stopped.is_set():
                    self.callback(evt)
            except (KeyboardInterrupt, EOFError):
                if "ready" in dir(evt):
                    evt.ready()
                _thread.interrupt_main()
                
    def poll(self):
        if not self.stopped.is_set():
            return self.queue.get()

    def put(self, evt):
        self.queue.put(evt)

    def register(self, typ, cbs):
        self.cbs[typ] = cbs

    def start(self):
        launch(self.loop)

    def stop(self):
        self.stopped.set()


def __dir__():
    return (
        'Reactor',
    )
