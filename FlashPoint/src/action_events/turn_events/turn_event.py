from abc import ABC, abstractmethod

from src.models.game_state_model import GameStateModel


class TurnEvent(ABC):
    """Abstract base class for all TurnEvent types. Checks if player has enough AP to execute
    a move and has an exec() method."""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def has_required_AP(self, playerAP: int, requiredAP: int) -> bool:
        if playerAP < requiredAP:
            return False

        return True
