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
        self._role: PlayerRoleEnum = role
        self.curr_player: PlayerModel = game.players[player_index]

    def execute(self):
        logger.info(f"Executing ChangeCrewEvent: {self._role}")
        self.curr_player.role = self._role
