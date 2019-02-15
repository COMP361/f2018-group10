from src.constants.state_enums import POIStatusEnum, POIIdentityEnum
from src.models.model import Model


class POIModel(Model):

    def __init__(self, identity: POIIdentityEnum):
        super().__init__()
        self._identity = identity
        self._status = POIStatusEnum.HIDDEN
        self._x_pos = 0
        self._y_pos = 0

    @property
    def x_pos(self) -> int:
        return self._x_pos

    @property
    def y_pos(self) -> int:
        return self._y_pos

    @property
    def status(self) -> POIStatusEnum:
        return self._status

    @property
    def identity(self) -> POIIdentityEnum:
        """Is this POI a Victim or a FalseAlarm?"""
        return self._identity
