from src.constants.state_enums import DoorStatusEnum
from src.models.game_board.edge_obstacle_model import EdgeObstacleModel


class DoorModel(EdgeObstacleModel):

    def __init__(self, door_status: DoorStatusEnum=DoorStatusEnum.CLOSED):
        super().__init__()
        self._door_status = door_status

    @property
    def door_status(self):
        return self._door_status

    def open_door(self):
        """Set the door status of this door to DoorStatusEnum.OPEN"""
        self._door_status = DoorStatusEnum.OPEN

    def close_door(self):
        """Set the door status of this door to DoorStatusEnum.CLOSED"""
        self._door_status = DoorStatusEnum.CLOSED

    def destroy_door(self):
        """Set the door status of this door to DoorStatusEnum.DESTROYED"""
        self._door_status = DoorStatusEnum.DESTROYED
