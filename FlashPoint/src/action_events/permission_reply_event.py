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
        game: GameStateModel = GameStateModel.instance()
        if self._reply:
            game.command = (self._source, self._target)
            commander: PlayerModel = [player for player in game.players if player == self._source][0]
            commander.special_ap = commander.special_ap - 1
            logger.info(f"Player {self._source.nickname} now commands {self._target.nickname}")
