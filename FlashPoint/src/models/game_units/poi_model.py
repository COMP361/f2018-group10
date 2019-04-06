from typing import List

from src.models.game_units.victim_model import VictimModel
from src.observers.poi_observer import POIObserver
from src.constants.state_enums import POIStatusEnum, POIIdentityEnum
from src.models.model import Model

import logging

logger = logging.getLogger("FlashPoint")


class POIModel(Model):

    def __init__(self, identity: POIIdentityEnum):
        super().__init__()
        self._identity = identity
        self._status = POIStatusEnum.HIDDEN
        self._row = -7
        self._column = -7

    def __str__(self):
        return f"POIModel: {self._identity} at: ({self._row}, {self._column})"

    def __eq__(self, other):
        if not isinstance(other, POIModel):
            return False
        return all([self.row == other.row, self.column==other.column, self.identity == other.identity, self.status == other.status])

    def reveal(self, victim_model: VictimModel):
        logger.info(f"{self} revealed.")
        if self._status == POIStatusEnum.HIDDEN:
            self._status = POIStatusEnum.REVEALED
            self._notify_status(victim_model)

    def _notify_status(self, victim_model: VictimModel):
        for obs in self.observers:
            obs.poi_status_changed(self.status, victim_model)

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

    def set_pos(self, row: int, column: int):
        self._row = row
        self._column = column
        logger.info("POIModel position: ({row}, {column})".format(row=self.row, column=self.column))
        self._notify_position()

    @property
    def status(self) -> POIStatusEnum:
        return self._status

    @status.setter
    def status(self, status: POIStatusEnum):
        self._status = status
        logger.info("POIModel status: {status}".format(status=self.status))

    @property
    def identity(self) -> POIIdentityEnum:  # GOTTA CHECK IF IT IS REVEALED YET
        """Is this POI a Victim or a FalseAlarm?"""
        return self._identity
