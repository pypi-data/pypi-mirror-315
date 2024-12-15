# This file is placed in the Public Domain.
# pylint: disable=C,R,W0105,W0212,W0718


"events"


import threading


from .default import Default


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready = threading.Event()
        self._thr   = None
        self.result = []
        self.type   = "event"
        self.txt    = ""

    def __str__(self):
        return str(self.__dict__)

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self.result.append(txt)

    def wait(self):
        self._ready.wait()
        if self._thr:
            self._thr.join()



def __dir__():
    return (
        'Event',
    )
