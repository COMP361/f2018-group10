from src.models.game_state_model import GameStateModel
from src.action_events.action_event import ActionEvent
from src.models.game_units.player_model import PlayerModel


class JoinEvent(ActionEvent):

    def __init__(self, player: PlayerModel, game: GameStateModel=None):
        super().__init__()
        self.player = player
        self.game = game

    def execute(self, game):
        game.add_player(self.player)
