from typing import Tuple, Union

import pygame

from src.core.event_queue import EventQueue
from src.UIComponents.file_importer import FileImporter
from src.UIComponents.components import Components
from src.UIComponents.rect_button import RectButton
from src.UIComponents.text import Text
import src.constants.color as color


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
        self._profile_list = pygame.sprite.Group()
        self._btn_list = []
        self._init_slots()
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

        for btn in self._btn_list:
            btn._render()

    def _init_slots(self):
        # margin between two buttons
        margin = 30
        width = (self.width / self._limit) - margin
        height = self.height - 40
        for i in range(self._limit):
            # draw the profile button for each profile
            x = self.x + ((width + margin) * i) + (margin / 2)
            y = self.y + 20

            btn = RectButton(x, y, width, height, color.STANDARDBTN, 0,
                             Text(pygame.font.SysFont('Arial', 20), "Empty", color.BLACK))
            self._btn_list.append(btn)
            self._profile_list.add(btn)

    def set_profile(self, index: int, name: str, click_action: callable, *args, **kwargs):
        self._btn_list[index].txt_obj = Text(pygame.font.SysFont('Arial', 20), name, color.BLACK)
        self._btn_list[index].on_click(click_action, args, kwargs)
        self._render()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
        self._profile_list.draw(surface)

    def update(self, event_queue: EventQueue):
        self._profile_list.update(event_queue)

    def change_color(self, clr: Tuple[int, int, int]):
        self.background = clr
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
