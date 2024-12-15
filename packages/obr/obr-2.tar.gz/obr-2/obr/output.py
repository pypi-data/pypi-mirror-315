# This file is placed in the Public Domain.
# pylint: disable=C


"output cache"


import queue


from .thread import launch


class Output:

    cache = {}

    def __init__(self):
        self.oqueue = queue.Queue()

    def dosay(self, channel, txt):
        raise NotImplementedError

    def oput(self, channel, txt):
        self.oqueue.put((channel, txt))

    def output(self):
        while True:
            (channel, txt) = self.oqueue.get()
            if channel is None and txt is None:
                self.oqueue.task_done()
                break
            self.dosay(channel, txt)
            self.oqueue.task_done()

    def start(self):
        launch(self.output)

    def stop(self):
        self.oqueue.put((None, None))

    def wait(self):
        self.oqueue.join()


def __dir__():
    return (
        'Output',
    )
