from enum import Enum


class CustomEvent(object):
    """
    This class defines a custom pygame event. These get passed to the EventQueue, to be picked up by any class
    that accesses the queue.

    Mostly used for switching scenes without causing circular imports.
    """
    def __init__(self, type: Enum,*args, **kwargs):
        self.args = args
        self.type = type
        self.__dict__.update(kwargs)
