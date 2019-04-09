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


class ChooseBoardScene(object):
    def __init__(self, screen, current_player: PlayerModel):
        self.game_kind = GameStateModel.instance().rules
        self.sprite_grp = pygame.sprite.Group()
        self._current_player = current_player
        self.resolution = (1280, 700)

        self._init_background()
        self._init_title_text()
        #self._init_back_box((int)(1280 / 2 - 250), 130, "", Color.GREY, Color.GREEN)

        self._init_board1(410, 400, "Original", Color.STANDARDBTN, Color.GREEN2)
        self._init_board1(575, 400, "Alternative", Color.STANDARDBTN, Color.GREEN2)
        self._init_board3(740, 400, "Random", Color.STANDARDBTN, Color.GREEN2)
        self._init_btn_back(20, 20, "Back", Color.STANDARDBTN, Color.GREEN2)

    def _init_back_box(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        user_box = RectLabel(x_pos, y_pos, 500, 500, color, 0,
                             Text(pygame.font.SysFont('Agency FB', 25), text, color_text))

        self.sprite_grp.add(user_box)

    def _init_title_text(self):
        box_size = (500, 50)
        self.text_title = RectButton((int)(1280 / 2 - 250), 300, box_size[0], box_size[1], Color.BLACK, 0,
                                     Text(pygame.font.SysFont('Agency FB', 35), "Choose Board", Color.GREEN2))
        self.text_title.change_bg_image('media/GameHud/wood2.png')
        self.text_title.add_frame('media/GameHud/frame.png')
        self.sprite_grp.add(self.text_title)

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/backgrounds/flashpoint_background.png")
        self.sprite_grp.add(background_box)

    def _init_board1(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.button_board1 = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                        Text(pygame.font.SysFont('Agency FB', 25), text, color_text))

        self.button_board1.change_bg_image('media/GameHud/wood2.png')
        self.button_board1.add_frame('media/GameHud/frame.png')
        self.button_board1.on_click(self.set_and_continue, GameBoardTypeEnum.ORIGINAL)
        self.sprite_grp.add(self.button_board1)

    def _init_board2(self, x_pos, y_pos, text, color, color_text):
        box_size = (130, 48)
        self.button_board2 = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                        Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        self.button_board2.on_click(self.set_and_continue, GameBoardTypeEnum.ALTERNATIVE)
        self.button_board2.change_bg_image('media/GameHud/wood2.png')
        self.button_board2.add_frame('media/GameHud/frame.png')
        self.sprite_grp.add(self.button_board2)

    def _init_board3(self, x_pos, y_pos, text, color, color_text):
        box_size = (130, 48)
        self.button_board3 = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                        Text(pygame.font.SysFont('Agency FB', 25), text, color_text))

        self.button_board3.on_click(self.set_and_continue, GameBoardTypeEnum.RANDOM)
        self.button_board3.change_bg_image('media/GameHud/wood2.png')
        self.button_board3.add_frame('media/GameHud/frame.png')
        self.sprite_grp.add(self.button_board3)

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        self.buttonBack.change_bg_image('media/GameHud/wood2.png')
        self.buttonBack.add_frame('media/GameHud/frame.png')
        self.buttonBack.on_click(self.destroy_game_and_back)
        self.sprite_grp.add(self.buttonBack)

    @staticmethod
    def destroy_game_and_back():
        GameStateModel.instance().destroy()
        EventQueue.post(CustomEvent(ChangeSceneEnum.CREATEGAMEMENU))

    @staticmethod
    def set_and_continue(board_type: GameBoardTypeEnum):
        GameStateModel.instance().board_type = board_type
        EventQueue.post(CustomEvent(ChangeSceneEnum.SETMAXPLAYERSCENE))

    def draw(self, screen):
        self.sprite_grp.draw(screen)

    def update(self, event_queue):
        self.sprite_grp.update(event_queue)
