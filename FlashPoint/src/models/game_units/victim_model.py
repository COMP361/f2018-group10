from src.constants.state_enums import VictimStateEnum
from src.models.game_units.poi_model import POIModel


class VictimModel(POIModel):

    def __init__(self, victim_state: VictimStateEnum):
        super().__init__(victim_state)
        self._state = victim_state
