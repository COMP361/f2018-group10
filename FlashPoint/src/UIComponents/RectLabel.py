from typing import Tuple, Optional

import pygame

from src.UIComponents.Text import Text


class RectLabel(object):
    """
        Draws a rectangle object and (optionally) inserts a text on it.
        This is a shorthand of pygame.draw.Rect()
    """
    def __init__(self,
                 rect: pygame.Rect,
                 color: Tuple[int, int, int],
                 txtobj: Optional[Text] = None,
                 surface: pygame.Surface=pygame.display.get_surface(),
                 width: int=0):
        pygame.init()
        self.rect = rect
        self.color = color
        self.width = width
        self.surface = surface
        self.txtobj = txtobj
        self.render()

    def render(self):
        pygame.draw.Rect(self.surface, self.color, self.rect, self.width)
        if self.txtobj:
            self.txtobj.set_center(((self.rect.left + (self.rect.width/2)), (self.rect.top + (self.rect.height/2))))
            self.surface.blit(self.txtobj.get_surf(), self.txtobj.get_rect())

    def change_color(self, color:Tuple[int,int,int]):
        self.color = color
        self.render()

    def change_rect(self, rect: pygame.Rect, width: int=0):
        self.rect = rect
        self.width = width
        self.render()
