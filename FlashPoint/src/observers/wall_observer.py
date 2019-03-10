from abc import ABC, abstractmethod
from src.constants.state_enums import WallStatusEnum
from src.models.game_board.edge_obstacle_model import EdgeObstacleModel
from src.observers.observer import Observer

class WallObserver(Observer, ABC):

    @abstractmethod
    def wall_status_changed(self, status:WallStatusEnum):
        pass
