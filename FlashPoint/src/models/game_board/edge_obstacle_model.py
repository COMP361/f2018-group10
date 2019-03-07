from abc import ABC
from typing import List

from src.observers.observer import Observer


class EdgeObstacleModel(ABC):
    """
    Abstract Base Class for WallModel and DoorModel. May be updated later as needed.
    """
    def __init__(self):
        super().__init__()
        self._observers = []

    @property
    def observers(self) -> List[Observer]:
        return self._observers

    def add_observer(self, obs: Observer):
        self._observers.append(obs)

    def remove_observer(self, obs: Observer):
        self._observers.remove(obs)
