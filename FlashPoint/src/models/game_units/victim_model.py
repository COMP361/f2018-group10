import logging

from src.constants.state_enums import VictimStateEnum
from src.models.model import Model
from typing import List
from src.observers.victim_observer import VictimObserver

logger = logging.getLogger("FlashPoint")

class VictimModel(Model):

    def __init__(self, victim_state: VictimStateEnum):
        super().__init__()
        self._state = victim_state
        self._row = -7
        self._column = -7

    def __str__(self):
        return f"Victim at ({self._row}, {self._column}) "

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, current_state: VictimStateEnum):
        self._state = current_state
        logger.info(self.__str__() + " state: {state}".format(state=self.state))
        for obs in self.observers:
            obs.victim_state_changed(self.state)

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
            obs.victim_position_changed(self._row, self._column)

    @property
    def observers(self) -> List[VictimObserver]:
        return self._observers
