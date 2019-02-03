import pygame

import src.constants.color as color

from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.UIComponents.input_box import InputBox
from src.UIComponents.profile_list import ProfileList


class StartScene(object):
    def __init__(self, screen):
        self.resolution = (1280, 700)
        self.sprite_grp = pygame.sprite.Group()
        self._init_background()

        # self._init_text_box(342, 350, "Username:", color.STANDARDBTN, color.BLACK)
        # self._init_text_box(342, 434, "Password:", color.STANDARDBTN, color.BLACK)
        # self._init_btn_login(594, 600, "Login", color.STANDARDBTN, color.BLACK)
        # self._init_btn_register(791, 600, "Register", color.STANDARDBTN, color.BLACK)
        self._init_profile_selector(((self.resolution[0]/2)-(500/2)), 330, color.GREY)
        self._text_bar1 = self._init_text_bar(((self.resolution[0]/2)-(500/2))-20, 600, 400, 32)
        self._init_btn_register(((self.resolution[0]/2)-(500/2))+400, 592, "Create Profile",
                                color.STANDARDBTN, color.BLACK)

        # self._text_bar1 = self._init_text_bar(500, 350, 400, 32)
        # self._text_bar2 = self._init_text_bar(500, 434, 400, 32)

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/flashpoint_background.png")
        self.sprite_grp.add(background_box)

    def _init_log_box(self, clr):
        box_size = (self.resolution[0] / 2, self.resolution[1] / 2)
        x_pos = self.resolution[0] / 2 - box_size[0] / 2
        y_pos = self.resolution[1] / 2 - box_size[1] / 2
        log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], clr)
        self.sprite_grp.add(log_box)

    def _init_text_box(self, x_pos, y_pos, text, clr, color_text):
        box_size = (136, 32)

        user_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], clr, 0,
                             Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(user_box)

    # def _init_btn_login(self, x_pos, y_pos, text, color, color_text):
    #     box_size = (130, 48)
    #     self.buttonLogin = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
    #                                   Text(pygame.font.SysFont('Arial', 20), text, color_text))
    #
    #     self.sprite_grp.add(self.buttonLogin)

    def _init_btn_register(self, x_pos, y_pos, text, clr, color_text):
        box_size = (130, 48)
        self.buttonRegister = RectButton(x_pos, y_pos, box_size[0], box_size[1], clr, 0,
                                         Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonRegister)

    @staticmethod
    def _init_text_bar(x_pos, y_pos, width, height):
        return InputBox(x=x_pos, y=y_pos, w=width, h=height)

    def _init_profile_selector(self, x_pos, y_pos, clr):
        box_size = (500, 250)
        self.profile = ProfileList(x_pos, y_pos, box_size[0], box_size[1], 3, clr)

    def draw(self, screen):
        self.sprite_grp.draw(screen)
        # self._text_bar2.draw(screen)
        self._text_bar1.draw(screen)
        self.profile.draw(screen)

    def update(self, event_queue):
        self.sprite_grp.update(event_queue)
        self._text_bar1.update(event_queue)
        self.profile.update(event_queue)
        # self._text_bar2.update(event_queue)
