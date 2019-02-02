from models.game_units.game_unit import GameUnit
from models.game_units.vehicle_model import VehicleModel
from src.constants.state_enums import VehicleKindEnum


class ParkingSpotModel(GameUnit):

    def __init__(self, tiles, vehicle_kind: VehicleKindEnum):
        super().__init__(tiles[0])
        self._vehicle_kind = vehicle_kind

    def _validate_tile(self, tile):
        # TODO: Implement this to only allow outside tiles.
        pass

    def park(self, vehicle: VehicleModel):
        """Associate a vehicle to this parking spot."""
