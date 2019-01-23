from typing import Tuple

from models.game_board.TileModel import TileModel
from models.game_units.GameUnit import GameUnit
from src.constants.enums.VehicleKindEnum import VehicleKindEnum


class ParkingSpotModel(GameUnit):

    def __init__(self, tiles: Tuple[TileModel, TileModel], vehicle_kind: VehicleKindEnum):
        # Fix call to super to only use 1 tile (or none)
        super().__init__(tiles[0])
        self._vehicle_kind = vehicle_kind

    def _validate_tile(self, tile: TileModel):
        # TODO: Implement this to only allow outside tiles.
        pass
