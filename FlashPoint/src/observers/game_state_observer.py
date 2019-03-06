from abc import abstractmethod

from src.observers.observer import Observer


class GameStateObserver(Observer):

    @abstractmethod
    def notify_player_index(self, player_index: int):
        pass
