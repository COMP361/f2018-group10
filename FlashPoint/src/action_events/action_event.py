from abc import ABC, abstractmethod


class ActionEvent(ABC):
    """Abstract base class for all ActionEvent types. Checks if player has enough AP to execute
    a move and has an exec() method."""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def execute(self):
        pass
