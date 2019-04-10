from abc import ABC, abstractmethod
from typing import List

from src.constants.state_enums import VehicleOrientationEnum
from src.models.game_units.player_model import PlayerModel
from src.observers.observer import Observer


class VehicleObserver(Observer, ABC):

    @abstractmethod
    def notify_vehicle_pos(self, orientation: VehicleOrientationEnum, row: int, column: int):
        pass

    @abstractmethod
    def notify_passengers(self, passengers: List[PlayerModel]):
        pass
