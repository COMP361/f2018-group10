from action_events.action_event import ActionEvent
from models.game_units.player_model import PlayerModel


class JoinEvent(ActionEvent):

    def __init__(self, player: PlayerModel):
        super().__init__()
        self.player = player

    def execute(self):
        pass
