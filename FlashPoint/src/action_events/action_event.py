from abc import ABC, abstractmethod


class ActionEvent(ABC):
    """Abstract base class for all ActionEvent types. Should contain all information needed to
        update game state on remote clients."""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def execute(self):
        pass
