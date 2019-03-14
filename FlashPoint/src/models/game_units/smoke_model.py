from models.model import Model


class SmokeModel(Model):

    def __init__(self, tile):
        super().__init__(tile)
        self.tile = tile

    def _validate_tile(self, tile):
        pass
