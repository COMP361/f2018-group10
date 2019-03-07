from src.constants.state_enums import VictimStateEnum
from src.models.model import Model


class VictimModel(Model):

    def __init__(self, victim_state: VictimStateEnum):
        super().__init__()
        self._state = victim_state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, current_state: VictimStateEnum):
        self._state = current_state
