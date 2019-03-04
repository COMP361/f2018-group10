from src.constants.state_enums import VictimStateEnum
from src.models.model import Model


class VictimModel(Model):

    def __init__(self, victim_state: VictimStateEnum):
        super().__init__()
        self._state = victim_state

    def set_dead(self):
        self._state = VictimStateEnum.LOST  # Not sure if I should simply delete it or set it to dead.
