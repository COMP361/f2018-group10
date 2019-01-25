from src.models.game_board.TileModel import TileModel
from src.models.game_units.GameUnit import GameUnit


class FireModel(GameUnit):

    def __init__(self, tile: TileModel):
        self.tile = tile

    def _validate_tile(self, tile: TileModel):
        pass
