# This file is placed in the Public Domain.
# pylint: disable=C,R,W0105,W0212,W0718


"default values"


class Default:

    def __contains__(self, key):
        return key in dir(self)

    def __getattr__(self, key):
        return self.__dict__.get(key, "")

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)


def __dir__():
    return (
        'Default',
    )
