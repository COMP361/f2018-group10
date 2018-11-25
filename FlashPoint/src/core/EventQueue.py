import pygame


class EventHandler(object):
    """
    Class for storing the Event Queue from pygame. It gets emptied while accessing it, so we need to keep it.
    !!!!!!!IMPORTANT: ANY TIME WE NEED TO ACCESS THE EVENT QUEUE, ACCESS THIS INSTEAD!!!!!!!!!!!!
    """
    def __init__(self):
        self.events = []

    def fill_queue(self):
        self.events = pygame.event.get()