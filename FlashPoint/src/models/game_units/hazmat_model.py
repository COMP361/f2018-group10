from typing import Tuple, List

import src.constants.color as Color
from src.models.game_board.null_model import NullModel
from src.models.game_units.victim_model import VictimModel
from src.constants.state_enums import PlayerStatusEnum
from src.models.model import Model


class HazmatModel(Model):

    def __init__(self, row: int, column: int):
        super().__init__()
        self.row = row
        self.column = column