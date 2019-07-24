import json

import pygame
import os.path

import src.constants.color as color
from src.controllers.chop_controller import ChopController
from src.controllers.door_controller import DoorController
from src.controllers.tile_input_controller import TileInputController
from src.models.game_state_model import GameStateModel
from src.sprites.game_board import GameBoard

from src.models.game_board.null_model import NullModel
from src.core.custom_event import CustomEvent
from src.core.networking import Networking
from src.core.serializer import JSONSerializer
from src.models.game_units.player_model import PlayerModel
from src.core.event_queue import EventQueue

from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.UIComponents.input_box import InputBox
from src.UIComponents.profile_list import ProfileList
from src.constants.change_scene_enum import ChangeSceneEnum


class StartScene(object):
    def __init__(self, screen):
        self.profiles = "src/media/profiles.json"
        self.resolution = (1280, 700)
        self.sprite_grp = pygame.sprite.Group()
        self._init_background()

        self._init_profile_selector(((self.resolution[0]/2)-(500/2)), 330, color.GREY)
        self.text_bar1 = self._init_text_bar(((self.resolution[0]/2)-(500/2))-20, 600, 400, 32)
        self.text_bar1.disable_enter()

        self._init_btn_register(((self.resolution[0]/2)-(500/2))+400, 592, "Create Profile",
                                color.STANDARDBTN, color.GREEN2)
        self.update_profiles()

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "src/media/backgrounds/flashpoint_background.png")
        self.sprite_grp.add(background_box)

    def _init_log_box(self, clr):
        box_size = (self.resolution[0] / 2, self.resolution[1] / 2)
        x_pos = self.resolution[0] / 2 - box_size[0] / 2
        y_pos = self.resolution[1] / 2 - box_size[1] / 2
        log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], clr)
        log_box.change_bg_image('src/media/GameHud/wood2.png')
        log_box.add_frame('src/media/GameHud/frame.png')
        self.sprite_grp.add(log_box)

    def _init_text_box(self, x_pos, y_pos, text, clr, color_text):
        box_size = (136, 32)

        user_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], clr, 0,
                             Text(pygame.font.SysFont('Agency FB', 20), text, color_text))
        self.sprite_grp.add(user_box)

    def _init_btn_register(self, x_pos, y_pos, text, clr, color_text):
        box_size = (130, 48)
        self.buttonRegister = RectButton(x_pos, y_pos, box_size[0], box_size[1], clr, 0,
                                         Text(pygame.font.SysFont('Agency FB', 25), text, color_text))
        self.buttonRegister.change_bg_image('src/media/GameHud/wood2.png')
        self.buttonRegister.add_frame('src/media/GameHud/frame.png')
        self.buttonRegister.on_click(self.register_profile)
        self.sprite_grp.add(self.buttonRegister)

    def register_profile(self):
        # Gets the text in the text bar and send the create profile event to the event queue (scene manager)
        self.create_profile(self.text_bar1)
        self.update_profiles()

    @staticmethod
    def _init_text_bar(x_pos, y_pos, width, height):
        return InputBox(x=x_pos, y=y_pos, w=width, h=height)

    def _init_profile_selector(self, x_pos, y_pos, clr):
        box_size = (500, 250)
        self.profile = ProfileList(x_pos, y_pos, box_size[0], box_size[1], 3, clr)

    def draw(self, screen):
        self.sprite_grp.draw(screen)
        # self._text_bar2.draw(screen)
        self.text_bar1.draw(screen)
        self.profile.draw(screen)

    def update(self, event_queue):
        self.sprite_grp.update(event_queue)
        self.text_bar1.update(event_queue)
        self.profile.update(event_queue)
        # self._text_bar2.update(event_queue)

    def init_error_message(self, msg):
        label_width = 400
        label_left = (pygame.display.get_surface().get_size()[0] / 2) - (label_width / 2)
        label_top = (pygame.display.get_surface().get_size()[1] / 6) * 2
        error_msg_label = RectLabel(label_left, label_top, label_width, label_width, (255, 255, 255),
                                    txt_obj=(Text(pygame.font.SysFont('Agency FB', 24), msg, color.RED)))
        error_msg_label.set_transparent_background(True)
        self.error_msg = error_msg_label

# ------------ Stuff for profiles and start scene ------------ #

    def update_profiles(self):
        if not os.path.exists(self.profiles):
            with open(self.profiles, mode="w+", encoding='utf-8') as myFile:
                myFile.write("[]")
        with open(self.profiles, mode='r', encoding='utf-8') as myFile:
            temp = json.load(myFile)
            for i, user in enumerate(temp):
                player: PlayerModel = JSONSerializer.deserialize(user)
                player.ip = Networking.get_instance().get_ip()
                player.set_pos(-1, -1)
                player.ap = 0
                player.special_ap = 0
                player.carrying_victim = NullModel()
                self.profile.set_profile(
                    i, player.nickname, player.wins, player.losses, EventQueue.post,
                    CustomEvent(ChangeSceneEnum.HOSTJOINSCENE, player=player)
                )
                self.profile.remove_profile_callback(i, self.remove_profile, player.nickname)

    def create_profile(self, text_bar: InputBox):
        temp = {}
        with open(self.profiles, mode='r+', encoding='utf-8') as myFile:

            temp = json.load(myFile)
            size = len(temp)
            if size >= 3:
                return

            if not text_bar.text.strip():
                return

            size = len(text_bar.text.strip())

            if size <= 12:
                player_model = PlayerModel(
                    ip=Networking.get_instance().get_ip(),
                    nickname=text_bar.text.strip()
                )
                player = JSONSerializer.serialize(player_model)
                temp.append(player)
            else:
                msg = "Nickname must have less than 12 letters"
                self.init_error_message(msg)

        with open(self.profiles, mode='w', encoding='utf-8') as myFile:
            json.dump(temp, myFile)

        self.update_profiles()

    def remove_profile(self, removename: str):
        temp = {}
        with open(self.profiles, mode='r+', encoding='utf-8') as myFile:
            temp = json.load(myFile)
            for perm in temp:
                for name in perm.values():
                    if name == removename:
                        temp.remove(perm)
                    else:
                        continue

        with open(self.profiles, mode='w', encoding='utf-8') as myFile:
            json.dump(temp, myFile)

        self.update_profiles()
