from abc import ABC
from typing import List

from observers.observer import Observer


class Model(ABC):
    """
    Abstract base class for Model type objects.
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
        """
        CAUTION: remove() uses __eq__ to test equality, and by default is only shallow. (Checks address only).
        Be sure to implement __eq__ in your Observer class to not have any surprises!
        """
        self._observers.remove(obs)
