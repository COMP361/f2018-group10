from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_board.wall_model import WallModel


class ChopEvent(TurnEvent):

    def __init__(self, fireman: PlayerModel, wall: WallModel):
        super().__init__()
        self.player = fireman
        self.wall = wall

    def execute(self):
        game: GameStateModel = GameStateModel.instance()
        self.wall.inflict_damage()
        self.player.ap -= 2
        game.damage += 1
