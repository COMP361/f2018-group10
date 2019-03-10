from abc import ABC, abstractmethod

from src.constants.state_enums import PlayerStatusEnum, VictimStateEnum
from src.observers.observer import Observer


class VictimObserver(Observer, ABC):
    """
    Base class for any observer that needs to get updates about the VictimModel. Implement all methods here to
    specify what should happen in your class whenever one of these attributes changes.
    """

    @abstractmethod
    def victim_state_changed(self, state: VictimStateEnum):
        pass

    @abstractmethod
    def victim_position_changed(self, row: int, column: int):
        pass
