from abc import ABC, abstractmethod

from src.constants.state_enums import VehicleOrientationEnum
from src.observers.observer import Observer


class VehicleObserver(Observer, ABC):

    @abstractmethod
    def notify_vehicle_pos(self, orientation: VehicleOrientationEnum, row: int, column: int):
        pass
