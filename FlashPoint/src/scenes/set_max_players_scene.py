import pygame

import src.constants.color as Color
from src.core.networking import Networking
from src.constants.change_scene_enum import ChangeSceneEnum
from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.constants.media_constants import WOOD, FRAME, FLASHPOINT_BACKGROUND


class SetMaxPlayers(object):
    def __init__(self, screen, current_player: PlayerModel):
        self.game_kind = GameStateModel.instance().rules
        self.sprite_grp = pygame.sprite.Group()
        self._current_player = current_player
        self.resolution = (1280, 700)

        self._init_background()
        self._init_title_text()
        #self._init_back_box((int)(1280/2-250), 130, "", Color.GREY, Color.GREEN)

        # COMMENT THIS OUT LATER
        self._init_solo(410, 400, "I'm alone :'(", Color.STANDARDBTN, Color.GREEN2)
        self._init_duo(740, 400, "Duo :'(", Color.STANDARDBTN, Color.GREEN2)
        self._init_button3(410, 200, "3", Color.STANDARDBTN, Color.GREEN2)
        self._init_button4(740, 200, "4", Color.STANDARDBTN, Color.GREEN2)
        self._init_button5(410, 300, "5", Color.STANDARDBTN, Color.GREEN2)
        self._init_button6(740, 300, "6", Color.STANDARDBTN, Color.GREEN2)
        self._init_btn_back(20, 20, "Back", Color.STANDARDBTN, Color.GREEN2)

    def _init_back_box(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        user_box = RectLabel(x_pos, y_pos, 500, 500, color, 0,
                             Text(pygame.font.SysFont('Agency FB', 20), text, color_text))
        self.sprite_grp.add(user_box)

    def _init_title_text(self):
        box_size = (500, 50)
        self.text_title = RectButton((int)(1280/2-250), 60, box_size[0], box_size[1], Color.BLACK, 0,
                                     Text(pygame.font.SysFont('Agency FB', 35), "Set Number of Max Players", Color.GREEN2))
        self.text_title.change_bg_image(WOOD)
        self.text_title.add_frame(FRAME)

        self.sprite_grp.add(self.text_title)

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], FLASHPOINT_BACKGROUND)
        self.sprite_grp.add(background_box)

    def _init_solo(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.button_solo = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        self.button_solo.change_bg_image(WOOD)
        self.button_solo.add_frame(FRAME)
        self.button_solo.on_click(self.set_and_continue, 1)
        self.sprite_grp.add(self.button_solo)

    def _init_button3(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.button_players3 = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        self.button_players3.on_click(self.set_and_continue, 3)
        self.button_players3.change_bg_image(WOOD)
        self.button_players3.add_frame(FRAME)
        self.sprite_grp.add(self.button_players3)

    def _init_button4(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.button_players4 = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        self.button_players4.change_bg_image(WOOD)
        self.button_players4.add_frame(FRAME)
        self.button_players4.on_click(self.set_and_continue, 4)
        self.sprite_grp.add(self.button_players4)

    def _init_button5(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.button_players5 = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        self.button_players5.change_bg_image(WOOD)
        self.button_players5.add_frame(FRAME)
        self.button_players5.on_click(self.set_and_continue, 5)
        self.sprite_grp.add(self.button_players5)

    def _init_button6(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.button_players6 = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        self.button_players6.on_click(self.set_and_continue, 6)
        self.button_players6.change_bg_image(WOOD)
        self.button_players6.add_frame(FRAME)
        self.sprite_grp.add(self.button_players6)

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        self.buttonBack.on_click(EventQueue.post, CustomEvent(ChangeSceneEnum.CHOOSEBOARDSCENE))
        self.buttonBack.change_bg_image(WOOD)
        self.buttonBack.add_frame(FRAME)
        self.sprite_grp.add(self.buttonBack)

    @staticmethod
    def set_and_continue(desired_players: int):
        GameStateModel.instance().max_players = desired_players
        Networking.get_instance().create_host()
        EventQueue.post(CustomEvent(ChangeSceneEnum.LOBBYSCENE))

    def draw(self, screen):
        self.sprite_grp.draw(screen)

    def update(self, event_queue):
        self.sprite_grp.update(event_queue)

    def _init_duo(self, x_pos, y_pos, text,color, color_text):
        box_size = (130, 48)
        self.button_duo= RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                      Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        self.button_duo.change_bg_image(WOOD)
        self.button_duo.add_frame(FRAME)
        self.button_duo.on_click(self.set_and_continue, 2)
        self.sprite_grp.add(self.button_duo)

