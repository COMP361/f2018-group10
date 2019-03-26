import pygame

import src.constants.color as Color
from src.constants.change_scene_enum import ChangeSceneEnum
from src.constants.state_enums import GameBoardTypeEnum
from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text


class ChooseBoard(object):
    def __init__(self, screen, current_player: PlayerModel):
        self.game_kind = GameStateModel.instance().rules
        self.sprite_grp = pygame.sprite.Group()
        self._current_player = current_player
        self.resolution = (1280, 700)

        self._init_background()
        self._init_title_text()
        self._init_back_box((int)(1280 / 2 - 250), 130, "", Color.GREY, Color.GREEN)

        # COMMENT THIS OUT LATER
        self._init_board1(410, 400, "Original", Color.STANDARDBTN, Color.BLACK)
        self._init_board2(740, 400, "Alternative", Color.STANDARDBTN, Color.BLACK)
        # self._init_button3(410, 200, "3", Color.STANDARDBTN, Color.BLACK)
        # self._init_button4(740, 200, "4", Color.STANDARDBTN, Color.BLACK)
        # self._init_button5(410, 300, "5", Color.STANDARDBTN, Color.BLACK)
        # self._init_button6(740, 300, "6", Color.STANDARDBTN, Color.BLACK)
        self._init_btn_back(20, 20, "Back", Color.STANDARDBTN, Color.BLACK)

    def _init_back_box(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        user_box = RectLabel(x_pos, y_pos, 500, 500, color, 0,
                             Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(user_box)

    def _init_title_text(self):
        box_size = (500, 50)
        self.text_title = RectButton((int)(1280 / 2 - 250), 60, box_size[0], box_size[1], Color.BLACK, 0,
                                     Text(pygame.font.SysFont('Arial', 35), "Choose Board", Color.WHITE))

        self.sprite_grp.add(self.text_title)

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/backgrounds/flashpoint_background.png")
        self.sprite_grp.add(background_box)

    def _init_board1(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.button_board1 = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                        Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.button_board1.on_click(self.set_and_continue, GameBoardTypeEnum.ORIGINAL)
        self.sprite_grp.add(self.button_board1)

    def _init_board2(self, x_pos, y_pos, text, color, color_text):
        box_size = (130, 48)
        self.button_board2 = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                        Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.button_board2.on_click(self.set_and_continue, GameBoardTypeEnum.ALTERNATIVE)
        self.sprite_grp.add(self.button_board2)

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.buttonBack.on_click(EventQueue.post, CustomEvent(ChangeSceneEnum.CREATEGAMEMENU))
        self.sprite_grp.add(self.buttonBack)

    @staticmethod
    def set_and_continue(type : GameBoardTypeEnum):
        GameStateModel.instance().game_board.board_type = type
        EventQueue.post(CustomEvent(ChangeSceneEnum.SETMAXPLAYERSCENE))

    def draw(self, screen):
        self.sprite_grp.draw(screen)

    def update(self, event_queue):
        self.sprite_grp.update(event_queue)
