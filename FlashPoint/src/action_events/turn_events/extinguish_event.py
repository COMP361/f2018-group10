import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import SpaceStatusEnum
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel

logger = logging.getLogger("FlashPoint")


class ExtinguishEvent(TurnEvent):

    def __init__(self, extinguish_space: TileModel):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        self.fireman: PlayerModel = game.players_turn
        self.extinguish_space: TileModel = game.game_board.get_tile_at(extinguish_space.row, extinguish_space.column)

    def execute(self):
        logger.info(f"Executing ExtinguishEvent on {self.extinguish_space}")
        fireman = self.fireman
        extinguish_space = self.extinguish_space

        if extinguish_space.space_status == SpaceStatusEnum.SMOKE:
            extinguish_space.space_status = SpaceStatusEnum.SAFE

        elif extinguish_space.space_status == SpaceStatusEnum.FIRE:
            extinguish_space.space_status = SpaceStatusEnum.SMOKE

        else:
            return

        fireman.ap = fireman.ap - 1

        return
