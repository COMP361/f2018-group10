import pygame

import src.constants.color as color

from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.UIComponents.input_box import InputBox
from src.models.game_units.player_model import PlayerModel
from src.constants.change_scene_enum import ChangeSceneEnum


class LoadGame(object):

    def __init__(self, screen, current_player: PlayerModel):
        self._current_player = current_player

        self.saves = "media/save_games.json"
        self.resolution = (1280, 700)
        self.sprite_grp = pygame.sprite.Group()
        self._init_background()
        self._init_load_menu(390,100, "", color.GREY, color.GREEN)

        self._init_btn_register(((self.resolution[0] / 2) - (500 / 2)) + 400, 592, "Create Profile",
                                color.STANDARDBTN, color.BLACK)
        self._init_btn_back(20, 20, "Back", color.STANDARDBTN, color.BLACK)
        self.buttonBack.on_click(EventQueue.post, CustomEvent(ChangeSceneEnum.HOSTMENUSCENE))

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/backgrounds/flashpoint_background.png")
        self.sprite_grp.add(background_box)

    def _init_log_box(self, clr):
        box_size = (self.resolution[0] / 2, self.resolution[1] / 2)
        x_pos = self.resolution[0] / 2 - box_size[0] / 2
        y_pos = self.resolution[1] / 2 - box_size[1] / 2
        log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], clr)
        self.sprite_grp.add(log_box)

    def _init_save_elem(self, x_pos, y_pos, text, clr, color_text):
        box_size = (220, 32)

        user_box = RectButton(x_pos, y_pos, box_size[0], box_size[1], clr, 0,
                             Text(pygame.font.SysFont('Arial', 20), text, color_text))
        return user_box

    def _init_btn_register(self, x_pos, y_pos, text, clr, color_text):
        box_size = (130, 48)
        self.buttonRegister = RectButton(x_pos, y_pos, box_size[0], box_size[1], clr, 0,
                                         Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonRegister)

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: color, color_text: color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonBack)

    def _init_load_menu(self, x_pos: int, y_pos: int, text: str, color: color, color_text: color ):

        user_box = RectLabel(x_pos, y_pos, 500, 500, color, 0,
                             Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(user_box)

    @staticmethod
    def _init_text_bar(x_pos, y_pos, width, height):
        return InputBox(x=x_pos, y=y_pos, w=width, h=height)

    def draw(self, screen):
        self.sprite_grp.draw(screen)

    def update(self, event_queue):
        self.sprite_grp.update(event_queue)
