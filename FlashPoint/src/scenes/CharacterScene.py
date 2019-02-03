import pygame

import src.constants.Color as Color

from src.UIComponents.RectButton import RectButton
from src.UIComponents.RectLabel import RectLabel

from src.UIComponents.Scene import Scene
from src.UIComponents.Text import Text


class CharacterScene(Scene):
    def __init__(self, screen):
        self.label_grp = pygame.sprite.Group()

        Scene.__init__(self, screen)
        self._init_background()
        self.createLabel(0, 0, 100, 150)
        self.create_butn_img(30, 80, 200, 302,
                             "media/spec_card/Cafs_Firefighter.png")

        self.create_butn_img(280, 80, 200, 302,
                             "media/spec_card/Driver_Operator.png")

        self.create_butn_img(530, 80, 200, 302,
                             "media/spec_card/Fire_Captain.png")

        self.create_butn_img(780, 80, 200, 302,
                             "media/spec_card/Generalist.png")

        self.create_butn_img(1030, 80, 200, 302,
                             "media/spec_card/Hazmat_Technician.png")

        self.create_butn_img(30, 420, 200, 302,
                             "media/spec_card/Imaging_Technician.png")

        self.create_butn_img(280, 420, 200, 302,
                             "media/spec_card/Parademic.png")

        self.create_butn_img(530, 420, 200, 302,
                             "media/spec_card/Rescue_Specialist.png")

        self._init_btn_back(20, 20, "Back", Color.STANDARDBTN, Color.BLACK)

        self._init_btn_confirm(1050, 575, "Confirm", Color.STANDARDBTN, Color.BLACK)

        self._init_title_text()

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/Backgrounds/FlashpointBackGround.png")
        self.sprite_grp.add(background_box)

    def create_butn_img(self, x, y, width, height, path):

        label = self.createLabel(x, y, width, height)
        self.label_grp.add(label)
        self.sprite_grp.add(label)

        box_size = (width, height)
        self.this_img = RectButton(x, y, box_size[0], box_size[1], path)

        self.this_img.on_click(self.click_img, label)

        self.sprite_grp.add(self.this_img)

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonBack)

    def _init_title_text(self):
        box_size = (400, 50)
        self.text_title = RectButton(400, 10, box_size[0], box_size[1], Color.BLACK, 0,
                                     Text(pygame.font.SysFont('Arial', 35), "Character Selection", Color.WHITE))

        self.sprite_grp.add(self.text_title)

    def _init_btn_confirm(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonConfirm = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                        Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonConfirm)

    def createLabel(self, x_pos, y_pos, width, height):
        return RectLabel(x_pos - 15, y_pos - 15, width + 30, height + 30, Color.BLACK)

    def click_img(self, btn):
        for sprite in self.label_grp:
            if isinstance(sprite, RectLabel):
                sprite.change_color(Color.BLACK)

        if isinstance(btn, RectLabel):
            btn.change_color(Color.WHITE)
