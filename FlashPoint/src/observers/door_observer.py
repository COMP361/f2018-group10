from abc import ABC, abstractmethod
from src.constants.state_enums import DoorStatusEnum
from src.observers.observer import Observer

class DoorObserver(Observer, ABC):

    @abstractmethod
    def door_status_changed(self, status:DoorStatusEnum):
        pass
