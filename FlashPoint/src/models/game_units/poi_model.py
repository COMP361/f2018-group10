from src.constants.state_enums import POIStatusEnum
from src.models.game_units.game_unit import GameUnit


class POIModel(GameUnit):

    def __init__(self, tile, status: POIStatusEnum):
        super().__init__(tile)
        self._status = status

    def _validate_tile(self, tile):
        # Todo: Implement this
        pass
