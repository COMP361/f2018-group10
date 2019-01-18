from src.models.game_board.TileModel import TileModel
from src.models.game_units.GameUnit import GameUnit


class VehicleModel(GameUnit):
    """Base class for Ambulance and Engine"""

    def __init__(self):
        super().__init__()

    def drive(self, tile: TileModel):
        pass
