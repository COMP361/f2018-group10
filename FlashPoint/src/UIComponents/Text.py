from typing import Tuple

import pygame


class Text(object):
    """
        Creates a text object based on your configurations.
    """

    def __init__(self, font: pygame.font.Font, text: str, color: Tuple[int, int, int]=(0, 0, 0), anti_alias: bool=True):
        """
        Constructor.
        :param font: Defines font style. MUST BE an instance of pygame.font.Font()
        :param text: String for your Text object
        :param color: (optional) int[3] - Color for your Text object, in the form of RGB triplet. Default: black
        :param anti_alias: (optional) Boolean - Anti aliasing option
        """
        self.font = font
        self.text = text
        self.color = color
        self.anti_alias = anti_alias
        pygame.init()
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

    def set_center(self, pos: Tuple[int, int]):
        self.text_rect.center = pos
        self.render()
