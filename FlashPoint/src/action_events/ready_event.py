from src.constants.state_enums import PlayerStatusEnum
from src.models.game_state_model import GameStateModel
from src.action_events.action_event import ActionEvent
from src.models.game_units.player_model import PlayerModel


class ReadyEvent(ActionEvent):
    """Event to signal that this player has clicked Ready and is ready to play the game."""

    def __init__(self, player: PlayerModel,ready:bool):
        super().__init__()
        self._player = player
        self._ready = ready

    def execute(self):
        with GameStateModel.lock:
            if self._ready:
                GameStateModel.instance().get_player_by_ip(self._player.ip).status = PlayerStatusEnum.READY
            else:
                GameStateModel.instance().get_player_by_ip(self._player.ip).status = PlayerStatusEnum.NOT_READY
