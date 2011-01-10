"""Module for defining base partition manipulators."""


class Part (object):
    def __new__ (cls):
        obj = object.__new__(cls)
        return obj

    @staticmethod
    def __call__ (*args, **kws):
        raise NotImplementedError

class Repart (object):
    def __new__ (cls):
        obj = object.__new__(cls)
        return obj

    @staticmethod
    def __call__ (*args, **kws):
        raise NotImplementedError

class Fuse (object):
    def __new__ (cls):
        obj = object.__new__(cls)
        return obj

    @staticmethod
    def __call__ (*args, **kws):
        raise NotImplementedError
