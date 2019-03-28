import pygame


class EventQueue(object):
    """
    Class for storing the Event Queue from pygame. It gets emptied while accessing it, so we need to keep it.
    !!!!!!!IMPORTANT: ANY TIME WE NEED TO ACCESS THE EVENT QUEUE, ACCESS THIS INSTEAD!!!!!!!!!!!!
    """
    _instance = None

    def __init__(self):
        if not EventQueue._instance:
            EventQueue._instance = EventQueue.EventQueueInner()
        else:
            raise Exception("Tried to instantiate singleton EventQueue twice")

    @staticmethod
    def get_instance():
        if not EventQueue._instance:
            EventQueue()
        return EventQueue._instance

    @staticmethod
    def block():
        """Block the event queue from being flushed"""
        EventQueue.get_instance().blocked = True

    @staticmethod
    def unblock():
        EventQueue.get_instance().blocked = False

    @staticmethod
    def post(event):
        EventQueue.get_instance().post(event)

    @staticmethod
    def fill_queue():
        EventQueue.get_instance().fill_queue()

    @staticmethod
    def flush_queue():
        EventQueue.get_instance().flush_queue()

    @staticmethod
    def __iter__():
        return EventQueue.get_instance().__iter__()

    class EventQueueInner(object):
        def __init__(self):
            self._events = []
            self.blocked = False

        def fill_queue(self):
            """Copy the pygame event queue into this object."""
            if not self.blocked:
                self._events += pygame.event.get()

        def post(self, event):
            self._events.append(event)

        def flush_queue(self):
            """Empty this event queue."""
            if not self.blocked:
                self._events = []

        def __iter__(self):
            """Iterator so you can loop through this class"""
            return iter(self._events)
