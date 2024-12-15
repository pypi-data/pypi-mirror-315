# This file is placed in the Public Domain.
# pylint:disable=C,W0718


"utilities"


import time
import _thread


from .errors import later


def forever():
    while True:
        try:
            time.sleep(0.1)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def spl(txt):
    try:
        result = txt.split(',')
    except (TypeError, ValueError):
        result = txt
    return [x for x in result if x]


def wrap(func):
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        pass
    except Exception as ex:
        later(ex)
