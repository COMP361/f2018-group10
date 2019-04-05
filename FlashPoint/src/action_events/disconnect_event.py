import logging

from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.action_events.action_event import ActionEvent

logger = logging.getLogger("FlashPoint")


class DisconnectEvent(ActionEvent):
    def __init__(self, player: PlayerModel):
        super().__init__()
        self._player = player

    def execute(self, *args, **kwargs):
        logger.info(f"Player at {self._player.ip} has disconnected")
        GameStateModel.instance().remove_player(self._player)
