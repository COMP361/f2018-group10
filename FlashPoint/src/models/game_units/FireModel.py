import src.models.game_board.TileModel as t
from src.models.game_units.GameUnit import GameUnit


class FireModel(GameUnit):

    def __init__(self, tile: t.TileModel):
        self.tile = tile

    def _validate_tile(self, tile: t.TileModel):
        pass
