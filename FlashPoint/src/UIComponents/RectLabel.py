from typing import Tuple, Optional

import pygame

from src.UIComponents.Text import Text


class RectLabel(pygame.sprite.Sprite):
    """
    Draws a rectangle object and (optionally) inserts a text on it.
    This is a shorthand of pygame.draw.rect()
    """
    def __init__(self,
                 rect: pygame.Rect,
                 color: Tuple[int, int, int],
                 txtobj: Optional[Text] = None,
                 width: int=0):
        """
        Constructor.
        :param rect: Rect object to be drawn
        :param color: RGB triplet for the background color
        :param txtobj: Text object to be inserted at the center of this label
        :param width: Outer width of the Rect object (to be drawn)
        """
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.color = color
        self.width = width
        self.txtobj = txtobj
        self.image = None
        self.render()

    def render(self):
        self.image = pygame.Surface([self.rect.width, self.rect.height])
        self.image.fill(self.color)
        if self.txtobj:
            self.txtobj.set_center((self.rect.width/2), (self.rect.height/2))
            self.image.blit(self.txtobj.text_surf, self.txtobj.text_rect)

    def change_color(self, color: Tuple[int, int, int]):
        self.color = color
        self.render()

    def change_rect(self, rect: pygame.Rect, width: int=0):
        self.rect = rect
        self.width = width
        self.render()
