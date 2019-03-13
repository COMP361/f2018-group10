from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_board.door_model import DoorModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel


class OpenDoorEvent(TurnEvent):

    def __init__(self, door: DoorModel, fireman: PlayerModel):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        self.door = game.game_board.get_tile_at(door.id[0], door.id[1]).get_obstacle_in_direction(door[2])
        self.fireman = game.players_turn

    def execute(self):
        door = self.door
        fireman = self.fireman
        door.open_door()
        fireman.ap -= 1
