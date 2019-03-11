from src.action_events.turn_events.turn_event import TurnEvent
from src.core.flashpoint_exceptions import NotEnoughAPException
from src.models.game_board.door_model import DoorModel
from src.models.game_units.player_model import PlayerModel


class CloseDoorEvent(TurnEvent):

    def __init__(self, door: DoorModel, fireman: PlayerModel):
        super().__init__()
        self.door = door
        self.fireman = fireman

    def execute(self):
        self.door.close_door()
        self.fireman.ap -= 1
