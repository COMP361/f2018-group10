from models.game_board.TileModel import TileModel
from src.constants.enums.POIStatusEnum import POIStatusEnum
from src.models.game_units.GameUnit import GameUnit


class POIModel(GameUnit):

    def __init__(self, tile: TileModel, status: POIStatusEnum):
        super().__init__(tile)
        self._status = status

    def _validate_tile(self, tile: TileModel):
        # Todo: Implement this
        pass
