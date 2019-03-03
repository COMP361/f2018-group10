import pygame

import src.constants.color as Color
from src.UIComponents.scene import Scene
from src.constants.state_enums import GameKindEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.UIComponents.chat_box import ChatBox
from src.core.networking import Networking

class SetMaxPlayers(object):
    def __init__(self, screen, current_player: PlayerModel, game: GameStateModel):
        self.sprite_grp = pygame.sprite.Group()
        self._current_player = current_player
        self._game = game
        self.resolution = (1280, 700)

        self._init_background()
        self._init_title_text()

        self._init_button3(420, 200, "3", Color.STANDARDBTN, Color.BLACK)
        self._init_button4(640, 200, "4", Color.STANDARDBTN, Color.BLACK)
        self._init_button5(420, 300, "5", Color.STANDARDBTN, Color.BLACK)
        self._init_button6(640, 300, "6", Color.STANDARDBTN, Color.BLACK)

    def _init_title_text(self):
        box_size = (400, 50)
        self.text_title = RectButton(400, 60, box_size[0], box_size[1], Color.BLACK, 0,
                                     Text(pygame.font.SysFont('Arial', 35), "Set Number of Max Players", Color.WHITE))

        self.sprite_grp.add(self.text_title)

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/backgrounds/flashpoint_background.png")
        self.sprite_grp.add(background_box)

    def _init_button3(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.button_players3 = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.button_players3)
    def _init_button4(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.button_players4 = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.button_players4)
    def _init_button5(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.button_players5 = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.button_players5)
    def _init_button6(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.button_players6 = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.button_players6)

    def draw(self, screen):
        self.sprite_grp.draw(screen)
        # self._text_bar2.draw(screen)
        # self.text_bar1.draw(screen)
        # self.profile.draw(screen)

    def update(self, event_queue):
        self.sprite_grp.update(event_queue)
        # self.text_bar1.update(event_queue)
        # self.profile.update(event_queue)
        # self._text_bar2.update(event_queue)

