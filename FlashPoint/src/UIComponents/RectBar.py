from typing import Tuple, Optional

import pygame

from src.UIComponents.Text import Text


class RectBar(pygame.sprite.Sprite):
    """
    Draws a rectangular bar and sets the fill value of its content
    """
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 color: Tuple[int, int, int],
                 bg_color: Tuple[int, int, int],
                 outer_width: int = 2,
                 txt_obj: Optional[Text] = None,
                 txt_pos: Optional[Text.Position] = Text.Position.CENTER,
                 progress: int = 100):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.outer_width = outer_width
        self.txt_obj = txt_obj
        self.txt_pos = txt_pos
        self.progress = progress
        self.color = color
        self.bg_color = bg_color
        self.image = None
        self.rect = None
        self.render()

    def render(self):
        # TODO complete the render func
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # draw the outer border of the bar
        pygame.draw.rect(self.image, self.bg_color, self.rect, self.outer_width)
        inner_width = self.progress * (self.width - 2*self.outer_width)/100
        inner_image = pygame.Surface([inner_width, self.height - 2*self.outer_width])
        inner_rect = inner_image.get_rect()
        inner_rect.x = self.x + self.outer_width
        inner_rect.y = self.y + self.outer_width

        # draw the inner progress bar
        pygame.draw.rect(inner_image, self.color, inner_rect, 0)

        if self.txt_obj:
            self.txt_obj.set_pos(self.rect, self.txt_pos)
            self.image.blit(self.txt_obj.text_surf, self.txt_obj.text_rect)
