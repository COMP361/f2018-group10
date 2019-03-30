from enum import Enum, auto


class ChangeSceneEnum(Enum):
    STARTSCENE = auto()
    HOSTJOINSCENE = auto()
    JOINSCENE = auto()
    HOSTMENUSCENE = auto()
    CREATEGAMEMENU = auto()
    CHARACTERSCENE = auto()
    LOADGAME = auto()
    LOBBYSCENE = auto()
    GAMEBOARDSCENE = auto()
    REGISTER = auto()
    SETMAXPLAYERSCENE = auto()
    LOSESCENE = auto()
    WINSCENE = auto()
    CHOOSEBOARDSCENE = auto()
