from src.action_events.action_event import ActionEvent
from src.models.game_state_model import GameStateModel


class SelectCharacterEvent(ActionEvent):

    def __init__(self,current_player,character):
        super().__init__()
        self._player = current_player
        self._character = character


    def execute(self, *args, **kwargs):

        GameStateModel.instance().get_player_by_ip(self._player.ip).character = self._character