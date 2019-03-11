from typing import List

from src.core.flashpoint_exceptions import WallAlreadyDestroyedException
from src.models.game_board.edge_obstacle_model import EdgeObstacleModel
from src.constants.state_enums import WallStatusEnum
from src.observers.wall_observer import WallObserver


class WallModel(EdgeObstacleModel):
    """Logical state of a Wall object."""
    def __init__(self, x: int, y: int, direction: str):
        super().__init__()
        self._wall_status = WallStatusEnum.INTACT
        self._id = (x, y, direction)


    @property
    def wall_status(self):
        return self._wall_status

    @property
    def id(self):
        return self._id

    def inflict_damage(self):
        """
        @precondition: wall is not already destroyed
        Inflict damage to the wall and change its status
        """
        if self._wall_status == WallStatusEnum.INTACT:
            self._wall_status = WallStatusEnum.DAMAGED

        elif self._wall_status == WallStatusEnum.DAMAGED:
            self._wall_status = WallStatusEnum.DESTROYED

        else:
            return

        for obs in self.observers:
            obs.wall_status_changed(self._wall_status)

    @property
    def observers(self) -> List[WallObserver]:
        return self._observers
