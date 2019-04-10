from abc import abstractmethod
from typing import List

from src.models.game_units.poi_model import POIModel
from src.observers.observer import Observer


class GameBoardObserver(Observer):

    @abstractmethod
    def notify_active_poi(self, active_pois: List[POIModel]):
        pass
