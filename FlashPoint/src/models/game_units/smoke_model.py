from src.models.game_units.game_unit import GameUnit


class SmokeModel(GameUnit):

    def __init__(self, tile):
        super().__init__(tile)
        self.tile = tile

    def _validate_tile(self, tile):
        pass
