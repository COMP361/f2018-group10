from src.models.game_board.tile_model import TileModel
from src.models.game_units.game_unit import GameUnit


class FireModel(GameUnit):

    def __init__(self, tile: TileModel):
        self.tile = tile

    def _validate_tile(self, tile: TileModel):
        pass
