import pygame

import src.constants.color as Color

from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue
from src.action_events.ready_event import ReadyEvent
from src.constants.state_enums import GameKindEnum, PlayerStatusEnum, PlayerRoleEnum, GameStateEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.UIComponents.chat_box import ChatBox
from src.constants.change_scene_enum import ChangeSceneEnum
from src.core.networking import Networking
from src.action_events.start_game_event import StartGameEvent
from src.observers.game_state_observer import GameStateObserver
from src.sprites.player_box import PlayerBox


class LobbyScene(GameStateObserver):

    def __init__(self, screen, current_player: PlayerModel):
        super().__init__()
        self._current_player = current_player
        self._game = GameStateModel.instance()
        self.player_boxes = []

        if Networking.get_instance().is_host:
            self._current_player.color = Color.BLUE
            self._game.host.color = Color.BLUE
            self._current_player.status = PlayerStatusEnum.READY

        self._player_count = len(self._game.players)
        self.isReady = False
        self.resolution = (1280, 700)
        self.sprite_grp = pygame.sprite.Group()
        self.players_not_ready_prompt = None
        self._init_all()

        if self._game.rules == GameKindEnum.EXPERIENCED:
            self.buttonSelChar.on_click(EventQueue.post, CustomEvent(ChangeSceneEnum.CHARACTERSCENE))
        if Networking.get_instance().is_host:
            self._current_player.status = PlayerStatusEnum.READY
            self.isReady = True
            self.start_button.on_click(self.start_game)
            self.start_button.disable()
        else:
            self._current_player.status = PlayerStatusEnum.NOT_READY
            self.buttonReady.on_click(self.set_ready)
        self.buttonBack.on_click(self.go_back)

    def go_back(self):
        Networking.get_instance().disconnect()
        EventQueue.post(CustomEvent(ChangeSceneEnum.STARTSCENE))

    def start_game(self):
        """Callback for when the host tries to start the game."""
        game = GameStateModel.instance()
        players_ready = len([player for player in game.players if player.status == PlayerStatusEnum.READY])

        if not players_ready == game.max_players:
            self.not_enough_players_ready_prompt()
            return
        # Perform the start game hook in Networking (ie. stop accepting new connections and kill broadcast)

        if Networking.get_instance().is_host:
            # Kill the broadcast
            Networking.get_instance().stop_broadcast.set()
            print("Broadcast killed")
            Networking.get_instance().send_to_all_client(StartGameEvent())

    def set_ready(self):
        """Set the status of the current player to ready."""
        if not self.isReady:
            self.isReady = True
            self.buttonReady.change_color(Color.STANDARDBTN)
            self._current_player.status = PlayerStatusEnum.READY
            event = ReadyEvent(self._current_player, True)

            if self._current_player.ip == GameStateModel.instance().host.ip:
                event.execute()
                Networking.get_instance().send_to_all_client(event)
            else:
                Networking.get_instance().send_to_server(event)
        else:
            self.isReady = False
            self.buttonReady.change_color(Color.GREY)
            self._current_player.status = PlayerStatusEnum.NOT_READY
            event = ReadyEvent(self._current_player, False)
            if self._current_player.ip == GameStateModel.instance().host.ip:
                event.execute()
                Networking.get_instance().send_to_all_client(event)
            else:
                Networking.get_instance().send_to_server(event)

    def _init_all(self, reuse=False):
        self._init_background()
        self._init_ip_addr()
        self.chat_box = ChatBox(self._current_player)

        if not reuse:
            self._init_btn_back(20, 20, "Exit", Color.STANDARDBTN, Color.BLACK)

            if self._current_player.ip == GameStateModel.instance().host.ip:
                self._init_start_game_button()
            else:
                # Ready button is grey at first
                self._init_ready(1050, 575, "Ready", Color.GREY, Color.BLACK)

            if not self._game.rules == GameKindEnum.FAMILY :
                self._init_selec_char(1050, 475, "Select Character", Color.STANDARDBTN, Color.BLACK)
        else:
            if not self._game.rules == GameKindEnum.FAMILY:
                self.sprite_grp.add(self.buttonSelChar)
            if self._current_player.ip == GameStateModel.instance().host.ip:
                self.sprite_grp.add(self.start_button)
            else:
                self.sprite_grp.add(self.buttonReady, self.buttonBack)

        self._init_sprites()

    def _init_start_game_button(self):
        """Button for starting the game once all players have clicked ready."""
        box_size = (130, 48)
        self.start_button = RectButton(1050, 575, box_size[0], box_size[1], Color.GREY, 0,
                                       Text(pygame.font.SysFont('Agency FB', 20), "Start", Color.BLACK))
        self.sprite_grp.add(self.start_button)

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/backgrounds/flashpoint_background.png")
        self.sprite_grp.add(background_box)

    def create_butn_img(self, x, y, width, height, path):
        box_size = (width, height)
        self.this_img = RectButton(x, y, box_size[0], box_size[1], path)

        self.sprite_grp.add(self.this_img)

    def _init_selec_char(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonSelChar = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                        Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonSelChar)

    def _init_ready(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)

        self.isReady = False
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
            label_left = (pygame.display.get_surface().get_size()[0] / 2) - (label_width / 2)
            ip_addr_label = RectLabel(label_left, 20, label_width, 50, (255, 255, 255),
                                      txt_obj=(Text(pygame.font.SysFont('Arial', 24), ip_addr)))
            ip_addr_label.set_transparent_background(True)
            self.sprite_grp.add(ip_addr_label)

    def _init_sprites(self):
        text_pos = [(565, 625, 200, 32), (100, 364, 150, 32),
                    (400, 289, 150, 32), (780, 289, 150, 32), (1080, 364, 150, 32)]
        background_pos = [(565, 375, 200, 250), (100, 164, 150, 200), (400, 89, 150, 200),
                          (780, 89, 150, 200), (1080, 164, 150, 200)]
        self.player_boxes = []
        current_player = [player for player in GameStateModel.instance().players if player.ip == self._current_player.ip][0]
        self.player_boxes.append(PlayerBox(text_pos[0], background_pos[0], self._current_player.nickname,
                                           current_player, current_player.color))

        players = [x for x in GameStateModel.instance().players if x.ip != self._current_player.ip]
        i = 1
        for player in players:
            self.player_boxes.append(PlayerBox(text_pos[i], background_pos[i], player.nickname, player, player.color))
            # self.sprite_grp.add(self._init_text_box(text_pos[i], player.nickname, player.color))
            # self.sprite_grp.add(self._init_background_player(background_pos[i]))
            i += 1

    def not_enough_players_ready_prompt(self):
        """Prompt to the host that there are not enough players to join the game."""
        label_width = 400
        label_height = 30
        label_left = 1050 - 100
        label_top = (pygame.display.get_surface().get_size()[1] - 50) - (label_height / 2)
        message = f"Not all players are ready!"
        prompt_label = RectLabel(label_left, label_top, label_width, label_height, Color.WHITE,
                                 txt_obj=Text(pygame.font.SysFont('Arial', 24), message))
        prompt_label.set_transparent_background(True)
        self.players_not_ready_prompt = prompt_label

    def draw(self, screen):
        self.sprite_grp.draw(screen)

        for box in self.player_boxes:
            box.draw(screen)

        self.chat_box.draw(screen)

        if self.players_not_ready_prompt:
            self.players_not_ready_prompt.draw(screen)

    def update(self, event_queue):
        if Networking.get_instance().is_host:
            game = GameStateModel.instance()
            players_ready = len([player for player in game.players if player.status == PlayerStatusEnum.READY])
            if players_ready == game.max_players:
                self.start_button.enable()
                self.start_button.change_color(Color.GREEN)
            else:
                self.start_button.disable()
                self.start_button.change_color(Color.GREY)

        self.chat_box.update(event_queue)

        # game is mutated by reference, BE CAREFUL!!!
        if len(GameStateModel.instance().players) != self._player_count:
            self._player_count = len(GameStateModel.instance().players)
            self.sprite_grp.empty()
            self._init_all(reuse=True)

        self.sprite_grp.update(event_queue)

    def notify_player_index(self, player_index: int):
        pass

    def notify_game_state(self, game_state: GameStateEnum):
        pass

    def damage_changed(self, new_damage: int):
        pass

    def saved_victims(self, victims_saved: int):
        pass

    def dead_victims(self, victims_dead: int):
        pass

    def player_list_changed(self):
        pass
