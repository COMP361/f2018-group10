from typing import Tuple, Optional, Union

import pygame

from src.UIComponents.Text import Text
from src.UIComponents.FileImporter import FileImporter
from src.UIComponents.Components import Components


class RectLabel(pygame.sprite.Sprite, Components):
    """
    Draws a rectangle object and (optionally) inserts a text on it.
    This is a shorthand of pygame.draw.rect()
    """
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 background: Union[Tuple[int, int, int], str]=(0, 0, 0),
                 outer_width: int=0,
                 txt_obj: Optional[Text]=None,
                 txt_pos: Text.Position=Text.Position.CENTER):
        """
        Constructor
        :param x: x position of the object on screen
        :param y: y position of the object on screen
        :param width: width of the object
        :param height: height of the object
        :param background: Background of the object, can be either RGB color tuples or imported image
        :param outer_width: The thickness of the outer edge. If width is zero then the object will be filled.
        :param txt_obj: Text object to be inserted at the center of this label
        :param txt_pos: Text position in the label, must be one of Text.Position
        """
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.background = background
        self.outer_width = outer_width
        self.txt_obj = txt_obj
        self.txt_pos = txt_pos
        self.image = None
        self.rect = None
        self.__render__()

    def __render__(self):
        # If self.background is an instance of Tuple, we assign that RGB tuple as the background color
        # Otherwise, self.background is an imported image (Surface) so we try to import it and assign as the background
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        if isinstance(self.background, Tuple):
            pygame.draw.rect(self.image, self.background, self.rect, self.outer_width)
        else:
            pygame.draw.rect(self.image, (0, 0, 0), self.rect, self.outer_width)
            image_file = FileImporter.import_image(self.background)
            self.image.blit(image_file, self.image)

        if self.txt_obj:
            self.txt_obj.set_pos(self.rect, self.txt_pos)
            self.image.blit(self.txt_obj.text_surf, self.txt_obj.text_rect)

    def change_color(self, color: Tuple[int, int, int]):
        self.background = color
        self.__render__()

    def change_bg_image(self, file_path: str):
        if FileImporter.file_exists(file_path):
            self.background = file_path
            self.__render__()
        else:
            raise Exception("File not found!")

    def change_rect(self, rect: pygame.Rect, width: int=0):
        self.rect = rect
        self.width = width
        self.__render__()

    def change_pos(self, x: int, y: int):
        self.x = x
        self.y = y
        self.__render__()

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
