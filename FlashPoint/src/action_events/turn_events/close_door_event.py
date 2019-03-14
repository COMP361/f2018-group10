from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_board.door_model import DoorModel
from src.models.game_state_model import GameStateModel


class CloseDoorEvent(TurnEvent):

    def __init__(self, door: DoorModel):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        self.door = game.game_board.get_tile_at(door.id[0], door.id[1]).get_obstacle_in_direction(door.id[2])
        self.fireman = game.players_turn

    def execute(self):
        print("Executing CloseDoorEvent")
        self.door.close_door()
        self.fireman.ap = self.fireman.ap - 1
