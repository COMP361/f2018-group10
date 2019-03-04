from abc import abstractmethod

from src.observers.observer import Observer


class TileObserver(Observer):
    """ABC for classes concerned with getting tile state."""

    @abstractmethod
    def tile_associated_models_changed(self):
        pass
