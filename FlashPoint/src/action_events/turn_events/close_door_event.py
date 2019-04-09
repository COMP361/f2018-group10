import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_board.door_model import DoorModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_state_model import GameStateModel

logger = logging.getLogger("FlashPoint")


class CloseDoorEvent(TurnEvent):

    def __init__(self, door: DoorModel):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        self.door = game.game_board.get_tile_at(door.id[0], door.id[1]).get_obstacle_in_direction(door.id[2])
        # Check if player is commanding
        if game.players_turn == game.command[0]:
            self.source: PlayerModel = game.command[0]
            self.fireman: PlayerModel = game.command[1]
        else:
            self.source = None
            self.fireman: PlayerModel = game.players_turn

    def execute(self):
        logger.info("Executing CloseDoorEvent")
        self.door.close_door()
        if self.source:
            fireman = self.source
        else:
            fireman = self.fireman
        fireman.ap = fireman.ap - 1
