import logging
from typing import List, Tuple

from src.constants.state_enums import VehicleOrientationEnum
from src.models.game_units.player_model import PlayerModel
from src.models.model import Model

logger = logging.getLogger("FlashPoint")


class VehicleModel(Model):
    """
    Base class for Ambulance and Engine.
    IMPORTANT NOTES:
    - For horizontal vehicles, row is the topmost row of the parking spot
    - For vertical vehicles, column is the leftmost column of the parking spot
    """

    def __init__(self, board_dimensions: Tuple[int, int]):
        super().__init__()
        self._board_dimensions = board_dimensions
        self._is_vertical = False
        self._row = -7
        self._column = -7
        self._passengers: List[PlayerModel] = []

    @property
    def orientation(self) -> VehicleOrientationEnum:
        """Determine if this vehicle model is vertical or horizontal, or unset."""
        if self._row < 0 or self._column < 0:
            return VehicleOrientationEnum.UNSET
        elif self._row == 0 or self._row == self._board_dimensions[0] - 1:
            return VehicleOrientationEnum.HORIZONTAL
        elif self._column == 0 or self._column == self._board_dimensions[1] - 1:
            return VehicleOrientationEnum.VERTICAL

    def _notify_pos(self):
        for obs in self._observers:
            obs.notify_vehicle_pos(self.orientation, self.row, self.column)

    def _notify_passengers(self):
        for obs in self._observers:
            obs.notify_passengers(self._passengers)

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    def drive(self, parking_spot: Tuple[int, int]):
        """Moving the Vehicle moves driver and passengers as well."""
        self._row = parking_spot[0]
        self._column = parking_spot[1]
        logger.info("Vehicle position: ({row}, {column})".format(row=self.row, column=self.column))

        if self.passengers:
            logger.info("Passengers moving")
            for passenger in self._passengers:
                passenger.set_pos(self.row, self.column)

        self._notify_pos()

    @property
    def passengers(self) -> List[PlayerModel]:
        return self._passengers

    def add_passenger(self, player: PlayerModel):
        self._passengers.append(player)
        self._notify_passengers()

    def remove_passenger(self, player: PlayerModel):
        self._passengers.remove(player)
        self._notify_passengers()

    def clear_passengers(self):
        self._passengers.clear()
        self._notify_passengers()
