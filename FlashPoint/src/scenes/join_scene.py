import time

import pygame

import src.constants.color as Color
import src.constants.fonts as Font
from src.core.serializer import JSONSerializer
from src.core.networking import Networking
from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue
from src.core.flashpoint_exceptions import TooManyPlayersException
from src.action_events.too_many_players_event import TooManyPlayersEvent
from src.constants.state_enums import PlayerStatusEnum
from src.models.game_units.player_model import PlayerModel
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.UIComponents.input_box import InputBox
from src.constants.change_scene_enum import ChangeSceneEnum


class JoinScene(object):
    def __init__(self, screen, current_player: PlayerModel):
        self._current_player = current_player
        self.resolution = (1280, 700)
        self.sprite_grp = pygame.sprite.Group()
        self._init_background()
        self._init_text_box(342, 350, "Enter IP:", Color.STANDARDBTN, Color.GREEN2)
        self._init_text_bar(500, 350, 400, 32)
        self._init_btn(625, 536, "Connect", Color.STANDARDBTN, Color.GREEN2)
        self._init_btn_back(20, 20, "Back", Color.STANDARDBTN, Color.GREEN2)
        self._text_bar = self._init_text_bar(500, 350, 400, 32)
        self.error_msg = ""
        self.buttonBack.on_click(EventQueue.post, CustomEvent(ChangeSceneEnum.HOSTJOINSCENE, player=self._current_player))
        self.buttonConnect.on_click(self.join)

    def join(self):
        """
        Start the join host process in Networking
        :param ip_addr: ip address to connect
        :param next_scene: next scene to be called after the process completes
        :param args: extra arguments for the next scene
        :return:
        """

        ip_addr = self.text_bar_msg

        try:
            self._current_player.status = PlayerStatusEnum.NOT_READY
            Networking.get_instance().join_host(ip_addr, player=self._current_player)
            reply = Networking.wait_for_reply()
            # Connection error will be raised if no reply
            if reply:
                reply = JSONSerializer.deserialize(reply)
                if isinstance(reply, TooManyPlayersEvent):
                    raise TooManyPlayersException(self._current_player)
                # GameStateModel.set_game(JSONSerializer.deserialize(reply))
                EventQueue.post(CustomEvent(ChangeSceneEnum.LOBBYSCENE))
        except TimeoutError:
            msg = "Host not found."
            print(msg)
            self.init_error_message(msg)
        except TooManyPlayersException:
            msg = "Lobby is full. Cannot join the game."
            print(msg)
            self.init_error_message(msg)
            # Disconnect client that's trying to connect
            if not Networking.get_instance().is_host:
                Networking.get_instance().client.disconnect()
        except Networking.Client.SocketError:
            msg = "Failed to establish connection."
            print(msg)
            self.init_error_message(msg)
        except OSError:
            msg = "Invalid IP address"
            print(msg)
            self.init_error_message(msg)

    def _init_text_box(self, x_pos, y_pos, text, color: Color, color_text: Color):
        box_size = (136, 32)

        user_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                             Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        user_box.change_bg_image('src/media/GameHud/wood2.png')
        user_box.add_frame('src/media/GameHud/frame.png')

        self.sprite_grp.add(user_box)

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "src/media/backgrounds/flashpoint_background.png")
        self.sprite_grp.add(background_box)

    def _init_btn(self, x_pos, y_pos, text, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonConnect = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                        Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        self.buttonConnect.change_bg_image('src/media/GameHud/wood2.png')
        self.buttonConnect.add_frame('src/media/GameHud/frame.png')
        self.sprite_grp.add(self.buttonConnect)

    def _init_text_bar(self, x_pos, y_pos, width, height):
        inputbox = InputBox(x=x_pos, y=y_pos, w=width, h=height)
        inputbox.disable_enter()
        return inputbox

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        self.buttonBack.change_bg_image('src/media/GameHud/wood2.png')
        self.buttonBack.add_frame('src/media/GameHud/frame.png')
        self.sprite_grp.add(self.buttonBack)

    def init_error_message(self, msg):
        label_width = 400
        label_left = (pygame.display.get_surface().get_size()[0] / 2) - (label_width / 2)
        label_top = (pygame.display.get_surface().get_size()[1] / 6) * 2
        error_msg_label = RectLabel(label_left, label_top, label_width, label_width, (255, 255, 255),
                                    txt_obj=(Text(pygame.font.SysFont('Agency FB', 24), msg, Color.RED)))
        error_msg_label.set_transparent_background(True)
        self.error_msg = error_msg_label

    def draw(self, screen):
        self.sprite_grp.draw(screen)
        self._text_bar.draw(screen)
        if self.error_msg:
            self.error_msg.draw(screen)

    def update(self, event_queue):
        self.sprite_grp.update(event_queue)
        self._text_bar.update(event_queue)
        if self.error_msg:
            self.error_msg.update(event_queue)

    @property
    def text_bar_msg(self):
        return self._text_bar.text
