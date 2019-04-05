from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.action_events.action_event import ActionEvent


class DisconnectEvent(ActionEvent):
    def __init__(self, player: PlayerModel):
        super().__init__()
        self._player = player

    def execute(self, *args, **kwargs):
        GameStateModel.instance().remove_player(self._player)
