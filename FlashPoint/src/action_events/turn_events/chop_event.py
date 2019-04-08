import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import PlayerRoleEnum
from src.models.game_state_model import GameStateModel
from src.models.game_board.wall_model import WallModel

logger = logging.getLogger("FlashPoint")


class ChopEvent(TurnEvent):

    def __init__(self, wall: WallModel):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        self.player = game.players_turn
        self.wall = game.game_board.get_tile_at(wall.id[0], wall.id[1]).get_obstacle_in_direction(wall.id[2])

    def execute(self):
        logger.info("Executing Chop Event")
        GameStateModel.lock.acquire()
        game: GameStateModel = GameStateModel.instance()
        self.wall.inflict_damage()
        if self.player.role == PlayerRoleEnum.RESCUE:
            self.player.ap = self.player.ap - 1
        else:
            self.player.ap = self.player.ap - 2
        game.damage = game.damage + 1
        GameStateModel.lock.release()
