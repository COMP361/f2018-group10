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
        self._remove_btn_list = []
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
            # Not ideal but the only way I know to re-render
            btn._render()

    def _init_slots(self):
        """
        Initialize the profile slots
        :return:
        """
        # margin between two buttons
        margin = 30
        width = (self.width / self._limit) - margin
        height = self.height - 40
        for i in range(self._limit):
            # draw the profile button for each profile
            x = self.x + ((width + margin) * i) + (margin / 2)
            y = self.y + 20

            btn = RectButton(x, y, width, height, color.STANDARDBTN, 0,
                             Text(pygame.font.SysFont('Agency FB', 20), "Empty", color.BLACK))
            remove_btn = RectButton(btn.x, (btn.y + self.height-80)+10, btn.width, 30, color.YELLOW, 0,
                                    Text(pygame.font.SysFont('Agency FB', 16), "Remove", color.BLACK))
            self._remove_btn_list.append(remove_btn)
            self._btn_list.append(btn)
            self._profile_list.add(btn)

    def set_profile(self, index: int, name: str, click_action: callable, *args, **kwargs):
        """
        Set the name for the profile slot and assign callbacks to it
        :param index: Index of the profile slot (0-2)
        :param name: Name of the profile
        :param click_action: Click callback
        :param args:
        :param kwargs:
        :return:
        """
        if 0 <= index <= self._limit:
            height = self.height - 80
            btn = self._btn_list[index]
            rect = pygame.rect.Rect(btn.x, btn.y, btn.width, height)
            btn.change_rect(rect)
            btn.txt_obj = Text(pygame.font.SysFont('Agency FB', 20), name, color.BLACK)
            btn.on_click(click_action, *args, **kwargs)
            btn.enable()
            self._profile_list.add(self._remove_btn_list[index])
            self._render()
        else:
            raise IndexError("Index out of range")

    def remove_profile(self, index: int):
        """
        Remove the player profile
        :param index: Index of the profile slot (0-2)
        :return:
        """
        if 0 <= index < len(self._btn_list):
            height = self.height - 40
            btn = self._btn_list[index]
            rect = pygame.rect.Rect(btn.x, btn.y, btn.width, height)
            btn.change_rect(rect)
            btn.txt_obj = Text(pygame.font.SysFont('Agency FB', 20), "Empty", color.BLACK)
            btn.disable()
            self._profile_list.remove(self._remove_btn_list[index])
            self._render()
        else:
            raise IndexError("Index out of range")

    def remove_profile_callback(self, index: int, callback: callable, *args, **kwargs):
        """
        Set the callback when removing profile
        :param index: Index of the profile slot (0-2)
        :param callback: Callback for this action
        :param args:
        :param kwargs:
        :return:
        """
        if 0 <= index < len(self._btn_list):
            self._remove_btn_list[index].on_click(self.remove_profile_action, index, callback, *args, **kwargs)
        else:
            raise IndexError("Index out of range")

    def remove_profile_action(self, index: int, callback: callable, *args, **kwargs):
        #self.remove_profile(index)
        callback(*args, **kwargs)
        self.remove_profile(index)

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
