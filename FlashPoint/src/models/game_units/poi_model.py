from typing import List

from src.core.flashpoint_exceptions import POINotRevealedYetException
from src.observers.poi_observer import POIObserver
from src.constants.state_enums import POIStatusEnum, POIIdentityEnum
from src.models.model import Model


class POIModel(Model):

    def __init__(self, identity: POIIdentityEnum, row: int, column: int):
        super().__init__()
        self._identity = identity
        self._status = POIStatusEnum.HIDDEN
        self._row = row
        self._column = column

    def reveal(self):
        if self._status is POIStatusEnum.HIDDEN:
            self._status = POIStatusEnum.REVEALED
            self._notify_status()

    def _notify_status(self):
        for obs in self.observers:
            obs.poi_status_changed(self.status)

    def _notify_position(self):
        for obs in self.observers:
            obs.poi_position_changed(self.row, self.column)

    @property
    def observers(self) -> List[POIObserver]:
        return self._observers

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    def set_position(self, row: int, column: int):
        self._row = row
        self._column = column
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
