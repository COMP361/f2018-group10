import pygame

import src.constants.Color as Color
from src.Windows.UIComponents.RectButton import RectButton
from src.Windows.UIComponents.RectLabel import RectLabel
from src.Windows.UIComponents.Text import Text


class StartScene(object):
    def __init__(self, screen):
        self.screen = screen
        self.label_grp = pygame.sprite.Group()
        self.info_object = pygame.display.Info()

        self.resolution = (self.info_object.current_w, self.info_object.current_h)

        self._init_log_box()
        self._init_text_box(342, 250, "Username:")
        self._init_text_box(342, 334, "Password:")
        self._init_text_bar()

        self._init_btn(594, 436, "Login")
        self._init_btn(791, 436, "Register")

    def draw(self):
        self.label_grp.draw(self.screen)

    def update(self):
        self.label_grp.update()

    def _init_log_box(self):
        box_size = (self.resolution[0] / 2, self.resolution[1] / 2)
        x_pos = self.resolution[0] / 2 - box_size[0] / 2
        y_pos = self.resolution[1] / 2 - box_size[1] / 2
        log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.GREEN)
        self.label_grp.add(log_box)

    def _init_text_box(self, x_pos, y_pos, text):
        box_size = (136, 32)

        user_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                             Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        self.label_grp.add(user_box)

    def _init_btn(self, x_pos, y_pos, text):
        box_size = (130, 48)
        button = RectButton(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                            Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        self.label_grp.add(button)

    def _init_text_bar(self):
        pass
