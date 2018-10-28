from typing import Tuple, Optional

import pygame

from src.UIComponents.Text import Text


class EllipseLabel(pygame.sprite.Sprite):
    """
    Draws a rectangle object and (optionally) inserts a text on it.
    This is a shorthand of pygame.draw.ellipse()
    """
    def __init__(self,
                 rect: pygame.Rect,
                 color: Tuple[int, int, int],
                 txtobj: Optional[Text] = None,
                 width: int = 0):
        """
        Constructor.
        :param rect: Defines the area that the circle (ellipse) will be drawn
        :param color: RGB triplet for the background color
        :param txtobj: Text object to be inserted at the center of this label
        :param width: The thickness to draw the outer edge. If width is zero then the ellipse will be filled.
        """
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.color = color
        self.txtObj = txtobj
        self.width = width
        self.image = None

    def render(self):
        self.image = pygame.Surface([self.rect.width, self.rect.height])
        pygame.draw.ellipse(self.image, self.color, self.rect, self.width)
        if self.txtobj:
            self.txtobj.set_center((self.rect.width/2), (self.rect.height/2))
            self.image.blit(self.txtobj.get_surf(), self.txtobj.get_rect())

    def change_color(self, color: Tuple[int, int, int]):
        self.color = color
        self.render()

    def change_rect(self, rect: pygame.Rect, width: int=0):
        self.rect = rect
        self.width = width
        self.render()
