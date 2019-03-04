from abc import abstractmethod

from src.constants.state_enums import POIStatusEnum
from src.observers.observer import Observer


class POIObserver(Observer):
    """Base class for getting changes regarding a POI model."""

    @abstractmethod
    def poi_status_changed(self, status: POIStatusEnum):
        pass

    @abstractmethod
    def poi_position_changed(self, x_pos: int, y_pos: int):
        pass
