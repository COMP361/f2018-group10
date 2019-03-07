from typing import List

from src.constants.state_enums import DoorStatusEnum
from src.models.game_board.edge_obstacle_model import EdgeObstacleModel
from src.observers.door_observer import DoorObserver


class DoorModel(EdgeObstacleModel):

    def __init__(self, x: int, y: int, direction: str, door_status: DoorStatusEnum = DoorStatusEnum.CLOSED):
        super().__init__()
        self._door_status = door_status
        self._id = (x, y, direction)

    def __str__(self):
        return f"Door at ({self.id[0]}, {self.id[1]}) in direction {self.id[2]}."

    @property
    def door_status(self):
        return self._door_status

    @property
    def id(self):
        return self._id

    def open_door(self):
        """Set the door status of this door to DoorStatusEnum.OPEN"""
        self._door_status = DoorStatusEnum.OPEN
        for obs in self.observers:
            obs.door_status_changed(self._door_status)

    def close_door(self):
        """Set the door status of this door to DoorStatusEnum.CLOSED"""
        self._door_status = DoorStatusEnum.CLOSED
        for obs in self.observers:
            obs.door_status_changed(self._door_status)

    def destroy_door(self):
        """Set the door status of this door to DoorStatusEnum.DESTROYED"""
        self._door_status = DoorStatusEnum.DESTROYED
        for obs in self.observers:
            obs.door_status_changed(self._door_status)

    @property
    def observers(self) -> List[DoorObserver]:
        return self._observers
