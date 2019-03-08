from abc import abstractmethod

from src.models.game_units.player_model import PlayerModel
from src.observers.observer import Observer


class GameStateObserver(Observer):

    @abstractmethod
    def notify_player_index(self, player_index: int):
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
