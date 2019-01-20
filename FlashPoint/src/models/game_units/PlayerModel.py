import src.constants.Color as Color
from src.constants.enums.PlayerStatusEnum import PlayerStatusEnum
from src.models.game_units.GameUnit import GameUnit


class PlayerModel(GameUnit):

    def __init__(self):
        super().__init__()
        self._user_name = ""
        self._password = ""
        self._color = Color.WHITE  # White by default
        self._status = PlayerStatusEnum.OFFLINE
        self._ability_points = 0
