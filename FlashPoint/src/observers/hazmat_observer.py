from abc import ABC, abstractmethod
from src.observers.observer import Observer


class HazmatObserver(Observer, ABC):

    @abstractmethod
    def hazmat_position_changed(self, row: int, col: int):
        pass
