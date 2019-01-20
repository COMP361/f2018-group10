from enum import Enum, auto

class VictimStateEnum(Enum):
    UNCONSCIOUS = auto()
    TREATED = auto()
    RESCUED = auto()
    LOST = auto()