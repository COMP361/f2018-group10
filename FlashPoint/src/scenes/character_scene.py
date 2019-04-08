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


class CharacterScene(Scene):
    def __init__(self, screen, current_player: PlayerModel):
        self.label_grp = pygame.sprite.Group()
        self._current_player = current_player
        Scene.__init__(self, screen)
        self._init_background()
        self._game = GameStateModel.instance()

        self.create_label(0, 0, 100, 150, 1)
        self.create_butn_img(250, 150, 99, 150,
                             "media/specialist_cards/cafs_firefighter.png", 1)

        self.create_butn_img(450, 150, 100, 150,
                             "media/specialist_cards/driver_operator.png", 2)

        self.create_butn_img(650, 150, 100, 150,
                             "media/specialist_cards/fire_captain.png", 3)

        self.create_butn_img(850, 150, 99, 150,
                             "media/specialist_cards/generalist.png", 4)

        self.create_butn_img(250, 450, 100, 150,
                             "media/specialist_cards/hazmat_technician.png", 5)

        self.create_butn_img(450, 450, 99, 150,
                             "media/specialist_cards/imaging_technician.png", 6)

        self.create_butn_img(650, 450, 99, 150,
                             "media/specialist_cards/paramedic.png", 7)

        self.create_butn_img(850, 450, 98, 150,
                             "media/specialist_cards/rescue_specialist.png", 8)

        self._init_btn_back(20, 20, "Back", Color.STANDARDBTN, Color.BLACK)

        self._init_btn_confirm(1050, 575, "Confirm", Color.STANDARDBTN, Color.BLACK)

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
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/backgrounds/flashpoint_background.png")
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

        else:
            return PlayerRoleEnum.RESCUE

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), text, Color.GREEN2))
        self.buttonBack.change_bg_image('media/GameHud/wood2.png')
        self.buttonBack.add_frame('media/GameHud/frame.png')
        self.sprite_grp.add(self.buttonBack)

    def _init_title_text(self):
        box_size = (400, 50)
        self.text_title = RectButton(400, 60, box_size[0], box_size[1], Color.BLACK, 0,
                                     Text(pygame.font.SysFont('Agency FB', 35), "Character Selection", Color.GREEN2))
        self.text_title.change_bg_image('media/GameHud/wood2.png')
        self.text_title.add_frame('media/GameHud/frame.png')
        self.sprite_grp.add(self.text_title)

    def _init_btn_confirm(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonConfirm = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                        Text(pygame.font.SysFont('Arial', 25), text, Color.GREEN2))
        self.buttonConfirm.change_bg_image('media/GameHud/wood2.png')
        self.buttonConfirm.add_frame('media/GameHud/frame.png')
        self.sprite_grp.add(self.buttonConfirm)

    def create_label(self, x_pos: int, y_pos: int, width: int, height: int, count: int):

        role: PlayerRoleEnum = self.decide_enum(count)

        accept = True

        if any([player.role == role for player in self._game.players]):
            accept = False

        if not accept:
            label =  RectLabel(x_pos - 15, y_pos - 15, width + 30, height + 30, Color.RED)
            label.change_bg_image('media/GameHud/wood2.png')
            return label
        else:
            label =  RectLabel(x_pos - 15, y_pos - 15, width + 30, height + 30, Color.GREEN)
            label.change_bg_image('media/GameHud/wood2.png')
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
