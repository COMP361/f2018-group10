from abc import ABC, abstractmethod

import src.constants.color as Color
from src.constants.state_enums import PlayerStatusEnum
from src.observers.observer import Observer


class PlayerObserver(Observer, ABC):
    """
    Base class for any observer that needs to get updates about the PlayerModel. Implement all methods here to
    specify what should happen in your class whenever one of these attributes changes.
    """

    @abstractmethod
    def player_status_changed(self, status: PlayerStatusEnum):
        pass

    @abstractmethod
    def player_ap_changed(self, updated_ap: int):
        pass

    @abstractmethod
    def player_special_ap_changed(self, updated_ap: int):
        pass

    @abstractmethod
    def player_position_changed(self, x_pos: int, y_pos: int):
        pass

    @abstractmethod
    def player_wins_changed(self, wins: int):
        pass

    @abstractmethod
    def player_losses_changed(self, losses: int):
        pass
