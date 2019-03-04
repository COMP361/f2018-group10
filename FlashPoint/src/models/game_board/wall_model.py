from typing import List

from src.models.game_board.edge_obstacle_model import EdgeObstacleModel
from src.constants.state_enums import WallStatusEnum
from src.models.game_board.tile_model import TileModel
from src.observers.wall_observer import WallObserver


class WallModel(EdgeObstacleModel):
    """Logical state of a Wall object."""
    def __init__(self):
        self._wall_status = WallStatusEnum.INTACT

    @property
    def wall_status(self):
        return self._wall_status

    def damage_wall(self):
        """Set wall status to WallStatusEnum.DAMAGED"""
        self._wall_status = WallStatusEnum.DAMAGED
        for obs in self.observers:
            obs.wall_status_changed(self._wall_status)


    def destroy_wall(self):
        """Set wall status to WallStatusEnum."""
        self._wall_status = WallStatusEnum.DESTROYED
        for obs in self.observers:
            obs.wall_status_changed(self._wall_status)


    def is_player_adjacent(self, player_tile: TileModel) -> bool:
        """Checks if the player is adjacent to the wall"""
        if self in player_tile.adjacent_edge_objects:
            return True

        return False


    @property
    def observers(self) -> List[WallObserver]:
        return self._observers
