from src.models.game_units.game_unit import GameUnit
from src.constants.state_enums import VictimStateEnum


class VictimModel(GameUnit):

    def __init__(self, victim_state: VictimStateEnum):
        super().__init__()
        self._state = victim_state
