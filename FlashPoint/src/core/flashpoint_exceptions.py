from src.constants.state_enums import DirectionEnum, GameKindEnum
from src.models.game_board.tile_model import TileModel
from src.models.game_units.player_model import PlayerModel


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


class TooManyPlayersException(FlashPointBaseException):
    """Class to tell you that there are too many players and this guy can't join."""

    def __init__(self, player: PlayerModel):
        message = f"Cannot add player {player} to current game, game is full."
        super().__init__(message)


class InvalidGameKindException(FlashPointBaseException):
    """Class to tell you that you tried to do something that this Game kind should not do."""

    def __init__(self, action: str, game_type: GameKindEnum):
        message = f"Invalid game type: {game_type} for action: {action}"
        super().__init__(message)
