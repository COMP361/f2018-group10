from typing import Optional
from abc import ABC, abstractmethod

from src.models.game_board.tile_model import TileModel


class GameUnit(ABC):
    """
    Abstract base class for GameUnit type objects.
    These include almost all game objects which are contained on Tiles, such as PlayerModel, POIModel, etc.
    """

    def __init__(self, tile: Optional[TileModel]):
        super().__init__()
        # TODO Consider empty tile type
        self._tile = tile

    @abstractmethod
    def _validate_tile(self, tile: TileModel) -> bool:
        pass

    @property
    def tile(self):
        return self._tile

    @tile.setter
    def tile(self, tile: TileModel):
        if self._validate_tile(tile):
            self._tile = tile
        else:
            # TODO: Raise exception
            pass
