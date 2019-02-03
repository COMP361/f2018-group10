from typing import Dict

import src.constants.color as Color
from src.constants.state_enums import PlayerStatusEnum
from src.models.game_units.game_unit import GameUnit


class PlayerModel(GameUnit):

    def __init__(self, ip: str, nickname: str, player_info: Dict=None):
        super().__init__()
        self._ip = ip
        self._x_pos = 0
        self._y_pos = 0
        self._nickname = nickname
        # self._color = Color.WHITE  # White by default (not racist I swear)
        # self._status = PlayerStatusEnum.OFFLINE
        self._ap = 0
        self._special_ap = 0
        self._wins = 0
        self._losses = 0

        self._saved_games_ids = []

        if player_info:
            self._initialize_player_info(player_info)

    def _initialize_player_info(self, player_info: Dict):
        """Decode a dict payload into an updated state."""
        self._ip = player_info.get("_ip") if player_info.get("_ip") else self._ip
        self._x_pos = player_info.get("_x_pos") if player_info.get("_x_pos") else self._x_pos
        self._y_pos = player_info.get("_y_pos") if player_info.get("_y_pos") else self._y_pos
        self._nickname = player_info.get("_nickname") if player_info.get("_nickname") else self._nickname
        self._color = player_info.get("_color") if player_info.get("_color") else self._color
        self._status = player_info.get("_status") if player_info.get("_status") else self._status
        self._ap = player_info.get("_ap") if player_info.get("_ap") else self._ap
        self._special_ap = player_info.get("_special_ap") if player_info.get("_special_ap") else self._special_ap
        self._wins = player_info.get("_wins") if player_info.get("_wins") else self._wins
        self._losses = player_info.get("_losses") if player_info.get("_losses") else self._losses
        self._saved_games_ids = player_info.get("_saved_games_ids") \
            if player_info.get("_saved_games_ids") else self._saved_games_ids
