import pygame

import src.constants.color as Color
from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue
from src.models.game_units.player_model import PlayerModel
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.UIComponents.scene import Scene
from src.constants.change_scene_enum import ChangeSceneEnum
from src.core.networking import Networking


class HostJoinScene(Scene):
    def __init__(self, screen: pygame.Surface, current_player: PlayerModel):
        Scene.__init__(self, screen)
        self._current_player = current_player
        self._init_background()
        self._init_btn_host(575, 481, "Host", Color.STANDARDBTN, Color.GREEN2)
        self._init_btn_join(575, 371, "Join", Color.STANDARDBTN, Color.GREEN2)
        self._init_btn_back(20, 20, "Back", Color.STANDARDBTN, Color.GREEN2)
        self.buttonJoin.on_click(EventQueue.post, CustomEvent(ChangeSceneEnum.JOINSCENE))
        self.buttonBack.on_click(EventQueue.post, CustomEvent(ChangeSceneEnum.STARTSCENE))
        self.buttonHost.on_click(self.host)

    @staticmethod
    def host():
        Networking.get_instance().create_host()
        EventQueue.post(CustomEvent(ChangeSceneEnum.HOSTMENUSCENE))

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/backgrounds/flashpoint_background.png")
        self.sprite_grp.add(background_box)

    def _init_log_box(self):
        box_size = (self.resolution[0] / 2, self.resolution[1] / 2)
        x_pos = self.resolution[0] / 2 - box_size[0] / 2
        y_pos = self.resolution[1] / 2 - box_size[1] / 2
        log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.GREEN)
        self.sprite_grp.add(log_box)

    def _init_btn_join(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonJoin = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        self.buttonJoin.change_bg_image('media/GameHud/wood2.png')
        self.buttonJoin.add_frame('media/GameHud/frame.png')
        self.sprite_grp.add(self.buttonJoin)

    def _init_btn_host(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonHost = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        self.buttonHost.change_bg_image('media/GameHud/wood2.png')
        self.buttonHost.add_frame('media/GameHud/frame.png')
        self.sprite_grp.add(self.buttonHost)

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        self.buttonBack.change_bg_image('media/GameHud/wood2.png')
        self.buttonBack.add_frame('media/GameHud/frame.png')

        self.sprite_grp.add(self.buttonBack)
