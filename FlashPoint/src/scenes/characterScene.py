import pygame

import src.constants.Color as Color

from src.Windows.UIComponents.RectButton import RectButton
from src.Windows.UIComponents.RectLabel import RectLabel

from src.Windows.UIComponents.Scene import Scene
from src.Windows.UIComponents.Text import Text


class CharacterScene(Scene):
    def __init__(self, screen):
        self.label_grp = pygame.sprite.Group()
        Scene.__init__(self, screen)
        self._init_char_box()
        self.createLabel(0, 0, 100, 150)
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

        self._init_btn_back(60, 60, "Back")

        self._init_title_text()

    def create_butn_img(self, x, y, width, height, path):

        label = self.createLabel(x, y, width, height)
        self.label_grp.add(label)
        self.sprite_grp.add(label)

        box_size = (width, height)
        self.this_img = RectButton(x, y, box_size[0], box_size[1], path)

        # self.this_img.on_hover(label.change_color, Color.WHITE)
        # self.this_img.off_hover(label.change_color, Color.BLACK)

        self.this_img.on_click(self.click_img, label)

        self.sprite_grp.add(self.this_img)

    def _init_char_box(self):
        box_size = (self.resolution[0] / 2, self.resolution[1] / 2)
        x_pos = self.resolution[0] / 2 - box_size[0] / 2
        y_pos = self.resolution[1] / 2 - box_size[1] / 2
        log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.BLACK)
        self.sprite_grp.add(log_box)

    def _init_btn_back(self, x_pos, y_pos, text):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], Color.BLUE, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        self.sprite_grp.add(self.buttonBack)

    def _init_title_text(self):
        box_size = (400, 50)
        self.text_title = RectButton(400, 60, box_size[0], box_size[1], Color.BLACK, 0,
                                     Text(pygame.font.SysFont('Arial', 35), "Character Selection", Color.WHITE))

        self.sprite_grp.add(self.text_title)

    def createLabel(self, x_pos, y_pos, width, height):
        return RectLabel(x_pos - 15, y_pos - 15, width + 30, height + 30, Color.BLACK)

    def click_img(self, btn):
        for sprite in self.label_grp:
            if isinstance(sprite, RectLabel):
                sprite.change_color(Color.BLACK)

        if isinstance(btn, RectLabel):
            btn.change_color(Color.WHITE)
