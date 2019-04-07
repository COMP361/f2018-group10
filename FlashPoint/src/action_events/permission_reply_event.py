import logging

from src.action_events.action_event import ActionEvent
from src.models.game_units.player_model import PlayerModel
from src.models.game_state_model import GameStateModel

logger = logging.getLogger("FlashPoint")


class PermissionReplyEvent(ActionEvent):

    def __init__(self, reply: bool, source: PlayerModel, target: PlayerModel):
        super().__init__()
        self._reply = reply
        self._source = source
        self._target = target

    def execute(self, *args, **kwargs):
        if self._reply:
            GameStateModel.instance().command = (self._source, self._target)
            logger.info(f"Player {self._source.nickname} now commands {self._target.nickname}")
