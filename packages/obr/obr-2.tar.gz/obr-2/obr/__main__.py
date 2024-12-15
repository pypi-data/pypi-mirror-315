# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,C0415,R0903,R0912,R0915,W0105,W0611,W0718,E0402


"main"


import os
import readline
import sys
import termios
import time


from .client  import Client
from .command import command, parse, scan
from .errors  import errors, later
from .event   import Event
from .persist import Config
from .utils   import forever


Config.name = "obr"
Config.wdr  = os.path.expanduser(f"~/.{Config.name}")


Cfg = Config()


class CLI(Client):


    def dosay(self, channel, txt):
        self.raw(txt)

    def raw(self, txt):
        print(txt)


class Console(CLI):

    def announce(self, txt):
        self.raw(txt)


    def callback(self, evt):
        CLI.callback(self, evt)
        evt.wait()

    def poll(self):
        evt = Event()
        evt.txt = input("> ")
        evt.type = "command"
        return evt


def banner():
    tme = time.ctime(time.time()).replace("  ", " ")
    print(f"{Cfg.name.upper()} since {tme}")


def wrap(func):
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (KeyboardInterrupt, EOFError):
        print("")
    except Exception as ex:
        later(ex)
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def main():
    parse(Cfg, " ".join(sys.argv[1:]))
    from obr.mods import face
    scan(face)
    if "c" in Cfg.opts:
        if "v" in Cfg.opts:
            banner()
        if os.path.exists("mods"):
            from mods import face as face2
            scan(face2, init=True)
            if "v" in Cfg.opts:
                face.irc.output = print
        csl = Console()
        csl.start()
        forever()
    evt = Event()
    evt.type = "command"
    evt.txt = Cfg.otxt
    csl = CLI()
    command(csl, evt)
    evt.wait()


if __name__ == "__main__":
    wrap(main)
    for text in errors():
        print(text)
