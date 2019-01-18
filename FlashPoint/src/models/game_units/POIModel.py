from src.constants.enums.POIStatusEnum import POIStatusEnum
from src.models.game_units.GameUnit import GameUnit


class POIModel(GameUnit):

    def __init__(self, status: POIStatusEnum):
        super().__init__()
        self._status =status
