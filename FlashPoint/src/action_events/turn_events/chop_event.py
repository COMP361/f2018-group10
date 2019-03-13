from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_state_model import GameStateModel
from src.models.game_board.wall_model import WallModel


class ChopEvent(TurnEvent):

    def __init__(self, wall: WallModel):
        super().__init__()
        self.player = GameStateModel.instance().players_turn
        self.wall = GameStateModel.instance().game_board.get_tile_at(wall.id[0], wall.id[1]).get_obstacle_in_direction(wall.id[2])

    def execute(self):
        GameStateModel.lock.acquire()
        game: GameStateModel = GameStateModel.instance()
        self.wall.inflict_damage()
        self.player.ap -= 2
        game.damage = game.damage + 1
        GameStateModel.lock.release()
