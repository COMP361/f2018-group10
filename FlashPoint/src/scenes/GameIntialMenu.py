import pygame

import src.constants.Color as Color

from src.UIComponents.RectButton import RectButton
from src.UIComponents.RectLabel import RectLabel
from src.UIComponents.Text import Text
from src.UIComponents.Scene import Scene


class CreateGameMenu(Scene):
    def __init__(self, screen):
        Scene.__init__(self, screen)
        self._init_background()

        self._init_text_box(344, 387, 200, 32, "Choose Game Mode:", Color.STANDARDBTN, Color.BLACK)
        self._init_btn_back(20, 20, "Back", Color.STANDARDBTN, Color.BLACK)
        self._init_btn_family(575, 381, "Family", Color.STANDARDBTN, Color.BLACK)
        self._init_btn_exp(741, 381, "Experienced", Color.STANDARDBTN, Color.BLACK)

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/Backgrounds/FlashpointBackGround.png")
        self.sprite_grp.add(background_box)

    def _init_text_box(self, x_pos, y_pos, w, h, text, color, color_text):
        box_size = (w, h)

        user_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                             Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(user_box)

    def _init_btn_family(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonFamily = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                       Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonFamily)

    def _init_btn_exp(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonExp = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                    Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonExp)

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonBack)
