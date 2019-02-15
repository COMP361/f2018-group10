from typing import List

from src.observers.poi_observer import POIObserver
from src.constants.state_enums import POIStatusEnum, POIIdentityEnum
from src.models.model import Model


class POIModel(Model):

    def __init__(self, identity: POIIdentityEnum, x_pos: int, y_pos: int):
        super().__init__()
        self._identity = identity
        self._status = POIStatusEnum.HIDDEN
        self._x_pos = x_pos
        self._y_pos = y_pos

    def _notify_status(self):
        for obs in self.observers:
            obs.poi_status_changed(self.status)

    def _notify_position(self):
        for obs in self.observers:
            obs.poi_position_changed(self.x_pos, self.y_pos)

    @property
    def observers(self) -> List[POIObserver]:
        return self._observers

    @property
    def x_pos(self) -> int:
        return self._x_pos

    @x_pos.setter
    def x_pos(self, x_pos: int):
        self._x_pos = x_pos
        self._notify_position()

    @property
    def y_pos(self) -> int:
        return self._y_pos

    @y_pos.setter
    def y_pos(self, y_pos: int):
        self._y_pos = y_pos
        self._notify_position()

    @property
    def status(self) -> POIStatusEnum:
        return self._status

    @status.setter
    def status(self, status: POIStatusEnum):
        self._status = status
        self._notify_status()

    @property
    def identity(self) -> POIIdentityEnum:
        """Is this POI a Victim or a FalseAlarm?"""
        return self._identity
