import pygame
from src.UIComponents.text import Text
import src.constants.color as Color
from src.constants.change_scene_enum import ChangeSceneEnum
from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue
from src.models.game_units.player_model import PlayerModel
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.scene import Scene
from src.core.networking import Networking

class WinScene(Scene):
    def __init__(self, screen: pygame.Surface):
        Scene.__init__(self, screen)
        self._init_background()
        self._init_continue_btn()
        self._init_title_text()


    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "src/media/Win_Loose/happy.jpg")
        self.sprite_grp.add(background_box)
    #
    # def _init_log_box(self):
    #     box_size = (self.resolution[0] / 2, self.resolution[1] / 2)
    #     x_pos = self.resolution[0] / 2 - box_size[0] / 2
    #     y_pos = self.resolution[1] / 2 - box_size[1] / 2
    #     log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.GREEN)
    #     self.sprite_grp.add(log_box)
    #
    #

    def _init_title_text(self):
        box_size = (500, 50)
        self.text_title = RectLabel(400, 350, box_size[0], box_size[1], "src/media/Win_Loose/WON.png"                                    )
        self.sprite_grp.add(self.text_title)


    def _init_continue_btn(self):
        box_size = (200,50)
        ctn_btn = RectButton(550,500,box_size[0],box_size[1],'src/media/GameHud/wood2.png',0,Text(pygame.font.SysFont('Agency FB', 20), "Continue", Color.GREEN2))
        ctn_btn.add_frame('src/media/GameHud/frame.png')
        ctn_btn.on_click(self._continue)
        self.sprite_grp.add(ctn_btn)


    def _continue(self):
        Networking.get_instance().disconnect()
        EventQueue.post(CustomEvent(ChangeSceneEnum.STARTSCENE))


