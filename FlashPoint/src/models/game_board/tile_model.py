from typing import Optional, List

from src.models.game_board.door_model import DoorModel
from src.models.game_board.wall_model import WallModel
from src.models.model import Model
from src.core.flashpoint_exceptions import TilePositionOutOfBoundsException
from src.models.game_board.edge_obstacle_model import EdgeObstacleModel
from src.models.game_board.null_model import NullModel
from src.constants.state_enums import SpaceKindEnum, DoorStatusEnum, WallStatusEnum
from src.constants.state_enums import SpaceStatusEnum
from src.observers.tile_observer import TileObserver


class TileModel(Model):
    """Logical state of a Tile object."""

    def __init__(self, row: int, column: int, space_kind: SpaceKindEnum):
        super().__init__()
        self._row = row
        self._column = column
        self._space_kind = space_kind
        self._space_status = SpaceStatusEnum.SAFE
        self._is_hotspot = False
        self._associated_models = []
        self._visited = False

        self._adjacent_tiles = {
            "North": NullModel(),
            "East": NullModel(),
            "West": NullModel(),
            "South": NullModel(),
        }

        self._adjacent_edge_objects = {
            "North": NullModel(),
            "East": NullModel(),
            "West": NullModel(),
            "South": NullModel(),
        }

    def __str__(self):
        return f"Tile at: ({self.row}, {self.column})."

    def _notify_status(self):
        for obs in self.observers:
            obs.tile_status_changed(self.space_status)

    def _notify_assoc_models(self):
        for obs in self.observers:
            obs.tile_assoc_models_changed(self.associated_models)

    @property
    def observers(self) -> List[TileObserver]:
        return self._observers

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def space_kind(self):
        return self._space_kind

    @space_kind.setter
    def space_kind(self, kind: SpaceKindEnum):
        self._space_kind = kind

    @property
    def space_status(self):
        return self._space_status

    @space_status.setter
    def space_status(self, space_status: SpaceStatusEnum):
        self._space_status = space_status
        self._notify_status()

    @property
    def is_hotspot(self):
        return self._is_hotspot

    @property
    def adjacent_tiles(self):
        return self._adjacent_tiles

    @property
    def adjacent_edge_objects(self):
        return self._adjacent_edge_objects

    @property
    def north_tile(self):
        """
        Get the TileModel to the North of this one.
        :raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
        """
        tile = self._adjacent_tiles.get("North", None)
        if not tile:
            raise TilePositionOutOfBoundsException(self, "North")
        return tile

    @north_tile.setter
    def north_tile(self, tile):
        self._adjacent_tiles["North"] = tile

    @property
    def east_tile(self):
        """
        Get the TileModel to the North of this one.
        :raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
        """
        tile = self._adjacent_tiles.get("East", None)
        if not tile:
            raise TilePositionOutOfBoundsException(self, "East")
        return tile

    @east_tile.setter
    def east_tile(self, tile):
        self._adjacent_tiles["East"] = tile

    @property
    def west_tile(self):
        """
        Get the TileModel to the  of this one.
        :raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
        """
        tile = self._adjacent_tiles.get("West", None)
        if not tile:
            raise TilePositionOutOfBoundsException(self, "West")
        return tile

    @west_tile.setter
    def west_tile(self, tile):
        self._adjacent_tiles["West"] = tile

    @property
    def south_tile(self):
        """
        Get the TileModel to the South of this one.
        :raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
        """
        tile = self._adjacent_tiles.get("South", None)
        if not tile:
            raise TilePositionOutOfBoundsException(self, "South")
        return tile

    @south_tile.setter
    def south_tile(self, tile):
        self._adjacent_tiles["South"] = tile

    def set_adjacent_edge_obstacle(self, direction: str, edge_obstacle: EdgeObstacleModel):
        self._adjacent_edge_objects[direction] = edge_obstacle

    def set_adjacent_tile(self, direction: str, tile):
        self._adjacent_tiles[direction] = tile

    def get_tile_in_direction(self, direction: str):
        """
        Get the TileModel in a specified direction.
        "raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
        """
        tile = self._adjacent_tiles.get(direction, None)
        if not tile:
            raise TilePositionOutOfBoundsException(self, direction)
        return tile

    def get_obstacle_in_direction(self, direction: str) -> Optional['EdgeObstacleModel']:
        """
        Get the EdgeObstacle model
        :return: EdgeObstacleModel in the direction specified, or NullModel.
        """
        return self._adjacent_edge_objects.get(direction, NullModel())

    def has_obstacle_in_direction(self, direction: str) -> bool:
        """
        Checks whether there is an obstacle in the given direction.
        :param direction:
        :return: False if there is -
                1. no obstacle
                2. destroyed wall
                3. destroyed door
                True otherwise
        """
        obstacle: EdgeObstacleModel = self.get_obstacle_in_direction(direction)
        if isinstance(obstacle, NullModel):
            return False
        elif isinstance(obstacle, DoorModel) and obstacle.door_status == DoorStatusEnum.DESTROYED:
            return False
        elif isinstance(obstacle, WallModel) and obstacle.wall_status == WallStatusEnum.DESTROYED:
            return False
        else:
            return True

    @property
    def associated_models(self):
        return self._associated_models

    def add_associated_model(self, model: Model):
        self._associated_models.append(model)
        self._notify_assoc_models()

    def remove_associated_model(self, model: Model):
        """CAUTION: YOUR MODEL MUST HAVE AN __EQ__ METHOD DEFINED FOR THIS TO WORK AS EXPECTED"""
        self._associated_models.remove(model)
        self._notify_assoc_models()

    @property
    def visited(self):
        return self._visited

    @visited.setter
    def visited(self, visit_status: bool):
        self._visited = visit_status

    def reset_adjacencies(self):
        self._adjacent_tiles = {}
