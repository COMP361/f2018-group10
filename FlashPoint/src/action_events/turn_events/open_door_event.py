import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_board.door_model import DoorModel
from src.models.game_state_model import GameStateModel

logger = logging.getLogger("FlashPoint")


class OpenDoorEvent(TurnEvent):

    def __init__(self, door: DoorModel):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        self.door = game.game_board.get_tile_at(door.id[0], door.id[1]).get_obstacle_in_direction(door.id[2])
        self.fireman = game.players_turn

    def execute(self):
        logger.info("Executing OpenDoorEvent")
        door = self.door
        fireman = self.fireman
        door.open_door()
        fireman.ap = fireman.ap - 1
