import pygame

import src.constants.Color as Color
from src.Windows.UIComponents.RectButton import RectButton
from src.Windows.UIComponents.RectLabel import RectLabel
from src.Windows.UIComponents.Text import Text
from src.Windows.UIComponents.Scene import Scene


class JoinScene(object):
    def __init__(self, screen):
        self.scene = Scene.__init__(screen)
        self._init_log_box()
        self._init_text_box(342, 250, "Enter IP:")

        # self._init_text_bar()

        self._init_btn(575, 436, "Connect")
        self._init_btn_back(100, 100, "Back")

    def draw(self):
        self.scene.sprite_grp.draw()

    def update(self):
        self.scene.sprite_grp.update()

    def _init_log_box(self):
        box_size = (self.scene.resolution[0] / 2, self.scene.resolution[1] / 2)
        x_pos = self.scene.resolution[0] / 2 - box_size[0] / 2
        y_pos = self.scene.resolution[1] / 2 - box_size[1] / 2
        log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.GREEN)
        self.scene.sprite_grp.add(log_box)

    def _init_text_box(self, x_pos, y_pos, text):
        box_size = (136, 32)

        user_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                             Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        self.scene.sprite_grp.add(user_box)

    def _init_btn(self, x_pos, y_pos, text):
        box_size = (130, 48)
        self.button = RectButton(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                                 Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        self.scene.sprite_grp.add(self.button)

    def _init_btn_back(self, x_pos, y_pos, text):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        self.scene.sprite_grp.add(self.buttonBack)

    def _init_text_bar(self):
        pass
