from typing import Tuple, Optional
from enum import Enum

import pygame

from src.Windows.UIComponents.Components import Components


class Text(pygame.sprite.Sprite, Components):
    """
        Creates a text object based on your configurations.
    """

    class Position(Enum):
        """
        Sub class for text position
        """
        TOP = 0
        CENTER = 1
        BOTTOM = 2
        LEFT = 3
        RIGHT = 4

    def __init__(self,
                 font: pygame.font.Font,
                 text: str,
                 color: Tuple[int, int, int, Optional[int]]=(0, 0, 0),
                 anti_alias: bool=True):
        """
        Constructor.
        :param font: Defines font style. MUST BE an instance of pygame.font.Font()
        :param text: String for your Text object
        :param color: Color for your Text object, in the form of RGB triplet. Alpha is optional. Default: black
        :param anti_alias: (optional) Boolean - Anti aliasing option
        """
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.text = text
        self.color = color
        self.anti_alias = anti_alias
        self.text_surf = None
        self.text_rect = None
        self.render()

    def render(self):
        self.text_surf = self.font.render(self.text, self.anti_alias, self.color)
        self.text_rect = self.text_surf.get_rect()

    def set_font(self, font: pygame.font.Font):
        self.font = font
        self.render()

    def set_text(self, text: str):
        self.text = text
        self.render()

    def set_color(self, color: Tuple[int, int, int, int, Optional[int]]):
        self.color = color
        self.render()

    # TODO: fix the freaking coordinates
    def set_center(self, rect: pygame.rect.Rect):
        self.text_rect.center = (rect.x + rect.width/2, rect.y + rect.height/2)
        print(self.text_rect)

    def set_top(self, rect: pygame.rect.Rect):
        self.text_rect.top = (rect.x + rect.width/2, rect.y)

    def set_bottom(self, rect: pygame.rect.Rect):
        self.text_rect.bottom = (rect.x + rect.width/2, rect.y + rect.height)

    def set_left(self, rect: pygame.rect.Rect):
        self.text_rect.left = (rect.x, rect.y + rect.height/2)

    def set_right(self, rect: pygame.rect.Rect):
        self.text_rect.right = (rect.x + rect.width, rect.y + rect.height/2)

    def set_pos(self, rect: pygame.rect.Rect, pos: Position):
        if pos is self.Position.TOP:
            self.set_top(rect),
        elif pos is self.Position.CENTER:
            self.set_center(rect)
        elif pos is self.Position.BOTTOM:
            self.set_bottom(rect)
        elif pos is self.Position.LEFT:
            self.set_left(rect)
        elif pos is self.Position.RIGHT:
            self.set_right(rect)
        self.render()

    def get_height(self):
        return self.text_rect.height

    def get_width(self):
        return self.text_rect.width
