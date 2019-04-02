from abc import abstractmethod
from typing import List

from src.constants.state_enums import SpaceStatusEnum
from src.models.model import Model
from src.observers.observer import Observer


class TileObserver(Observer):
    """ABC for classes concerned with getting tile state."""

    @abstractmethod
    def tile_status_changed(self, status: SpaceStatusEnum):
        pass

    @abstractmethod
    def tile_assoc_models_changed(self, assoc_models: List[Model]):
        pass

    @abstractmethod
    def tile_hotspot_changed(self, is_hotspot: bool):
        pass
