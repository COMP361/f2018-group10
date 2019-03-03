from abc import ABC, abstractmethod

from src.models.game_state_model import GameStateModel


class ActionEvent(ABC):
    """Abstract base class for all ActionEvent types. Should contain all information needed to
        update game state on remote clients."""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def has_required_AP(self, playerAP: int, requiredAP: int) -> bool:
        if playerAP < requiredAP:
            return False

        return True
