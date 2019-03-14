from abc import abstractmethod

from src.constants.state_enums import GameStateEnum
from src.observers.observer import Observer


class GameStateObserver(Observer):

    @abstractmethod
    def notify_player_index(self, player_index: int):
        pass

    @abstractmethod
    def notify_game_state(self, game_state: GameStateEnum):
        pass
    @abstractmethod
    def damage_changed(self,new_damage:int):
        pass

    @abstractmethod
    def saved_victims(self,victims_saved:int):
        pass

    @abstractmethod
    def dead_victims(self,victims_dead:int):
        pass
