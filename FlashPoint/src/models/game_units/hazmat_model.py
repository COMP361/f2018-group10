import logging
from typing import List

from src.models.model import Model
from src.observers.hazmat_observer import HazmatObserver
logger = logging.getLogger("FlashPoint")


class HazmatModel(Model):

    def __init__(self):
        super().__init__()
        self._row = -7
        self._column = -7

    def __str__(self):
        return f"Hazmat at ({self._row}, {self._column}) "

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    def set_pos(self, row: int, column: int):
        self._row = row
        self._column = column
        logger.info(self.__str__())
        for obs in self.observers:
            obs.hazmat_position_changed(self._row, self._column)

    @property
    def observers(self) -> List[HazmatObserver]:
        return self._observers

    def __eq__(self, other):
        if isinstance(other, HazmatModel):
            return True

        return False
