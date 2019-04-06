import pygame
import logging as logger
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.constants.state_enums import PlayerRoleEnum, PlayerStatusEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.observers.player_observer import PlayerObserver
import src.constants.color as Color


class PlayerBox(PlayerObserver):

    def __init__(self, text_position, background_position, username: str, player: PlayerModel, color: Color):
        super().__init__()
        self._game = GameStateModel.instance()
        self._assoc_player = player
        self._assoc_player.add_observer(self)
        self.player_username = username
        self.txt_pos = text_position
        self.background_position = background_position
        self.text_box = self._init_text_box(color)
        self.background = RectLabel(self.background_position[0], self.background_position[1],
                                    self.background_position[2],
                                    self.background_position[3],
                                    self.get_path_from_character_enum(self._assoc_player.role))

    def _init_text_box(self, color: Color):

        box_size = (self.txt_pos[2], self.txt_pos[3])

        user_box = RectLabel(self.txt_pos[0], self.txt_pos[1], box_size[0], box_size[1], color, 0,
                             Text(pygame.font.SysFont('Arial', 20), self.player_username, (0, 255, 0, 0)))
        return user_box

    def get_path_from_character_enum(self, enum: PlayerRoleEnum):
        if enum == PlayerRoleEnum.CAFS:
            return "media/specialist_cards/cafs_firefighter.png"
        elif enum == PlayerRoleEnum.CAPTAIN:
            return "media/specialist_cards/fire_captain.png"
        elif enum == PlayerRoleEnum.GENERALIST:
            return "media/specialist_cards/generalist.png"
        elif enum == PlayerRoleEnum.DRIVER:
            return "media/specialist_cards/driver_operator.png"
        elif enum == PlayerRoleEnum.HAZMAT:
            return "media/specialist_cards/hazmat_technician.png"
        elif enum == PlayerRoleEnum.IMAGING:
            return "media/specialist_cards/imaging_technician.png"
        elif enum == PlayerRoleEnum.PARAMEDIC:
            return "media/specialist_cards/paramedic.png"
        elif enum == PlayerRoleEnum.RESCUE:
            return "media/specialist_cards/rescue_specialist.png"
        elif enum == PlayerRoleEnum.FAMILY:
            return "media/specialist_cards/family.png"
        elif enum == PlayerRoleEnum.DOGE:
            return "media/specialist_cards/doge.png"
        elif enum == PlayerRoleEnum.VETERAN:
            return "media/specialist_cards/veteran.png"

    def draw(self, screen):
        self.text_box.draw(screen)
        if self.background:
            self.background.draw(screen)

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

    def player_role_changed(self, role: PlayerRoleEnum):
        logger.info(f"new role: {role}")
        role_path = self.get_path_from_character_enum(role)
        self.background = (RectLabel(self.background_position[0], self.background_position[1], self.background_position[2],
                                     self.background_position[3], role_path))
