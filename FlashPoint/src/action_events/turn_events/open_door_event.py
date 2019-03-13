from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_board.door_model import DoorModel
from src.models.game_units.player_model import PlayerModel


class OpenDoorEvent(TurnEvent):

    def __init__(self, door: DoorModel, fireman: PlayerModel):
        super().__init__()
        self.door = door
        self.fireman = fireman

    def execute(self):
        door = self.door
        fireman = self.fireman
        door.open_door()
        fireman.ap -= 1
