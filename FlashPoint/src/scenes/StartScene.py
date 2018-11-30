import pygame

import src.constants.Color as Color

from src.Windows.UIComponents.RectButton import RectButton
from src.Windows.UIComponents.RectLabel import RectLabel
from src.Windows.UIComponents.Text import Text
from src.Windows.UIComponents.Scene import Scene
from src.Windows.UIComponents.TextBar import InputBox


class StartScene(Scene):
        def __init__(self, screen):
            Scene.__init__(self, screen)
            self._init_background()
            self._init_text_box(342, 350, "Username:", Color.STANDARDBTN,Color.BLACK)
            self._init_text_box(342, 434, "Password:", Color.STANDARDBTN,Color.BLACK)
            self._init_text_bar(500, 350, 400, 32)
            self._init_text_bar(500, 434, 400, 32)
            self._init_btn_login(594, 536, "Login", Color.STANDARDBTN,Color.BLACK)
            self._init_btn_register(791, 536, "Register", Color.STANDARDBTN,Color.BLACK)

        def _init_background(self):
            box_size = (self.resolution[0], self.resolution[1])
            background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/FlashpointBackGround.png")
            self.sprite_grp.add(background_box)

        def _init_log_box(self,color):
            box_size = (self.resolution[0] / 2, self.resolution[1] / 2)
            x_pos = self.resolution[0] / 2 - box_size[0] / 2
            y_pos = self.resolution[1] / 2 - box_size[1] / 2
            log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], color)
            self.sprite_grp.add(log_box)

        def _init_text_box(self, x_pos, y_pos, text,color,color_text):
            box_size = (136, 32)

            user_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                 Text(pygame.font.SysFont('Arial', 20), text,color_text ))
            self.sprite_grp.add(user_box)

        def _init_btn_login(self, x_pos, y_pos, text,color,color_text):
            box_size = (130, 48)
            self.buttonLogin = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                          Text(pygame.font.SysFont('Arial', 20), text, color_text))

            self.sprite_grp.add(self.buttonLogin)

        def _init_btn_register(self, x_pos, y_pos, text,color,color_text):
            box_size = (130, 48)
            self.buttonRegister = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                             Text(pygame.font.SysFont('Arial', 20), text, color_text))

            self.sprite_grp.add(self.buttonRegister)

        def _init_text_bar(self, x_pos, y_pos, width, height):
            input_box1 = InputBox(x=x_pos, y=y_pos, w=width, h=height)
            self.sprite_grp.add(input_box1)
