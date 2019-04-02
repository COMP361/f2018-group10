import logging

from src.constants.state_enums import PlayerRoleEnum, GameKindEnum
from src.core.flashpoint_exceptions import WrongEventInstantiation
from src.models.game_state_model import GameStateModel
from src.action_events.action_event import ActionEvent
from src.models.game_units.player_model import PlayerModel


logger = logging.getLogger("FlashPoint")


class ChooseCharacterEvent(ActionEvent):

    def __init__(self, role: PlayerRoleEnum, player_index: int):
        super().__init__()
        self._game: GameStateModel = GameStateModel.instance()
        if self._game.rules == GameKindEnum.FAMILY:
            raise WrongEventInstantiation(self)
        self._player_index = player_index
        self._role: PlayerRoleEnum = role
        self.curr_player: PlayerModel = self._game.players[player_index]

    def execute(self):
        logger.info("Executing ChooseCharacterEvent")
        self.curr_player.role = self.role
