from typing import Tuple, List

import pygame


from src.UIComponents.interactable import Interactable
from src.core.event_queue import EventQueue


class MenuWindow(object):
    """
    Popup Menu class. Simply pass in a List of Groups you wish to disable. They must be composed of Interactable objects.
    They will be disabled upon the instantiation of this object. They will be reenabled when either:
        1) this object gets garbage collected
        2) close() is called. (Delete this object()).
    """
    def __init__(self,
                 buttons_to_disable: List[pygame.sprite.Group],
                 width: int,
                 height: int,
                 position: Tuple[int, int],
                 #bg_color: Tuple[int, int, int, int] = (175, 175, 175, 0.5),
                 components: pygame.sprite.Group = None):
        """
        Constructor
        :param width: Width of the object
        :param height: Height of the object
        :param position: Defined position for the object. Optional
        :param color: Background color of the object represented by an RGB tuple (Alpha optional)
        """
        # Disable all buttons.
        self.is_closed = True  # Used to delete the menu from outside. Stupid python doesn't allow call-by-reference >:(
        self._grey = pygame.Surface((1280,700))
        self._grey.fill((64,64,64))
        self._grey.set_alpha(150)
        self._image = pygame.Surface((width, height))
        #self._bg_color = bg_color
        self.bg = pygame.image.load("src/media/GameHud/wood2.png")
        self.bg = pygame.transform.scale(self.bg,(width,height))
        self.frame = pygame.image.load("src/media/GameHud/frame.png")
        self.frame = pygame.transform.scale(self.frame,(width,height))
        self.cross = pygame.image.load("src/media/GameHud/crosss.png")
        self._rect = self._image.get_rect().move(position[0], position[1])
        self._buttons_to_disable = buttons_to_disable
        self._components: pygame.sprite.Group = components if components else pygame.sprite.Group()

    def add_component(self, component):
        component.rect.move_ip(self._rect.x, self._rect.y)
        self._components.add(component)

    def draw(self, screen):
        # alpha = self._bg_color[3] if len(self._bg_color) == 4 else 100
        #self._image.fill(self._bg_color[0])
        self._image.blit(self.bg,self._image.get_rect())
        self._image.blit(self.frame,self._image.get_rect())
        #self._image.blit(self.cross, self._image.get_rect())
        #self._components.draw(self._image)
        screen.blit(self._grey,self._grey.get_rect())
        screen.blit(self._image, self._rect)
        self._components.draw(screen)

    def update(self, event_queue: EventQueue):
        self._components.update(event_queue)

    def open(self):
        """Disable all buttons under this window."""
        self.is_closed = False
        for group in self._buttons_to_disable:
            for button in group:
                if isinstance(button, Interactable):
                    button.disable()

    #def remove_from_disable(self,component):

    def close(self):
        """Reenable all buttons under this window, and delete this object."""
        for group in self._buttons_to_disable:
            for button in group:
                if isinstance(button, Interactable):
                    button.enable()
        self.is_closed = True
