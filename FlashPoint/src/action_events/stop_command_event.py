import logging

from src.action_events.action_event import ActionEvent
from src.models.game_units.player_model import PlayerModel
from src.models.game_state_model import GameStateModel

logger = logging.getLogger("FlashPoint")


class StopCommandEvent(ActionEvent):

    def __init__(self, source: PlayerModel):
        super().__init__()
        self._source = source

    def execute(self, *args, **kwargs):
        GameStateModel.instance().command = (None, None)
        logger.info(f"Player {self._source.nickname} stopped commanding")
