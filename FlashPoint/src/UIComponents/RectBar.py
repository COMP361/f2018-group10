from typing import Tuple, Optional

import pygame


class RectBar(pygame.sprite.Sprite):
    """
    Draws a rectangular bar and sets the fill value of its content
    """
    def __init__(self,
                 color: Tuple[int, int, int],
                 bgColor: Tuple[int, int, int],
                 width: int=0,
                 outerWidth: int=0):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.bgColor = bgColor
        self.width = width
        self.outerWidth = outerWidth
        self.image = None
        self.render()

    def render(self):
        # TODO complete the render func
        self.image = pygame.Surface([self.rect.width, self.rect.height])
        self.image.fill(self.color)
        if self.txtobj:
            self.txtobj.set_center((self.rect.width / 2), (self.rect.height / 2))
            self.image.blit(self.txtobj.get_surf(), self.txtobj.get_rect())
