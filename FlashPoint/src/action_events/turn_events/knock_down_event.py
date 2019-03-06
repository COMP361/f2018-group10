from src.action_events.action_event import ActionEvent
from src.models.game_units.player_model import PlayerModel

# TODO: resolve knock down. Please refer to M5 models to save some time on this:
# Player status = KnockedDown
# Player location = Nearest Ambulance
#


class KnockDownEvent(ActionEvent):

    def __init__(self, player: PlayerModel):
        super().__init__()
        self.player = player

    def execute(self):
        pass
