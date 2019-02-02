from abc import ABC, abstractmethod


class VehicleModel(ABC):
    """Base class for Ambulance and Engine"""

    def __init__(self, parking_spot):
        super().__init__()
        self._parking_spot = parking_spot

    @abstractmethod
    def drive(self, tile):
        pass
