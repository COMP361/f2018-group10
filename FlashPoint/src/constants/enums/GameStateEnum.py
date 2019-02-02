from enum import Enum, auto


class GameStateEnum(Enum):
    READY_TO_JOIN = auto()
    PLACING = auto()
    MAIN_GAME = auto()
    KNOCKED_DOWN_PLACEMENT = auto()
    COMPLETED = auto()
