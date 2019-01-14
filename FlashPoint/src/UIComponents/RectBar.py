from typing import Tuple, Optional

import pygame

from src.UIComponents.Text import Text
from src.UIComponents.Components import Components


class RectBar(pygame.sprite.Sprite, Components):
    """
    Draws a rectangular bar and sets the fill value of its content
    """
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 color: Tuple[int, ...],
                 bg_color: Tuple[int, ...],
                 outer_width: int = 2,
                 txt_obj: Optional[Text] = None,
                 txt_pos: Optional[Text.Position] = Text.Position.CENTER,
                 progress: int = 100):
        """
        Constructor
        :param x: X position of the object on screen
        :param y: Y position of the object on screen
        :param width: Width of the object
        :param height: Height of the object
        :param color: Color of the progress bar represented by an RGB tuple (Alpha optional)
        :param bg_color: Color of the background represented by an RGB tuple (Alpha optional)
        :param outer_width: Outer width of the progress bar
        :param txt_obj: Text object to be shown
        :param txt_pos: Position of the Text object
        :param progress: Progress of the object, should be between 0(%) -> 100(%)
        """
        pygame.sprite.Sprite.__init__(self)
        Components.__init__(self, x, y, width, height)
        self.outer_width = outer_width
        self.txt_obj = txt_obj
        self.txt_pos = txt_pos
        self._progress = progress
        self.color = color
        self.bg_color = bg_color
        self.image = None
        self.rect = None
        self._render()

    def progress_update(self):
        inner_width = self._progress * (self.width - 2 * self.outer_width) / 100
        inner_image = pygame.Surface([inner_width, self.height - 2 * self.outer_width])
        inner_rect = inner_image.get_rect()
        inner_rect.x = self.x + self.outer_width
        inner_rect.y = self.y + self.outer_width

        # draw the inner progress bar
        pygame.draw.rect(inner_image, self.color, inner_rect, 0)

    def _render(self):
        # TODO complete the _render func
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # draw the outer border of the bar
        pygame.draw.rect(self.image, self.bg_color, self.rect, self.outer_width)
        self.progress_update()

        if self.txt_obj:
            self.txt_obj.set_pos(self.rect, self.txt_pos)
            self.image.blit(self.txt_obj.text_surf, self.txt_obj.text_rect)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def set_progress(self, progress: int):
        self._progress = progress
        self.progress_update()

    def change_color(self, color: Tuple[int, int, int], bg_color: Tuple[int, int, int]):
        self.color = color
        self.bg_color = bg_color
        self._render()

    def change_pos(self, x: int, y: int):
        self.x(x)
        self.y(y)
        self._render()
