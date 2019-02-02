from abc import ABC, abstractmethod

from models.game_board.ParkingSpotModel import ParkingSpotModel
from src.models.game_board.tile_model import TileModel


class VehicleModel(ABC):
    """Base class for Ambulance and Engine"""

    def __init__(self, parking_spot: ParkingSpotModel):
        super().__init__()
        self._parking_spot = parking_spot

    @abstractmethod
    def drive(self, tile: TileModel):
        pass
