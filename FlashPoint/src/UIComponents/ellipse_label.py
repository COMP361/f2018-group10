from typing import Tuple, Optional, Union

import pygame

from src.UIComponents.text import Text
from src.UIComponents.file_importer import FileImporter
from src.UIComponents.components import Components


class EllipseLabel(pygame.sprite.Sprite, Components):
    """
    Draws a rectangle object and (optionally) inserts a text on it.
    This is a shorthand of pygame.draw.ellipse()
    """
    def __init__(self,
                 x: Union[int, float],
                 y: Union[int, float],
                 width: Union[int, float],
                 height: Union[int, float],
                 background: Union[Tuple[int, int, int], str] = (0, 0, 0),
                 outer_width: Union[int, float] = 0,
                 txt_obj: Optional[Text] = None,
                 txt_pos: Optional[Text.Position] = Text.Position.CENTER):
        """
        Constructor
        :param x: x position of the object on screen
        :param y: y position of the object on screen
        :param width: width of the object
        :param height: height of the object
        :param background: Background of the object, can be either RGB color (Alpha optional) tuples or imported image
        :param outer_width: The thickness of the outer edge. If width is zero then the object will be filled.
        :param txt_obj: Text object to be inserted at the center of this label
        :param txt_pos: Text position in the label, must be one of Text.Position
        """
        pygame.sprite.Sprite.__init__(self)
        Components.__init__(self, x, y, width, height)
        self.background = background
        self.outer_width = outer_width
        self.txt_obj = txt_obj
        self.txt_pos = txt_pos
        self.image = None
        self.rect = None
        self._render()

    def _render(self):
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        if isinstance(self.background, Tuple):
            pygame.draw.ellipse(self.image, self.background, self.rect, self.outer_width)
        else:
            self.image = self.image.convert_alpha(pygame.display.get_surface())
            self.image.fill((0, 0, 0, 0), None, pygame.BLEND_RGBA_MULT)
            image_file = FileImporter.import_image(self.background)
            self.image.blit(image_file, self.image)

        if self.txt_obj:
            self.txt_obj.set_pos(self.rect, self.txt_pos)
            self.image.blit(self.txt_obj.text_surf, self.txt_obj.text_rect)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def change_color(self, color: Tuple[int, int, int]):
        self.background = color
        self._render()

    def change_bg_image(self, file_path: str):
        if FileImporter.file_exists(file_path):
            self.background = file_path
            self._render()
        else:
            raise Exception("File not found!")

    def change_rect(self, rect: pygame.Rect, outer_width: int=0):
        self.rect = rect
        self.outer_width = outer_width
        self._render()

    def change_pos(self, x: int, y: int):
        self.x(x)
        self.y(y)
        self._render()
