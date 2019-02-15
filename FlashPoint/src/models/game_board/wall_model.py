
from src.models.game_board.edge_obstacle_model import EdgeObstacleModel
from src.constants.state_enums import WallStatusEnum


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

    def destroy_wall(self):
        """Set wall status to WallStatusEnum."""
        self._wall_status = WallStatusEnum.DESTROYED
