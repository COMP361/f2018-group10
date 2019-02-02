<<<<<<< HEAD:FlashPoint/src/models/game_units/VictimModel.py
from src.constants.enums.victim_state_enum import VictimStateEnum
from src.models.game_units.POIModel import POIModel
=======
from src.constants.enums.VictimStateEnum import VictimStateEnum
from src.models.game_units.poi_model import POIModel
>>>>>>> GSD-Alek:FlashPoint/src/models/game_units/victim_model.py


class VictimModel(POIModel):

    def __init__(self, victim_state: VictimStateEnum):
        super().__init__()
        self._state = victim_state
