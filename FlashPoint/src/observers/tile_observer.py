from abc import abstractmethod

from src.constants.state_enums import SpaceStatusEnum
from src.observers.observer import Observer


class TileObserver(Observer):
    """ABC for classes concerned with getting tile state."""

    @abstractmethod
    def tile_status_changed(self, status: SpaceStatusEnum):
        pass
