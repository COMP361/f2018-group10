from enum import Enum, auto


class DifficultyLevelEnum(Enum):
    RECRUIT = auto()
    VETERAN = auto()
    HEROIC = auto()


class DirectionEnum(Enum):
    NORTH = auto()
    EAST = auto()
    WEST = auto()
    SOUTH = auto()


class DoorStatusEnum(Enum):
    OPEN = auto()
    CLOSED = auto()
    DESTROYED = auto()


class GameKindEnum(Enum):
    FAMILY = auto()
    EXPERIENCED = auto()


class GameStateEnum(Enum):
    READY_TO_JOIN = auto()
    PLACING = auto()
    MAIN_GAME = auto()
    KNOCKED_DOWN_PLACEMENT = auto()
    COMPLETED = auto()


class PlayerStatusEnum(Enum):
    OFFLINE = auto()
    READY = auto()
    ONLINE = auto()
    IN_GAME = auto()


class POIStatusEnum(Enum):
    HIDDEN = auto()
    REVEALED = auto()


class SpaceKindEnum(Enum):
    INDOOR = auto()
    OUTDOOR = auto()


class SpaceStatusEnum(Enum):
    SAFE = auto()
    SMOKE = auto()
    FIRE = auto()


class VehicleKindEnum(Enum):
    AMBULANCE = auto()
    ENGINE = auto()


class VictimStateEnum(Enum):
    UNCONSCIOUS = auto()
    TREATED = auto()
    RESCUED = auto()
    LOST = auto()


class WallStatusEnum(Enum):
    INTACT = auto()
    DAMAGED = auto()
    DESTROYED = auto()