from src.constants.state_enums import DirectionEnum, GameKindEnum
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.poi_model import POIModel


class FlashPointBaseException(Exception):
    """Base class for FlashPoint specific Exceptions. Please please please use this
    as it will be infinitely valuable for debugging.
    """

    def __init__(self, message: str):
        super().__init__(message)


class POINotRevealedYetException(FlashPointBaseException):
    """Class to tell you you can't identify a POI if it has not been revealed yet"""

    def __init__(self, poi: POIModel):
        message = f"{poi} was not revealed yet, cannot identify it."
        super().__init__(message)


class TilePositionOutOfBoundsException(FlashPointBaseException):
    """Class to tell you that you fucked up."""

    def __init__(self, tile, direction: DirectionEnum):
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


class PlayerNotFoundException(FlashPointBaseException):
    """Player was not found in the game state"""

    def __init__(self, player_ip: str):
        message = f"Player with ip: {player_ip} was not found in the Game State."
        super().__init__(message)
