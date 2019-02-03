from typing import Dict

import src.constants.color as Color
from src.core.serializable import Serializable
from src.core.networking import Networking
from src.constants.state_enums import PlayerStatusEnum
from src.models.game_units.game_unit import GameUnit


class PlayerModel(GameUnit, Serializable):

    def __init__(self, player_info: Dict=None, ip: str="", nickname: str="", ):
        super().__init__()
        self._ip = ip
        self._x_pos = 0
        self._y_pos = 0
        self._nickname = nickname
        self._color = Color.WHITE  # White by default (not racist I swear)
        self._status = PlayerStatusEnum.OFFLINE
        self._ap = 0
        self._special_ap = 0
        self._wins = 0
        self._losses = 0

        self._saved_games_ids = []

        if player_info:
            self._deserialize(player_info)

    def _deserialize(self, player_info: Dict):
        """Decode a dict payload into an updated state."""
        self._ip = Networking.get_instance().get_ip()
        self._x_pos = player_info.get("_x_pos") if player_info.get("_x_pos") else self._x_pos
        self._y_pos = player_info.get("_y_pos") if player_info.get("_y_pos") else self._y_pos
        self._nickname = player_info.get("_nickname") if player_info.get("_nickname") else self._nickname
        self._color = player_info.get("_color") if player_info.get("_color") else self._color
        self._status = PlayerStatusEnum(player_info["_status"]["value"])\
            if player_info.get("_status") else self._status
        self._ap = player_info.get("_ap") if player_info.get("_ap") else self._ap
        self._special_ap = player_info.get("_special_ap") if player_info.get("_special_ap") else self._special_ap
        self._wins = player_info.get("_wins") if player_info.get("_wins") else self._wins
        self._losses = player_info.get("_losses") if player_info.get("_losses") else self._losses
        self._saved_games_ids = player_info.get("_saved_games_ids") \
            if player_info.get("_saved_games_ids") else self._saved_games_ids

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def nickname(self) -> str:
        return self._nickname

    @property
    def wins(self) -> int:
        return self._wins

    @property
    def losses(self) -> int:
        return self._losses
