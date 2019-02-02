<<<<<<< HEAD:FlashPoint/src/models/game_units/POIModel.py
from src.models.game_board.TileModel import TileModel
from src.constants.enums.poi_status_enum import POIStatusEnum
from src.models.game_units.GameUnit import GameUnit
=======
from src.models.game_board.tile_model import TileModel
from src.constants.enums.POIStatusEnum import POIStatusEnum
from src.models.game_units.game_unit import GameUnit
>>>>>>> GSD-Alek:FlashPoint/src/models/game_units/poi_model.py


class POIModel(GameUnit):

    def __init__(self, tile: TileModel, status: POIStatusEnum):
        super().__init__(tile)
        self._status = status

    def _validate_tile(self, tile: TileModel):
        # Todo: Implement this
        pass
