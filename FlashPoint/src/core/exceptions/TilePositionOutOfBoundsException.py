from constants.enums.DirectionEnum import DirectionEnum
from core.exceptions.FlashPointBaseException import FlashPointBaseException
from models.game_board.TileModel import TileModel


class TilePositionOutOfBoundsException(FlashPointBaseException):
    """Class to tell you that you fucked up."""

    def __init__(self, tile: TileModel, direction: DirectionEnum):
        message = f"{tile} has no adjacent tile in direction: {direction.value}."
        super().__init__(message)
