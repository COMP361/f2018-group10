from src.constants.state_enums import GameKindEnum
from src.models.game_units.player_model import PlayerModel



class FlashPointBaseException(Exception):
    """Base class for FlashPoint specific Exceptions. Please please please use this
    as it will be infinitely valuable for debugging.
    """

    def __init__(self, message: str):
        super().__init__(message)


class POINotRevealedYetException(FlashPointBaseException):
    """Class to tell you you can't identify a POI if it has not been revealed yet"""

    def __init__(self):
        message = f"POI was not revealed yet, cannot identify it."
        super().__init__(message)


class TilePositionOutOfBoundsException(FlashPointBaseException):
    """Class to tell you that you fucked up."""

    def __init__(self, tile, direction: str):
        message = f"{tile} has no adjacent tile in direction: {direction}."
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


class NotEnoughAPException(FlashPointBaseException):
    """Class to tell you that the player does not have enough AP to perform a given action."""

    def __init__(self, action: str, minPoints: int):
        message = f"Player does not have enough AP to {action}. Player needs at least {minPoints} points."
        super().__init__(message)


class WallNotAdjacent(FlashPointBaseException):
    """Class to tell you that the wall is not adjacent to the player's current space."""

    def __init__(self, player_x: int, player_y: int):
        message = f"The wall is not adjacent to the player located at ({player_x}, {player_y})."
        super().__init__(message)


class WallAlreadyDestroyed(FlashPointBaseException):
    """Class to tell you that the wall cannot be chopped because it is already destroyed."""

    def __init__(self, player_x: int, player_y: int):
        message = f"The wall adjacent to the player located at ({player_x}, {player_y}) cannot be chopped because it is already destroyed."
        super().__init__(message)