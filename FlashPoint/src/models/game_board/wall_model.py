<<<<<<< HEAD:FlashPoint/src/models/game_board/WallModel.py
from src.models.game_board.EdgeObstacleModel import EdgeObstacleModel
from src.constants.enums.wall_status_enum import WallStatusEnum
=======
from src.models.game_board.edge_obstacle_model import EdgeObstacleModel
from src.constants.enums.WallStatusEnum import WallStatusEnum
>>>>>>> GSD-Alek:FlashPoint/src/models/game_board/wall_model.py


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
