from src.constants.enums.VictimStateEnum import VictimStateEnum
from src.models.game_units.POIModel import POIModel


class VictimModel(POIModel):

    def __init__(self, victim_state: VictimStateEnum):
        super().__init__()
        self._state = victim_state
