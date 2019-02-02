from src.models.game_units.game_unit import GameUnit


class FireModel(GameUnit):

    def __init__(self, tile):
        super().__init__(tile)
        self.tile = tile

    def _validate_tile(self, tile):
        pass
