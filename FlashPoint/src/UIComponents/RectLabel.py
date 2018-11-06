from typing import Tuple, Optional, Union

import pygame

from src.UIComponents.Text import Text
from src.UIComponents.FileImporter import FileImporter


class RectLabel(pygame.sprite.Sprite):
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
                 txt_obj: Optional[Text]=None,
                 txt_pos: Optional[Text.Position]=Text.Position.CENTER):
        """
        Constructor
        :param x: x position of the object on screen
        :param y: y position of the object on screen
        :param width: width of the object
        :param height: height of the object
        :param background: Background of the object, can be either RGB color tuples or imported image
        :param txt_obj: Text object to be inserted at the center of this label
        :param txt_pos: Text position in the label, must be one of Text.Position
        """
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.background = background
        self.txt_obj = txt_obj
        self.txt_pos = txt_pos
        self.image = None
        self.rect = None
        self.render()

    def render(self):
        # If self.background is an instance of Tuple, we assign that RGB tuple as the background color
        # Otherwise, self.background is an imported image (Surface) so we try to import it and assign as the background

        self.image = pygame.Surface([self.width, self.height])
        if isinstance(self.background, Tuple):
            self.image.fill(self.background)
        else:
            image_file = FileImporter.import_image(self.background)
            self.image.blit(image_file, self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        if self.txt_obj:
            self.txt_obj.set_pos(self.rect, self.txt_pos)
            self.image.blit(self.txt_obj.text_surf, self.txt_obj.text_rect)

    def change_color(self, color: Tuple[int, int, int]):
        self.background = color
        self.render()

    def change_bg_image(self, file_path: str):
        if FileImporter.file_exists(file_path):
            self.background = file_path
            self.render()
        else:
            raise Exception("File not found!")

    def change_rect(self, rect: pygame.Rect, width: int=0):
        self.rect = rect
        self.width = width
        self.render()
