import pygame

import src.constants.Color as Color
from src.Windows.UIComponents.RectButton import RectButton
from src.Windows.UIComponents.RectLabel import RectLabel
from src.Windows.UIComponents.Text import Text
from src.Windows.UIComponents.Scene import Scene


class HostMenuScene(Scene):
    def __init__(self, screen):
        Scene.__init__(self, screen)

        self._init_log_box()
        self._init_btn1(575, 381, "New Game")
        self._init_btn2(575, 271, "Load Existing Game")
        self._init_btn_back(100, 100, "Back")

    def _init_log_box(self):
        box_size = (self.resolution[0] / 2, self.resolution[1] / 2)
        x_pos = self.resolution[0] / 2 - box_size[0] / 2
        y_pos = self.resolution[1] / 2 - box_size[1] / 2
        log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.GREEN)
        self.sprite_grp.add(log_box)

    def _init_btn1(self, x_pos, y_pos, text):
        box_size = (130, 48)
        self.button1 = RectButton(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                            Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        self.sprite_grp.add(self.button1)

    def _init_btn2(self, x_pos, y_pos, text):
        box_size = (130, 48)
        self.button2 = RectButton(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                                 Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        self.sprite_grp.add(self.button2)

    def _init_btn_back(self, x_pos, y_pos, text):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        self.sprite_grp.add(self.buttonBack)
