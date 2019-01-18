from enum import Enum, auto


class PlayerStatus(Enum):
    OFFLINE = auto()
    READY = auto()
    ONLINE = auto()
    IN_GAME = auto()
