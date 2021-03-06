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


class ArrowDirectionEnum(Enum):
    NORTH = auto()
    NORTH_EAST = auto()
    EAST = auto()
    SOUTH_EAST = auto()
    SOUTH = auto()
    SOUTH_WEST = auto()
    WEST = auto()
    NORTH_WEST = auto()
    NO_DIRECTION = auto()


class DoorStatusEnum(Enum):
    OPEN = auto()
    CLOSED = auto()
    DESTROYED = auto()


class GameBoardTypeEnum(Enum):
    ORIGINAL = auto()
    ALTERNATIVE = auto()
    RANDOM = auto()


class GameKindEnum(Enum):
    FAMILY = auto()
    EXPERIENCED = auto()


class GameStateEnum(Enum):
    READY_TO_JOIN = auto()
    PLACING_PLAYERS = auto()
    PLACING_VEHICLES = auto()
    MAIN_GAME = auto()
    KNOCKED_DOWN_PLACEMENT = auto()
    LOST = auto()
    WON = auto()


class PlayerStatusEnum(Enum):
    READY = auto()
    NOT_READY = auto()
    IN_GAME = auto()


class POIStatusEnum(Enum):
    HIDDEN = auto()
    REVEALED = auto()
    LOST = auto()


class POIIdentityEnum(Enum):
    VICTIM = auto()
    FALSE_ALARM = auto()


class SpaceKindEnum(Enum):
    INDOOR = auto()
    OUTDOOR = auto()
    ENGINE_PARKING = auto()
    AMBULANCE_PARKING = auto()


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
    ON_BOARD = auto()


class WallStatusEnum(Enum):
    INTACT = auto()
    DAMAGED = auto()
    DESTROYED = auto()


class PlayerRoleEnum(Enum):
    CAFS = auto()
    DRIVER = auto()
    FAMILY = auto()
    CAPTAIN = auto()
    GENERALIST = auto()
    HAZMAT = auto()
    IMAGING = auto()
    PARAMEDIC = auto()
    RESCUE = auto()
    DOGE = auto()
    VETERAN = auto()


class VehicleOrientationEnum(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()
    UNSET = auto()


class QuadrantEnum(Enum):
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()
