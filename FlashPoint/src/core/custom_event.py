from enum import Enum


class CustomEvent(object):

    def __init__(self, type: Enum, **kwargs):
        self.type = type
        self.__dict__.update(kwargs)
