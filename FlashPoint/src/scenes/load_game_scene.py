import os

import pygame

import src.constants.color as color
import json

from src.core.custom_event import CustomEvent
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.UIComponents.input_box import InputBox
from src.constants.change_scene_enum import ChangeSceneEnum
from src.core.event_queue import EventQueue
from src.core.serializer import JSONSerializer
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel

RESOLUTION = (1280, 700)


class LoadGameScene(object):

    def __init__(self, screen, current_player: PlayerModel):
        self._current_player = current_player

        self._saved_games_path = "media/saved_games.json"
        if not os.path.exists(self._saved_games_path):
            with open(self._saved_games_path, mode="w+", encoding='utf-8') as myFile:
                myFile.write("[]")

        self.sprite_grp = pygame.sprite.Group()
        self._init_background()
        self._init_load_menu(390, 100, "", color.GREY, color.GREEN)
        self._load_saved_games_buttons()

        self._init_btn_back(20, 20, "Back", color.STANDARDBTN, color.GREEN2)

    def _init_background(self):
        box_size = (RESOLUTION[0], RESOLUTION[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/backgrounds/flashpoint_background.png")
        self.sprite_grp.add(background_box)

    def _init_log_box(self, clr):
        box_size = (RESOLUTION[0] / 2, RESOLUTION[1] / 2)
        x_pos = RESOLUTION[0] / 2 - box_size[0] / 2
        y_pos = RESOLUTION[1] / 2 - box_size[1] / 2
        log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], clr)
        self.sprite_grp.add(log_box)

    def _init_save_elem(self, x_pos, y_pos, text, clr, color_text, save_data):
        box_size = (350, 32)

        user_box = RectButton(x_pos, y_pos, box_size[0], box_size[1], clr, 0,
                              Text(pygame.font.SysFont('Agency FB', 20), text, color_text))
        user_box.change_bg_image('media/GameHud/wood2.png')
        pygame.draw.rect(user_box.image, color.YELLOW, [0, 0, 350, 32], 5)

        user_box.on_click(self.load_game, save_data)
        return user_box

    def load_game(self, save):
        """Instantiate a new family game and move to the lobby scene."""
        data = save

        # Restore game metadata
        game: GameStateModel = JSONSerializer.deserialize(data)
        game.host = self._current_player
        game.players = [self._current_player]

        game.board_type = GameBoardTypeEnum.LOADED
        # Restore GameBoard
        GameStateModel.set_game(game)
        game.game_board.is_loaded = True
        EventQueue.post(CustomEvent(ChangeSceneEnum.LOBBYSCENE))

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: color, color_text: color):
        box_size = (130, 48)
        button_back = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 25), text, color_text))
        button_back.on_click(EventQueue.post, CustomEvent(ChangeSceneEnum.HOSTMENUSCENE))
        button_back.change_bg_image('media/GameHud/wood2.png')
        button_back.add_frame('media/GameHud/frame.png')
        self.sprite_grp.add(button_back)

    def _init_load_menu(self, x_pos: int, y_pos: int, text: str, color: color, color_text: color):
        user_box = RectLabel(x_pos, y_pos, 500, 500, color, 0,
                             Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        user_box.change_bg_image('media/GameHud/wood2.png')
        user_box.add_frame('media/GameHud/frame.png')
        self.sprite_grp.add(user_box)

    @staticmethod
    def _init_text_bar(x_pos, y_pos, width, height):
        return InputBox(x=x_pos, y=y_pos, w=width, h=height)

    def _load_saved_games_buttons(self):
        with open(self._saved_games_path, mode='r', encoding='utf-8') as myFile:
            temp = json.load(myFile)
            for i, game_json in enumerate(temp):
                x = game_json["time"]
                temp_str: str = "Game " + str(i + 1) + "  |  " + x
                self.sprite_grp.add(self._init_save_elem(470, 155 + 34 * i, temp_str, color.ORANGE, color.GREEN2, game_json))

    def draw(self, screen):
        self.sprite_grp.draw(screen)

    def update(self, event_queue):
        self.sprite_grp.update(event_queue)
