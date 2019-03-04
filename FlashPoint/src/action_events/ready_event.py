from src.constants.state_enums import PlayerStatusEnum
from src.models.game_state_model import GameStateModel
from src.action_events.action_event import ActionEvent
from src.models.game_units.player_model import PlayerModel


class ReadyEvent(ActionEvent):
    """Event to signal that this player has clicked Ready and is ready to play the game."""

    def __init__(self, player: PlayerModel):
        super().__init__()
        self._player = player

    def execute(self):
        GameStateModel.instance().get_player_by_ip(self._player.ip).status = PlayerStatusEnum.READY
