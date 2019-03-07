from abc import ABC, abstractmethod
from src.constants.state_enums import DoorStatusEnum
from src.models.game_board.edge_obstacle_model import EdgeObstacleModel
from src.observers.observer import Observer

class DoorObserver(Observer, ABC):


    def door_status_changed(self,status:DoorStatusEnum):
        pass

