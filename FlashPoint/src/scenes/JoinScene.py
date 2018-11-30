import pygame

import src.constants.Color as Color
from src.Windows.UIComponents.RectButton import RectButton
from src.Windows.UIComponents.RectLabel import RectLabel
from src.Windows.UIComponents.Text import Text
from src.Windows.UIComponents.Scene import Scene
from src.Windows.UIComponents.InputBox import InputBox


class JoinScene(object):
    def __init__(self, screen):

        self.resolution = (1280, 700)
        self.sprite_grp = pygame.sprite.Group()
        self._init_background()
        self._init_text_box(342, 350, "Enter IP:", Color.STANDARDBTN, Color.BLACK)
        self._init_text_bar(500, 350, 400, 32)
        self._init_btn(575, 536, "Connect", Color.STANDARDBTN, Color.BLACK)
        self._init_btn_back(20, 20, "Back", Color.STANDARDBTN, Color.BLACK)
        self._text_bar = self._init_text_bar(500, 350, 400, 32)

    def _init_text_box(self, x_pos, y_pos, text, color: Color, color_text: Color):
        box_size = (136, 32)

        user_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                             Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(user_box)

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/FlashpointBackGround.png")
        self.sprite_grp.add(background_box)

    def _init_btn(self, x_pos, y_pos, text, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonConnect = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                        Text(pygame.font.SysFont('Arial', 20), text, color_text))

        self.sprite_grp.add(self.buttonConnect)

    def _init_text_bar(self, x_pos, y_pos, width, height):
        return InputBox(x=x_pos, y=y_pos, w=width, h=height)

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonBack)

    def draw(self, screen):
        self.sprite_grp.draw(screen)
        self._text_bar.draw(screen)


    def update(self, event_queue):
        self.sprite_grp.update(event_queue)
        self._text_bar.update(event_queue)
