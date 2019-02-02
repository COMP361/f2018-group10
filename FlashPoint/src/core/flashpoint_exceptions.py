
from src.models.game_board.TileModel import TileModel


class FlashPointBaseException(Exception):
    """Base class for FlashPoint specific Exceptions. Please please please use this
    as it will be infinitely valuable for debugging.
    """

    def __init__(self, message: str):
        super().__init__(message)


class TilePositionOutOfBoundsException(FlashPointBaseException):
    """Class to tell you that you fucked up."""

    def __init__(self, tile: TileModel, direction: DirectionEnum):
        message = f"{tile} has no adjacent tile in direction: {direction.value}."
        super().__init__(message)