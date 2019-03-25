from typing import Tuple

from src.models.game_units.vehicle_model import VehicleModel


class EngineModel(VehicleModel):

    def __init__(self, board_dimensions: Tuple[int, int]):
        super().__init__(board_dimensions)
