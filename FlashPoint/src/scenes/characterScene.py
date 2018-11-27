import pygame

import src.constants.Color as Color

from src.Windows.UIComponents.RectButton import RectButton
from src.Windows.UIComponents.RectLabel import RectLabel

from src.Windows.UIComponents.Scene import Scene


class CharacterScene(Scene):
    def __init__(self, screen):
        Scene.__init__(self, screen)
        self._init_char_box()
        self.create_butn_img(250, 150, 99, 150,
                             "media/cafs_firefighter.png")

        self.create_butn_img(450, 150, 100, 150,
                             "media/driver_operator.png")

        self.create_butn_img(650, 150, 100, 150,
                             "media/fire_captain.png")

        self.create_butn_img(850, 150, 99, 150,
                             "media/generalist.png")

        self.create_butn_img(250, 450, 100, 150,
                             "media/hazmat_tech.png")

        self.create_butn_img(450, 450, 99, 150,
                             "media/imaging_tech.png")

        self.create_butn_img(650, 450, 99, 150,
                             "media/paramedic.png")

        self.create_butn_img(850, 450, 98, 150,
                             "media/rescue.png")

    def create_butn_img(self, x, y, width, height, path):
        box_size = (width, height)
        self.this_img = RectButton(x, y, box_size[0], box_size[1], path)

        self.sprite_grp.add(self.this_img)

    def _init_char_box(self):
        box_size = (self.resolution[0] / 2, self.resolution[1] / 2)
        x_pos = self.resolution[0] / 2 - box_size[0] / 2
        y_pos = self.resolution[1] / 2 - box_size[1] / 2
        log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.BLACK)
        self.sprite_grp.add(log_box)
