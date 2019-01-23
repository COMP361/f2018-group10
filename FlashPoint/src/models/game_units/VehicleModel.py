from src.models.game_board.TileModel import TileModel

# TODO Make this an interface or abstract class


class VehicleModel(object):
    """Base class for Ambulance and Engine"""

    def __init__(self, tile: TileModel):
        super().__init__(tile)

    def drive(self, tile: TileModel):
        pass
