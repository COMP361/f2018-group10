import pygame


class EventQueue(object):
    """
    Class for storing the Event Queue from pygame. It gets emptied while accessing it, so we need to keep it.
    !!!!!!!IMPORTANT: ANY TIME WE NEED TO ACCESS THE EVENT QUEUE, ACCESS THIS INSTEAD!!!!!!!!!!!!
    """
    def __init__(self):
        self._events = []

    def fill_queue(self):
        """Copy the pygame event queue into this object."""
        self._events = pygame.event.get()

    def flush_queue(self):
        """Empty this event queue."""
        self._events = []

    def __iter__(self):
        """Iterator so you can loop through this class"""
        return iter(self._events)
