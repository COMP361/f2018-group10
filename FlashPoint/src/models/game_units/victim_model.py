from src.constants.state_enums import VictimStateEnum
from src.models.model import Model
from typing import List
from src.observers.victim_observer import VictimObserver


class VictimModel(Model):

    def __init__(self, victim_state: VictimStateEnum):
        super().__init__()
        self._state = victim_state
        self._row = 0
        self._column = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, current_state: VictimStateEnum):
        self._state = current_state
        for obs in self.observers:
            obs.victim_state_changed(self.state)

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    def set_position(self, row: int, column: int):
        self._row = row
        self._column = column
        for obs in self.observers:
            obs.victim_position_changed(self._row, self._column)

    @property
    def observers(self) -> List[VictimObserver]:
        return self._observers