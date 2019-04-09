import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import PlayerRoleEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel

logger = logging.getLogger("FlashPoint")


class CrewChangeEvent(TurnEvent):

    def __init__(self, role: PlayerRoleEnum, player_index: int):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        self._player_index = player_index
        logger.info(f"ROLE IS: {role}")
        if isinstance(role, int):
            self._role = self.determine_enum(role)
        else:
            self._role: PlayerRoleEnum = role
        self.curr_player: PlayerModel = game.players[player_index]

    def execute(self):
        logger.info(f"Executing ChangeCrewEvent: {self._role}")
        self.curr_player.role = self._role
        if self.curr_player.role == PlayerRoleEnum.CAPTAIN:
            self.curr_player.special_ap = 2
            self.curr_player.ap -= 2
        elif self.curr_player.role == PlayerRoleEnum.CAFS:
            self.curr_player.ap = self.curr_player.ap - 3
            self.curr_player.special_ap = 3

        elif self.curr_player.role == PlayerRoleEnum.GENERALIST:
            self.curr_player.ap = self.curr_player.ap + 1 - 2

        elif self.curr_player.role == PlayerRoleEnum.RESCUE:
            self.curr_player.special_ap = 3
            self.curr_player.ap -= 2

        elif self.curr_player.role == PlayerRoleEnum.DOGE:
            self.curr_player.ap = self.curr_player.ap + 8 - 2
        else:
            self.curr_player.ap -= 2

        self.curr_player._notify_role()


    def determine_enum(self, role):
        if role == 1:
            return PlayerRoleEnum.CAFS
        elif role == 2:
            return PlayerRoleEnum.DRIVER
        elif role == 4:
            return PlayerRoleEnum.CAPTAIN
        elif role == 5:
            return PlayerRoleEnum.GENERALIST
        elif role == 6:
            return PlayerRoleEnum.HAZMAT
        elif role == 7:
            return PlayerRoleEnum.IMAGING
        elif role == 8:
            return PlayerRoleEnum.PARAMEDIC
        elif role == 9:
            return PlayerRoleEnum.RESCUE
        elif role == 10:
            return PlayerRoleEnum.DOGE
        elif role == 11:
            return PlayerRoleEnum.VETERAN
