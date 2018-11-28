import pygame

import src.constants.Color as Color

from src.Windows.UIComponents.RectButton import RectButton
from src.Windows.UIComponents.RectLabel import RectLabel
from src.Windows.UIComponents.Text import Text
from src.Windows.UIComponents.Scene import Scene
from src.Windows.UIComponents.TextBar import InputBox


class LobbyScene(Scene):
    def __init__(self, screen):
        Scene.__init__(self, screen)

        # self._init_log_box()
        self._init_text_box(100, 314, "Player1")
        self._init_text_box(400, 239, "Player2")
        self._init_text_box(780, 239, "Player3")
        self._init_text_box(1080, 314, "Player4")
        self._init_btn_login(1000, 525, "Select Character")
        self._init_btn_back(100, 100, "Exit")

    def create_butn_img(self, x, y, width, height, path):
        box_size = (width, height)
        self.this_img = RectButton(x, y, box_size[0], box_size[1], path)

        self.sprite_grp.add(self.this_img)

    def _init_log_box(self):
        box_size = (self.resolution[0] / 2, self.resolution[1] / 2)
        x_pos = self.resolution[0] / 2 - box_size[0] / 2
        y_pos = self.resolution[1] / 2 - box_size[1] / 2
        log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.GREEN)
        self.sprite_grp.add(log_box)

    def _init_text_box(self, x_pos, y_pos, text):
        box_size = (100, 32)

        user_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                             Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        self.sprite_grp.add(user_box)

    def _init_btn_login(self, x_pos, y_pos, text):
        box_size = (130, 48)
        self.buttonLogin = RectButton(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                                      Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))

        self.sprite_grp.add(self.buttonLogin)

    def _init_btn_register(self, x_pos, y_pos, text):
        box_size = (130, 48)
        self.buttonRegister = RectButton(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                                         Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))

        self.sprite_grp.add(self.buttonRegister)

    def _init_btn_back(self, x_pos, y_pos, text):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        self.sprite_grp.add(self.buttonBack)
