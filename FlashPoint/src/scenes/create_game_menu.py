import pygame

import src.constants.color as Color
from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue
from src.models.game_units.player_model import PlayerModel
from src.models.game_state_model import GameStateModel

from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.UIComponents.scene import Scene
from src.constants.state_enums import GameKindEnum, DifficultyLevelEnum
from src.constants.change_scene_enum import ChangeSceneEnum
from src.core.networking import Networking


class CreateGameMenuScene(Scene):
    def __init__(self, screen: pygame.Surface, current_player: PlayerModel):
        Scene.__init__(self, screen)
        self._current_player = current_player

        self._init_background()
        self._init_text_box(344, 387, 200, 32, "Choose Game Mode:", Color.STANDARDBTN, Color.BLACK)
        self._init_btn_back(20, 20, "Back", Color.STANDARDBTN, Color.BLACK)
        self._init_btn_family(575, 381, "Family", Color.STANDARDBTN, Color.BLACK)
        self._init_btn_rec(575, 500, "Recruit", Color.GREEN, Color.BLACK)
        self._init_btn_veteran(710, 500, "Veteran", Color.YELLOW, Color.BLACK)
        self._init_btn_heroic(845, 500, "Heroic", Color.RED, Color.BLACK)

        self.buttonRecruit.on_click(self.create_new_game, GameKindEnum.EXPERIENCED, DifficultyLevelEnum.RECRUIT)
        self.buttonVeteran.on_click(self.create_new_game, GameKindEnum.EXPERIENCED, DifficultyLevelEnum.VETERAN)
        self.buttonHeroic.on_click(self.create_new_game, GameKindEnum.EXPERIENCED, DifficultyLevelEnum.HEROIC)
        self.buttonFamily.on_click(self.create_new_game, GameKindEnum.FAMILY)
        self.buttonBack.on_click(self._disconnect_and_back)

    @staticmethod
    def _disconnect_and_back():
        Networking.get_instance().disconnect()
        EventQueue.post(CustomEvent(ChangeSceneEnum.HOSTMENUSCENE))

    # ------------- GAME CREATE/LOAD STUFF ---------- #

    def create_new_game(self, game_kind: GameKindEnum, difficulty_level: DifficultyLevelEnum = None):
        """Instantiate a new family game and move to the lobby scene."""
        GameStateModel(self._current_player, 6, game_kind, None, difficulty_level)
        if game_kind == GameKindEnum.FAMILY:
            EventQueue.post(CustomEvent(ChangeSceneEnum.CHOOSEBOARDSCENE))
        elif game_kind == GameKindEnum.EXPERIENCED:
            EventQueue.post(CustomEvent(ChangeSceneEnum.CHOOSEBOARDSCENE))

    # ----------------------------------------------- #

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/backgrounds/flashpoint_background.png")
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

    def _init_btn_rec(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonRecruit = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                    Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonRecruit)

    def _init_btn_veteran(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonVeteran = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                    Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonVeteran)

    def _init_btn_heroic(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonHeroic = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                    Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonHeroic)

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonBack)
