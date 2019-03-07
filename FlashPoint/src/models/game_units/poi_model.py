from typing import List

from src.core.flashpoint_exceptions import POINotRevealedYetException
from src.observers.poi_observer import POIObserver
from src.constants.state_enums import POIStatusEnum, POIIdentityEnum
from src.models.model import Model


class POIModel(Model):

    def __init__(self, identity: POIIdentityEnum):
        super().__init__()
        self._identity = identity
        self._status = POIStatusEnum.HIDDEN
        self._x_pos = 0
        self._y_pos = 0

    def reveal(self):
        if self._status is POIStatusEnum.HIDDEN:
            self._status = POIStatusEnum.REVEALED

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

    @property
    def y_pos(self) -> int:
        return self._y_pos

    def set_position(self, x: int, y: int):
        self._x_pos = x
        self._y_pos = y
        self._notify_position()

    @property
    def status(self) -> POIStatusEnum:
        return self._status

    @status.setter
    def status(self, status: POIStatusEnum):
        self._status = status
        self._notify_status()

    @property
    def identity(self) -> POIIdentityEnum:  # GOTTA CHECK IF IT IS REVEALED YET
        """Is this POI a Victim or a FalseAlarm?"""
        if self._status is not POIStatusEnum.REVEALED:
            raise POINotRevealedYetException()

        else:
            return self._identity

    @property
    def observers(self) -> List[POIObserver]:
        return self._observers
