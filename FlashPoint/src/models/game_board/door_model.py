import logging
from typing import List

from src.constants.state_enums import DoorStatusEnum
from src.models.game_board.edge_obstacle_model import EdgeObstacleModel
from src.observers.door_observer import DoorObserver

logger = logging.getLogger("FlashPoint")


class DoorModel(EdgeObstacleModel):

    def __init__(self, row: int, column: int, direction: str, door_status: DoorStatusEnum = DoorStatusEnum.CLOSED):
        super().__init__()
        self._door_status = door_status
        self._id = (row, column, direction)

    def __str__(self):
        if self.door_status == DoorStatusEnum.OPEN:
            stat = "Open"
        elif self.door_status == DoorStatusEnum.CLOSED:
            stat = "Closed"
        else:
            stat = "Destroyed"
        return f"{stat} door at ({self.id[0]}, {self.id[1]}) in direction {self.id[2]}."

    @property
    def door_status(self):
        return self._door_status

    @door_status.setter
    def door_status(self, door_status: DoorStatusEnum):
        self._door_status = door_status
        self.log_info()
        for obs in self.observers:
            obs.door_status_changed(self._door_status)

    @property
    def id(self):
        return self._id

    def open_door(self):
        self._door_status = DoorStatusEnum.OPEN
        self.log_info()
        for obs in self.observers:
            obs.door_status_changed(self._door_status)

    def close_door(self):
        self._door_status = DoorStatusEnum.CLOSED
        self.log_info()
        for obs in self.observers:
            obs.door_status_changed(self._door_status)

    def destroy_door(self):
        self._door_status = DoorStatusEnum.DESTROYED
        self.log_info()
        for obs in self.observers:
            obs.door_status_changed(self._door_status)

    def log_info(self):
        logger.info(self.__str__())

    @property
    def observers(self) -> List[DoorObserver]:
        return self._observers
