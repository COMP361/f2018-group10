import pygame

import src.constants.color as Color
from src.action_events.choose_character_event import ChooseCharacterEvent
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
import src.constants.media_constants as MEDIA_CONSTS


class CharacterScene(Scene):
    def __init__(self, screen, current_player: PlayerModel):
        self.label_grp = pygame.sprite.Group()
        self._current_player = current_player
        Scene.__init__(self, screen)
        self._init_background()
        self._game = GameStateModel.instance()

        self.create_label(0, 0, 100, 150, 1)
        self.create_butn_img(150, 150, 99, 150,
                             MEDIA_CONSTS.CAFS_FIREFIGHTER, 1)

        self.create_butn_img(350, 150, 100, 150,
                             MEDIA_CONSTS.DRIVER_OPERATOR, 2)

        self.create_butn_img(550, 150, 100, 150,
                             MEDIA_CONSTS.FIRE_CAPTAIN, 3)

        self.create_butn_img(750, 150, 99, 150,
                             MEDIA_CONSTS.GENERALIST, 4)

        self.create_butn_img(150, 450, 100, 150,
                             MEDIA_CONSTS.HAZMAT_TECHNICIAN, 5)

        self.create_butn_img(350, 450, 99, 150,
                             MEDIA_CONSTS.IMAGING_TECHNICIAN, 6)

        self.create_butn_img(550, 450, 99, 150,
                             MEDIA_CONSTS.PARAMEDIC, 7)

        self.create_butn_img(750, 450, 98, 150,
                             MEDIA_CONSTS.RESCUE_SPECIALIST, 8)

        self.create_butn_img(950, 150, 98, 150,
                             MEDIA_CONSTS.DOGE, 9)

        self.create_butn_img(950, 450, 99, 150,
                             MEDIA_CONSTS.VETERAN, 10)

        self._init_btn_back(20, 20, "Back", Color.STANDARDBTN, Color.BLACK)

        self._init_btn_confirm(1100, 575, "Confirm", Color.STANDARDBTN, Color.BLACK)

        self._init_title_text()
        self.character_enum: PlayerRoleEnum = None
        self.buttonBack.on_click(EventQueue.post, CustomEvent(ChangeSceneEnum.LOBBYSCENE))
        self.buttonConfirm.on_click(self.confirm)

    def confirm(self):
        if self.character_enum:

            accept = True  # This is a boolean flag

            if any([player.role == self.character_enum for player in self._game.players]):
                accept = False

            if accept:  # means no one took this character
                EventQueue.post(CustomEvent(ChangeSceneEnum.LOBBYSCENE))

                event = ChooseCharacterEvent(self.character_enum, self._game.players.index(self._current_player))

                if Networking.get_instance().is_host:
                    Networking.get_instance().send_to_all_client(event)
                else:
                    Networking.get_instance().send_to_server(event)

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], MEDIA_CONSTS.FLASHPOINT_BACKGROUND)
        self.sprite_grp.add(background_box)

    def create_butn_img(self, x, y, width, height, path: str, count: int):
        label = self.create_label(x, y, width, height, count)
        self.label_grp.add(label)
        self.sprite_grp.add(label)

        box_size = (width, height)
        self.this_img = RectButton(x, y, box_size[0], box_size[1], path)

        role: PlayerRoleEnum = self.decide_enum(count)

        self.this_img.on_click(self.click_img, label, role)

        self.sprite_grp.add(self.this_img)

    @staticmethod
    def decide_enum(count: int):
        if count == 1:
            return PlayerRoleEnum.CAFS

        elif count == 2:
            return PlayerRoleEnum.DRIVER

        elif count == 3:
            return PlayerRoleEnum.CAPTAIN

        elif count == 4:
            return PlayerRoleEnum.GENERALIST

        elif count == 5:
            return PlayerRoleEnum.HAZMAT

        elif count == 6:
            return PlayerRoleEnum.IMAGING

        elif count == 7:
            return PlayerRoleEnum.PARAMEDIC

        elif count == 8:
            return PlayerRoleEnum.RESCUE

        elif count == 9:
            return PlayerRoleEnum.DOGE

        elif count == 10:
            return PlayerRoleEnum.VETERAN

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), text, Color.GREEN2))
        self.buttonBack.change_bg_image(MEDIA_CONSTS.WOOD)
        self.buttonBack.add_frame(MEDIA_CONSTS.FRAME)
        self.sprite_grp.add(self.buttonBack)

    def _init_title_text(self):
        box_size = (400, 50)
        self.text_title = RectButton(400, 60, box_size[0], box_size[1], Color.BLACK, 0,
                                     Text(pygame.font.SysFont('Agency FB', 35), "Character Selection", Color.GREEN2))
        self.text_title.change_bg_image(MEDIA_CONSTS.WOOD)
        self.text_title.add_frame(MEDIA_CONSTS.FRAME)
        self.sprite_grp.add(self.text_title)

    def _init_btn_confirm(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonConfirm = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                        Text(pygame.font.SysFont('Agency FB', 25), text, Color.GREEN2))
        self.buttonConfirm.change_bg_image(MEDIA_CONSTS.WOOD)
        self.buttonConfirm.add_frame(MEDIA_CONSTS.FRAME)
        self.sprite_grp.add(self.buttonConfirm)

    def create_label(self, x_pos: int, y_pos: int, width: int, height: int, count: int):

        role: PlayerRoleEnum = self.decide_enum(count)

        accept = True

        if any([player.role == role for player in self._game.players]):
            accept = False

        if not accept:
            label =  RectLabel(x_pos - 15, y_pos - 15, width + 30, height + 30, Color.RED)
            label.change_bg_image(MEDIA_CONSTS.WOOD)
            return label
        else:
            label =  RectLabel(x_pos - 15, y_pos - 15, width + 30, height + 30, Color.GREEN)
            label.change_bg_image(MEDIA_CONSTS.WOOD)
            return label

    def set_color(self, sprite: pygame.sprite.Sprite, i: int=0, enum:PlayerRoleEnum=None):
        accept = True
        role = self.decide_enum(i) if i else enum
        if any([player.role == role for player in self._game.players]):
            accept = False
        if isinstance(sprite, RectLabel):
            if accept:
                #sprite.change_color(Color.GREEN)
                pygame.draw.rect(sprite.image, Color.GREEN, [0, 0, 130, 180], 7)
            else:
                #sprite.change_color(Color.RED)
                pygame.draw.rect(sprite.image, Color.RED, [0, 0, 130, 180], 7)
            if self.character_enum == role:
                #sprite.change_color(Color.WHITE)
                pygame.draw.rect(sprite.image, Color.WHITE, [0, 0, 130, 180], 7)

    def click_img(self, btn, enum: PlayerRoleEnum):
        self.character_enum = enum
        self.set_color(btn, enum=enum)

    def update(self, event_queue: EventQueue):
        for i, sprite in enumerate(self.label_grp, 1):
            self.set_color(sprite, i)
        self.sprite_grp.update(event_queue)
