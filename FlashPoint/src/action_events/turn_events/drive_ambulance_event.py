from typing import Tuple
import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel

logger = logging.getLogger("FlashPoint")


class DriveAmbulanceEvent(TurnEvent):
    """Move the Ambulance and all its passengers to the designated spot. Assumes passengers have already climbed on."""

    def __init__(self, parking_spot: Tuple[TileModel, TileModel] = None):
        super().__init__()
        self._player: PlayerModel = GameStateModel.instance().players_turn
        self._row = min(tile.row for tile in parking_spot) if parking_spot else -1
        self._column = min(tile.column for tile in parking_spot) if parking_spot else -1
        self._board_model: GameBoardModel = GameStateModel.instance().game_board

    def execute(self, *args, **kwargs):
        logger.info("Executing DriveAmbulance Event")
        destination_first_tile = self._board_model.get_tile_at(self._row, self._column)
        destination_second_tile = self._board_model.get_other_parking_tile(destination_first_tile)

        ap_multiplier = self._board_model.get_distance_to_parking_spot(
            (destination_first_tile, destination_second_tile))
        self._player.ap = self._player.ap - 2*ap_multiplier

        self._board_model.ambulance.drive((self._row, self._column))


