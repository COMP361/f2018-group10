from abc import abstractmethod

from src.models.game_units.player_model import PlayerModel
from src.observers.observer import Observer


class GameStateObserver(Observer):

    @abstractmethod
    def notify_player_index(self, player_index: int):
        pass

    # @abstractmethod
    #     # def ap_changed(self,by:int,player:PlayerModel):
    #     #     pass