from enum import Enum, auto


class PlayerStatusEnum(Enum):
    OFFLINE = auto()
    READY = auto()
    ONLINE = auto()
    IN_GAME = auto()
