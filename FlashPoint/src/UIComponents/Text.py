from typing import Tuple
from enum import Enum

import pygame


class Text(pygame.sprite.Sprite):
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

    def __init__(self, font: pygame.font.Font, text: str, color: Tuple[int, int, int]=(0, 0, 0), anti_alias: bool=True):
        """
        Constructor.
        :param font: Defines font style. MUST BE an instance of pygame.font.Font()
        :param text: String for your Text object
        :param color: (optional) int[3] - Color for your Text object, in the form of RGB triplet. Default: black
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

    def set_font(self, font):
        self.font = font
        self.render()

    def set_text(self, text):
        self.text = text
        self.render()

    def set_color(self, color):
        self.color = color
        self.render()

    def set_center(self, rect: pygame.rect.Rect):
        self.text_rect.center = (rect.width/2, rect.height/2)

    def set_top(self, rect: pygame.rect.Rect):
        self.text_rect.top = (rect.width/2, 0)

    def set_bottom(self, rect: pygame.rect.Rect):
        self.text_rect.bottom = (rect.width/2, rect.height)

    def set_left(self, rect: pygame.rect.Rect):
        self.text_rect.left = (0, rect.height/2)

    def set_right(self, rect: pygame.rect.Rect):
        self.text_rect.right = (rect.width, rect.height/2)

    def set_pos(self, rect: pygame.rect.Rect, pos: Position):
        switcher = {
            self.Position.TOP: self.set_top(rect),
            self.Position.CENTER: self.set_center(rect),
            self.Position.BOTTOM: self.set_bottom(rect),
            self.Position.LEFT: self.set_left(rect),
            self.Position.RIGHT: self.set_right(rect)
        }
        switcher.get(pos, "Invalid argument!")
        self.render()
