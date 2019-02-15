from src.constants.state_enums import POIStatusEnum
from models.model import Model


class POIModel(Model):

    def __init__(self, tile, status: POIStatusEnum):
        super().__init__(tile)
        self._status = status

    def _validate_tile(self, tile):
        # Todo: Implement this
        pass
