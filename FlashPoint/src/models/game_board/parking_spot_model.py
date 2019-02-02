from typing import Tuple

from models.game_board.TileModel import TileModel
from models.game_units.GameUnit import GameUnit
from models.game_units.VehicleModel import VehicleModel
from src.constants.enums.vehicle_kind_enum import VehicleKindEnum


class ParkingSpotModel(GameUnit):

    def __init__(self, tiles: Tuple[TileModel, TileModel], vehicle_kind: VehicleKindEnum):
        super().__init__(tiles[0])
        self._vehicle_kind = vehicle_kind

    def _validate_tile(self, tile: TileModel):
        # TODO: Implement this to only allow outside tiles.
        pass

    def park(self, vehicle: VehicleModel):
        """Associate a vehicle to this parking spot."""
