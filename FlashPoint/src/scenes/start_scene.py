import pygame

import src.constants.Color as Color

from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.UIComponents.input_box import InputBox


class StartScene(object):
    def __init__(self, screen):
        self.resolution = (1280, 700)
        self.sprite_grp = pygame.sprite.Group()
        self._init_background()

        self._init_text_box(342, 350, "Username:", Color.STANDARDBTN, Color.BLACK)
        self._init_text_box(342, 434, "Password:", Color.STANDARDBTN, Color.BLACK)
        self._init_btn_login(594, 536, "Login", Color.STANDARDBTN, Color.BLACK)
        self._init_btn_register(791, 536, "Register", Color.STANDARDBTN, Color.BLACK)

        self._text_bar1 = self._init_text_bar(500, 350, 400, 32)
        self._text_bar2 = self._init_text_bar(500, 434, 400, 32)

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/flashpoint_background.png")
        self.sprite_grp.add(background_box)

    def _init_log_box(self, color):
        box_size = (self.resolution[0] / 2, self.resolution[1] / 2)
        x_pos = self.resolution[0] / 2 - box_size[0] / 2
        y_pos = self.resolution[1] / 2 - box_size[1] / 2
        log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], color)
        self.sprite_grp.add(log_box)

    def _init_text_box(self, x_pos, y_pos, text, color, color_text):
        box_size = (136, 32)

        user_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                             Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(user_box)

    def _init_btn_login(self, x_pos, y_pos, text, color, color_text):
        box_size = (130, 48)
        self.buttonLogin = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                      Text(pygame.font.SysFont('Arial', 20), text, color_text))

        self.sprite_grp.add(self.buttonLogin)

    def _init_btn_register(self, x_pos, y_pos, text, color, color_text):
        box_size = (130, 48)
        self.buttonRegister = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                         Text(pygame.font.SysFont('Arial', 20), text, color_text))

        self.sprite_grp.add(self.buttonRegister)

    def _init_text_bar(self, x_pos, y_pos, width, height):
        return InputBox(x=x_pos, y=y_pos, w=width, h=height)

    def draw(self, screen):
        self.sprite_grp.draw(screen)
        self._text_bar2.draw(screen)
        self._text_bar1.draw(screen)

    def update(self, event_queue):
        self.sprite_grp.update(event_queue)
        self._text_bar1.update(event_queue)
        self._text_bar2.update(event_queue)
