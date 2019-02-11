import pygame

import src.constants.color as Color
from src.constants.state_enums import GameKindEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.UIComponents.chat_box import ChatBox
from src.core.networking import Networking


class LobbyScene(object):
    def __init__(self, screen, current_player: PlayerModel, game: GameStateModel):
        self._current_player = current_player
        self._game = game
        self._player_count = len(self._game.players)

        self.resolution = (1280, 700)
        self.sprite_grp = pygame.sprite.Group()
        self._init_all()

    def _init_all(self, reuse=False):
        self._init_background()
        self._init_ip_addr()
        self.chat_box = ChatBox()

        if not reuse:
            self._init_btn_back(20, 20, "Exit", Color.STANDARDBTN, Color.BLACK)
            self._init_ready(1050, 575, "Ready", Color.STANDARDBTN, Color.BLACK)
            if self._game.rules == GameKindEnum.EXPERIENCED:
                self._init_selec_char(1050, 475, "Select Character", Color.STANDARDBTN, Color.BLACK)
        else:
            if self._game.rules == GameKindEnum.EXPERIENCED:
                self.sprite_grp.add(self.buttonSelChar)
            self.sprite_grp.add(self.buttonReady, self.buttonBack)
        self._init_sprites()

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/backgrounds/flashpoint_background.png")
        self.sprite_grp.add(background_box)

    def create_butn_img(self, x, y, width, height, path):
        box_size = (width, height)
        self.this_img = RectButton(x, y, box_size[0], box_size[1], path)

        self.sprite_grp.add(self.this_img)

    def _init_background_player(self, rect):
        user_box = RectLabel(rect[0], rect[1], rect[2], rect[3], "media/specialist_cards/generalist.png")
        return user_box

    def _init_text_box(self, position, text, color):
        box_size = (position[2], position[3])

        user_box = RectLabel(position[0], position[1], box_size[0], box_size[1], color, 0,
                             Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        return user_box

    def _init_selec_char(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonSelChar = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonSelChar)

    def _init_ready(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonReady = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonReady)

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonBack)

    def _init_ip_addr(self):
        if Networking.get_instance().is_host:
            ip_addr = f"Your IP address: {Networking.get_instance().get_ip()}"
            label_width = 400
            label_left = (pygame.display.get_surface().get_size()[0]/2) - (label_width/2)
            ip_addr_label = RectLabel(label_left, 20, label_width, 50, (255, 255, 255),
                                      txt_obj=(Text(pygame.font.SysFont('Arial', 24), ip_addr)))
            ip_addr_label.set_transparent_background(True)
            self.sprite_grp.add(ip_addr_label)

    def _init_sprites(self):
        text_pos = [(565, 625, 200, 32), (100, 364, 150, 32),
                    (400, 289, 150, 32), (780, 289, 150, 32), (1080, 364, 150, 32)]
        background_pos = [(565, 375, 200, 250), (100, 164, 150, 200), (400, 89, 150, 200),
                          (780, 89, 150, 200), (1080, 164, 150, 200)]

        self.sprite_grp.add(self._init_text_box(text_pos[0], self._current_player.nickname, self._current_player.color))
        self.sprite_grp.add(self._init_background_player(background_pos[0]))

        players = [x for x in self._game.players if x.ip != self._current_player.ip]
        i = 1
        for player in players:
            self.sprite_grp.add(self._init_text_box(text_pos[i], player.nickname, player.color))
            self.sprite_grp.add(self._init_background_player(background_pos[i]))
            i += 1

    def draw(self, screen):
        self.sprite_grp.draw(screen)
        self.chat_box.draw(screen)

    def update(self, event_queue):
        self.sprite_grp.update(event_queue)
        self.chat_box.update(event_queue)

        # game is mutated by reference, BE CAREFUL!!!
        if len(self._game.players) != self._player_count:
            print("Redrawing sprites")
            self._player_count = len(self._game.players)
            self.sprite_grp.empty()
            self._init_all(reuse=True)

