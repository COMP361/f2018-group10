from src.action_events.turn_events.turn_event import TurnEvent
from src.core.flashpoint_exceptions import NotEnoughAPException
from src.models.game_board.door_model import DoorModel
from src.models.game_units.player_model import PlayerModel


class CloseDoorEvent(TurnEvent):

    def __init__(self):
        super().__init__()

    def execute(self, door: DoorModel, fireman: PlayerModel):
        # TODO: Start here - This is the precondition code - Move it to the GUI
        if not self.has_required_AP(fireman.ap, 1):
            raise NotEnoughAPException("close the door", 1)
        # End here

        door.close_door()
