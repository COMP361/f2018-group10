from typing import Tuple, List

import src.constants.color as Color
from src.observers.player_observer import PlayerObserver
from src.constants.state_enums import PlayerStatusEnum
from src.models.model import Model


class PlayerModel(Model):

    def __init__(self, ip: str, nickname: str):
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

    def __eq__(self, other):
        x = [other.ip == self.ip, other.nickname == self.nickname, other.x_pos == self.x_pos, other.y_pos == self.y_pos]
        return all(x)

    def _notify_position(self, x_pos: int, y_pos: int):
        for obs in self.observers:
            obs.player_position_changed(x_pos, y_pos)

    def _notify_ap(self, ap: int):
        for obs in self.observers:
            obs.player_ap_changed(ap)

    def _notify_special_ap(self, ap: int):
        for obs in self.observers:
            obs.player_special_ap_changed(ap)

    def _notify_status(self, status: PlayerStatusEnum):
        for obs in self.observers:
            obs.player_status_changed(status)

    @property
    def observers(self) -> List[PlayerObserver]:
        return self._observers

    @property
    def x_pos(self) -> int:
        return self._x_pos

    @x_pos.setter
    def x_pos(self, x_pos: int):
        self._x_pos = x_pos

    @property
    def y_pos(self) -> int:
        return self._y_pos

    @y_pos.setter
    def y_pos(self, y_pos: int):
        self._y_pos = y_pos

    @property
    def ip(self) -> str:
        return self._ip

    @ip.setter
    def ip(self, ip: str):
        self._ip = ip

    @property
    def nickname(self) -> str:
        return self._nickname

    @nickname.setter
    def nickname(self, nickname: str):
        self._nickname = nickname

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, color: Tuple):
        self._color = color

    @property
    def wins(self) -> int:
        return self._wins

    @wins.setter
    def wins(self, wins: int):
        self._wins = wins

    @property
    def losses(self) -> int:
        return self._losses

    @losses.setter
    def losses(self, losses: int):
        self._losses = losses

    @property
    def ap(self) -> int:
        return self._ap

    @ap.setter
    def ap(self, ap: int):
        self._ap = ap

    @property
    def special_ap(self) -> int:
        return self._special_ap

    @special_ap.setter
    def special_ap(self, special_ap: int):
        self._special_ap = special_ap

    @property
    def status(self) -> PlayerStatusEnum:
        return self._status

    @status.setter
    def status(self, status: PlayerStatusEnum):
        self._status = status
