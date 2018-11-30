import pygame

import src.constants.Color as Color
from src.Windows.UIComponents.RectButton import RectButton
from src.Windows.UIComponents.RectLabel import RectLabel
from src.Windows.UIComponents.Text import Text
from src.Windows.UIComponents.Scene import Scene
from src.Windows.UIComponents.InputBox import InputBox


class JoinScene(Scene):
    def __init__(self, screen):
        Scene.__init__(self, screen)
        self._init_log_box()
        self._init_text_box(342, 250, "Enter IP:")
        self._init_text_bar(500, 250, 400, 32)
        self._init_btn(575, 436, "Connect")
        self._init_btn_back(100, 100, "Back")

    def _init_log_box(self):
        box_size = (self.resolution[0] / 2, self.resolution[1] / 2)
        x_pos = self.resolution[0] / 2 - box_size[0] / 2
        y_pos = self.resolution[1] / 2 - box_size[1] / 2
        log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.GREEN)
        self.sprite_grp.add(log_box)

    def _init_text_box(self, x_pos, y_pos, text):
        box_size = (136, 32)

        user_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                             Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        self.sprite_grp.add(user_box)

    def _init_btn(self, x_pos, y_pos, text):
        box_size = (130, 48)
        self.button = RectButton(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                                 Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        self.sprite_grp.add(self.button)

    def _init_btn_back(self, x_pos, y_pos, text):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        self.sprite_grp.add(self.buttonBack)

    def _init_text_bar(self,x_pos,y_pos,width,height):
        input_box1 = InputBox(x=x_pos, y=y_pos, w= width, h= height)
        self.sprite_grp.add(input_box1)
