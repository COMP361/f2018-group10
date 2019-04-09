import logging

from src.constants.custom_event_enums import CustomEventEnum
from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue
from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_units.player_model import PlayerModel
from src.models.game_state_model import GameStateModel

logger = logging.getLogger("FlashPoint")


class CommandPermissionEvent(TurnEvent):
    """
    Event for asking permission from a player to be commanded
    """

    def __init__(self, source: PlayerModel, target: PlayerModel):
        super().__init__()
        self._source = source
        self._target = target
        self.game: GameStateModel = GameStateModel.instance()
        self.game_board = self.game.game_board

    def execute(self):
        logger.info(f"Player {self._source.nickname} is asking you for command permission")
        EventQueue.post(CustomEvent(CustomEventEnum.PERMISSION_PROMPT, source=self._source, target=self._target))
