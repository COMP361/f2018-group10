from src.models.game_board.tile_model import TileModel
from src.constants.enums.POIStatusEnum import POIStatusEnum
from src.models.game_units.game_unit import GameUnit


class POIModel(GameUnit):

    def __init__(self, tile: TileModel, status: POIStatusEnum):
        super().__init__(tile)
        self._status = status

    def _validate_tile(self, tile: TileModel):
        # Todo: Implement this
        pass
