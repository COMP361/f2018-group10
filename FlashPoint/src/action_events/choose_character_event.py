import logging

from src.constants.state_enums import PlayerRoleEnum, GameKindEnum
from src.core.flashpoint_exceptions import WrongEventInstantiation
from src.models.game_state_model import GameStateModel
from src.action_events.action_event import ActionEvent
from src.models.game_units.player_model import PlayerModel

logger = logging.getLogger("FlashPoint")


class ChooseCharacterEvent(ActionEvent):

    def __init__(self, role: PlayerRoleEnum,player:PlayerModel):
        super().__init__()
        self._game: GameStateModel = GameStateModel.instance()
        if self._game.rules == GameKindEnum.FAMILY:
            raise WrongEventInstantiation(self)

        self._player = player
        self._role: PlayerRoleEnum = role

    def execute(self):
        logger.info("Executing ChooseCharacterEvent")
        self._player.character = self._role
