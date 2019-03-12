from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_board.door_model import DoorModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel


class OpenDoorEvent(TurnEvent):

    def __init__(self, door: DoorModel):
        super().__init__()
        self.door = door
        self.fireman: PlayerModel = GameStateModel.instance().players_turn

    def execute(self):
        door = self.door
        fireman = self.fireman
        # TODO: Start here - This is the precondition code - Move it to the GUI
        # if not self.has_required_AP(fireman.ap, 1):
        #     raise NotEnoughAPException("open the door", 1)
        # End here

        door.open_door()
        fireman.ap -= 1
