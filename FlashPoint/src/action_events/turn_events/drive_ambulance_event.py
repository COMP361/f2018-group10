from typing import Tuple

from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import VehicleOrientationEnum
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel


class DriveAmbulanceEvent(TurnEvent):
    """Move the Ambulance and all its passengers to the designated spot. Assumes passengers have already climbed on."""

    def __init__(self, parking_spot: Tuple[TileModel] = None):
        super().__init__()
        self._player: PlayerModel = GameStateModel.instance().players_turn
        self._row = min(tile.row for tile in parking_spot) if parking_spot else -1
        self._column = min(tile.column for tile in parking_spot) if parking_spot else -1
        self._board_model = GameStateModel.instance().game_board

    def _determine_distance(self, original_orientation: VehicleOrientationEnum) -> int:
        """Find out how many parking spaces between this vehicle and the chosen spot.
            :return 1 for 1 spot, 2 for 2 spots"""
        # If the chosen spot would cause the vehicle to go from vertical to horizontal or visa versa, its 1 away
        # Otherwise, its on the other side of the board so 2 away.
        return 1 if self._board_model.ambulance.orientation != original_orientation else 2

    def execute(self, *args, **kwargs):
        original_orientation = self._board_model.ambulance.orientation
        self._board_model.ambulance.drive((self._row, self._column))

        ap_multiplier = self._determine_distance(original_orientation)
        self._player.ap = self._player.ap - 2*ap_multiplier

