from abc import ABC, abstractmethod
from src.constants.state_enums import DoorStatusEnum
from src.observers.observer import Observer


class HazmatObservers(Observer, ABC):

    @abstractmethod
    def hazmat_status_changed(self):
        pass
