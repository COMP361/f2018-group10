import pygame
import logging as logger
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.constants.state_enums import PlayerRoleEnum, PlayerStatusEnum, GameStateEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.observers.player_observer import PlayerObserver
import src.constants.color as Color
import src.constants.media_constants as MEDIA_CONSTS


class PlayerBox(PlayerObserver):

    def __init__(self, text_position, background_position, username: str, player: PlayerModel, color: Color):
        super().__init__()
        self._game:GameStateModel = GameStateModel.instance()
        self._assoc_player = player
        self._assoc_player.add_observer(self)
        self.player_username = username
        self.txt_pos = text_position
        self.background_position = background_position
        self.text_box = self._init_text_box(color)
        self.background = RectLabel(self.background_position[0], self.background_position[1],
                                    self.background_position[2],
                                    self.background_position[3],
                                    )
        self.background.change_bg_image(MEDIA_CONSTS.WOOD)
        self.background.add_frame(self.get_path_from_character_enum(self._assoc_player.role))
        self.background.add_frame(MEDIA_CONSTS.FRAME)

    def delete_class(self):
        self._assoc_player.remove_observer(self)

    def _init_text_box(self, color: Color):

        box_size = (self.txt_pos[2], self.txt_pos[3])

        user_box = RectLabel(self.txt_pos[0], self.txt_pos[1], box_size[0], box_size[1], color, 0,
                             Text(pygame.font.SysFont('Agency FB', 27), self.player_username, color))
        user_box.change_bg_image(MEDIA_CONSTS.WOOD)
        user_box.add_frame(MEDIA_CONSTS.FRAME)
        return user_box

    def get_path_from_character_enum(self, enum: PlayerRoleEnum):
        if enum == PlayerRoleEnum.CAFS:
            return MEDIA_CONSTS.CAFS_FIREFIGHTER
        elif enum == PlayerRoleEnum.CAPTAIN:
            return MEDIA_CONSTS.FIRE_CAPTAIN
        elif enum == PlayerRoleEnum.GENERALIST:
            return MEDIA_CONSTS.GENERALIST
        elif enum == PlayerRoleEnum.DRIVER:
            return MEDIA_CONSTS.DRIVER_OPERATOR
        elif enum == PlayerRoleEnum.HAZMAT:
            return MEDIA_CONSTS.HAZMAT_TECHNICIAN
        elif enum == PlayerRoleEnum.IMAGING:
            return MEDIA_CONSTS.IMAGING_TECHNICIAN
        elif enum == PlayerRoleEnum.PARAMEDIC:
            return MEDIA_CONSTS.PARAMEDIC
        elif enum == PlayerRoleEnum.RESCUE:
            return MEDIA_CONSTS.RESCUE_SPECIALIST
        elif enum == PlayerRoleEnum.FAMILY:
            return MEDIA_CONSTS.FAMILY
        elif enum == PlayerRoleEnum.DOGE:
            return MEDIA_CONSTS.DOGE
        elif enum == PlayerRoleEnum.VETERAN:
            return MEDIA_CONSTS.VETERAN

    def draw(self, screen):
        self.text_box.draw(screen)
        if self.background:
            self.background.draw(screen)
            self.background.change_bg_image(MEDIA_CONSTS.WOOD)
            self.background.add_frame(self.get_path_from_character_enum(self._assoc_player.role))
            self.background.add_frame(MEDIA_CONSTS.FRAME)

    def player_status_changed(self, status: PlayerStatusEnum):
        pass

    def player_ap_changed(self, updated_ap: int):
        pass

    def player_special_ap_changed(self, updated_ap: int):
        pass

    def player_position_changed(self, row: int, column: int):
        pass

    def player_wins_changed(self, wins: int):
        pass

    def player_losses_changed(self, losses: int):
        pass

    def player_carry_changed(self, carry):
        pass

    def player_leading_victim_changed(self, leading_victim):
        pass

    def player_role_changed(self, role: PlayerRoleEnum):
        if self._game.state == GameStateEnum.READY_TO_JOIN:
            logger.info(f"new role: {role}")
            role_path = self.get_path_from_character_enum(role)
            logger.info(f"Role Path is: {role_path}")
            self.background = (RectLabel(self.background_position[0], self.background_position[1], self.background_position[2],
                                         self.background_position[3], role_path))
