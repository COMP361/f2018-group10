from src.constants.state_enums import POIStatusEnum, POITypeEnum
from src.models.game_units.game_unit import GameUnit


class POIModel(GameUnit):

    def __init__(self, poi_type: POITypeEnum):
        super().__init__()
        self._status = POIStatusEnum.HIDDEN
        self._type = poi_type

    @property
    def status(self) -> POIStatusEnum:
        return self._status

    @status.setter
    def status(self, poi_status: POIStatusEnum):
        self._status = poi_status

    @property
    def type(self) -> POITypeEnum:
        return self._type

    def _validate_tile(self, tile):
        # Todo: Implement this
        pass
