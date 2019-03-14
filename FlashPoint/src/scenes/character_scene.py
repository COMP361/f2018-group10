import pygame

import src.constants.color as Color
from src.action_events.select_character_event import SelectCharacterEvent
from src.constants.state_enums import PlayerRoleEnum
from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue

from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.core.networking import Networking
from src.models.game_state_model import GameStateModel
from src.UIComponents.scene import Scene
from src.UIComponents.text import Text
from src.models.game_units.player_model import PlayerModel
from src.constants.change_scene_enum import ChangeSceneEnum


class CharacterScene(Scene):

    def __init__(self, screen, current_player: PlayerModel):
        self.label_grp = pygame.sprite.Group()
        self._current_player = current_player
        self.role = None
        self.str = None
        self.roles = {
            "cafs": PlayerRoleEnum.CAFS,
            "captain": PlayerRoleEnum.CAPTAIN,
            "paramedic": PlayerRoleEnum.PARAMEDIC,
            "hazmat": PlayerRoleEnum.HAZMAT,
            "driver": PlayerRoleEnum.DRIVER,
            "generalist": PlayerRoleEnum.GENERALIST,
            "imaging":PlayerRoleEnum.IMAGING,
            "rescue":PlayerRoleEnum.RESCUE,
        }


        Scene.__init__(self, screen)
        self._init_background()
        self.create_label(0, 0, 100, 150)
        self.create_butn_img(250, 150, 99, 150,
                             "media/specialist_cards/cafs_firefighter.png", "cafs")

        self.create_butn_img(450, 150, 100, 150,
                             "media/specialist_cards/driver_operator.png", "driver")

        self.create_butn_img(650, 150, 100, 150,
                             "media/specialist_cards/fire_captain.png", "captain")

        self.create_butn_img(850, 150, 99, 150,
                             "media/specialist_cards/generalist.png", "generalist")

        self.create_butn_img(250, 450, 100, 150,
                             "media/specialist_cards/hazmat_technician.png", "hazmat")

        self.create_butn_img(450, 450, 99, 150,
                             "media/specialist_cards/imaging_technician.png", "imaging")

        self.create_butn_img(650, 450, 99, 150,
                             "media/specialist_cards/paramedic.png", "paramedic")

        self.create_butn_img(850, 450, 98, 150,
                             "media/specialist_cards/rescue_specialist.png", "rescue")

        self._init_btn_back(20, 20, "Back", Color.STANDARDBTN, Color.BLACK)

        self._init_btn_confirm(1050, 575, "Confirm", Color.STANDARDBTN, Color.BLACK)

        self._init_title_text()
        self.buttonBack.on_click(EventQueue.post, CustomEvent(ChangeSceneEnum.LOBBYSCENE))
        self.buttonConfirm.on_click(self.confirm)

    def confirm(self):

        available = self.check(self.str)
        if not available:
            """already taken"""
            return
        else:
            event = SelectCharacterEvent(self._current_player,self.role)
            if self._current_player.ip == GameStateModel.instance().host.ip:
                Networking.get_instance().send_to_all_client(event)
            else:
                Networking.get_instance().send_to_server(event)


            EventQueue.post(CustomEvent(ChangeSceneEnum.LOBBYSCENE))

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/backgrounds/flashpoint_background.png")
        self.sprite_grp.add(background_box)

    def create_butn_img(self, x, y, width, height, path: str,  count: str):
        label = self.create_label(x, y, width, height)
        self.label_grp.add(label)
        self.sprite_grp.add(label)

        box_size = (width, height)
        self.this_img = RectButton(x, y, box_size[0], box_size[1], path)


        if count == "cafs":
            self.role = PlayerRoleEnum.CAFS

        elif count == "driver":
            self.role = PlayerRoleEnum.DRIVER

        elif count == "captain":
            self.role = PlayerRoleEnum.CAPTAIN

        elif count == "generalist":
            self.role = PlayerRoleEnum.GENERALIST

        elif count == "hazmat":
            self.role = PlayerRoleEnum.HAZMAT

        elif count == "imaging":
            self.role = PlayerRoleEnum.IMAGING

        elif count == "paramedic":
            self.role = PlayerRoleEnum.PARAMEDIC

        else:
            self.role = PlayerRoleEnum.RESCUE

        self.this_img.on_click(self.click_img, label, self.role)
        self.sprite_grp.add(self.this_img)

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonBack)

    def _init_title_text(self):
        box_size = (400, 50)
        self.text_title = RectButton(400, 60, box_size[0], box_size[1], Color.BLACK, 0,
                                     Text(pygame.font.SysFont('Arial', 35), "Character Selection", Color.WHITE))

        self.sprite_grp.add(self.text_title)

    def _init_btn_confirm(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonConfirm = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                        Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonConfirm)

    def create_label(self, x_pos: int, y_pos: int, width: int, height: int):
        return RectLabel(x_pos - 15, y_pos - 15, width + 30, height + 30, Color.BLACK)

    def click_img(self, btn, enum: PlayerRoleEnum):
        for sprite in self.label_grp:
            if isinstance(sprite, RectLabel):
                sprite.change_color(Color.BLACK)

        if isinstance(btn, RectLabel):
            btn.change_color(Color.WHITE)

        #self._current_player.character = enum

    def check(self,role):

        available = False
        players = GameStateModel.instance().players

        for role in self.roles:
            available = True
            for player in players:
                if player.character == self.roles[role]:
                    available = False
                    break
                else:
                    continue

        return available
