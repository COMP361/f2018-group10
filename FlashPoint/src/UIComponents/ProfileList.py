from typing import Tuple, Optional, Union

import pygame

from src.UIComponents.FileImporter import FileImporter
from src.UIComponents.Components import Components
from src.UIComponents.RectButton import RectButton
from src.UIComponents.Text import Text
import src.constants.Color as Color


class ProfileList(pygame.sprite.Sprite, Components):
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 limit: int = 3,
                 background: Union[Tuple[int, int, int], str] = (0, 0, 0),
                 outer_width: int = 0):
        pygame.sprite.Sprite.__init__(self)
        Components.__init__(self, x, y, width, height)
        self._limit = limit
        self.background = background
        self.outer_width = outer_width
        self.image = None
        self.rect = None
        self._list = []
        self._render()

    def _render(self):
        # If self.background is an instance of Tuple, we assign that RGB tuple as the background color
        # Otherwise, self.background is an imported image (Surface) so we try to import it and assign as the background
        self.image = pygame.Surface([self.width, self.height])

        self.rect = self.image.get_rect()

        if isinstance(self.background, Tuple):
            self.rect = pygame.draw.rect(self.image, self.background, self.rect, self.outer_width)
        else:
            self.rect = pygame.draw.rect(self.image, (0, 0, 0), self.rect, self.outer_width)
            image_file = FileImporter.import_image(self.background)
            image_file = pygame.transform.scale(image_file, (self.width, self.height))
            self.image.blit(image_file, (0, 0))

        self.rect.x = self.x
        self.rect.y = self.y

        profile_list = None
        if self.can_remove:
            profile_list = pygame.sprite.Group
            # margin between two buttons
            margin = 10
            index = len(self._list)
            width = (self.width / self._limit) - margin
            height = self.height - 40
            origin_x = self.x
            origin_y = self.y

            for name in self._list:
                # draw the profile button for each profile
                x = origin_x + ((width + margin) * index) + (margin/2)
                y = origin_y + 20

                btn = RectButton(x, y, width, height, (0, 0, 0), 0,
                                 Text(pygame.font.SysFont('Arial', 20), name, Color.BLACK))
                btn.add(profile_list)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def add(self, name: str):
        if self.can_add:
            self._list.append(name)
        else:
            raise OverflowError("Limit exceeded")

    def change_color(self, color: Tuple[int, int, int]):
        self.background = color
        self._render()

    def change_bg_image(self, file_path: str):
        if FileImporter.file_exists(file_path):
            self.background = file_path
            self._render()
        else:
            raise Exception("File not found!")

    def change_rect(self, rect: pygame.Rect, outer_width: int = 0):
        self.rect = rect
        self.outer_width = outer_width
        self._render()

    def change_pos(self, x: int, y: int):
        self.x(x)
        self.y(y)
        self._render()

    @property
    def can_add(self):
        return len(self._list) <= self._limit

    @property
    def can_remove(self):
        return len(self._list) > 0
