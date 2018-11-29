from typing import Tuple, Optional, List

import pygame

from src.Windows.UIComponents.Components import Components
from src.Windows.UIComponents.Interactable import Interactable
from src.core.EventQueue import EventQueue


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
                 bg_color: Tuple[int, int, int, int] = (175, 175, 175, 0.5),
                 components: pygame.sprite.Group = None):
        """
        Constructor
        :param width: Width of the object
        :param height: Height of the object
        :param position: Defined position for the object. Optional
        :param color: Background color of the object represented by an RGB tuple (Alpha optional)
        """
        # Disable all buttons.
        self._image = pygame.Surface((width, height))
        self._bg_color = bg_color
        self._rect = self._image.get_rect().move(position[0], position[1])
        self._buttons_to_disable = buttons_to_disable
        self._components: pygame.sprite.Group = components if components else pygame.sprite.Group()
        self._open()

    def add_component(self, component: pygame.sprite.Sprite):
        self._components.add(component)

    def draw(self, screen):
        # alpha = self._bg_color[3] if len(self._bg_color) == 4 else 100
        self._image.fill(self._bg_color[0])
        # self._image.set_alpha(alpha)
        self._components.draw(self._image)
        screen.blit(self._image, self._rect)

    def update(self, event_queue: EventQueue):
        for component_group in self._components:
            component_group.update(event_queue)

    def _open(self):
        """Disable all buttons under this window."""
        for group in self._buttons_to_disable:
            for button in group:
                if isinstance(button, Interactable):
                    button.disable()

    def close(self):
        """Reenable all buttons under this window, and delete this object."""
        for group in self._buttons_to_disable:
            for button in group:
                if isinstance(button, Interactable):
                    button.enable()
        del self
