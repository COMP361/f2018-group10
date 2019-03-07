from typing import Tuple, List

import src.constants.color as Color
from src.models.game_board.null_model import NullModel
from src.models.game_units.victim_model import VictimModel
from src.observers.player_observer import PlayerObserver
from src.constants.state_enums import PlayerStatusEnum
from src.models.model import Model


class PlayerModel(Model):

    def __init__(self, ip: str, nickname: str):
        super().__init__()
        self._ip = ip
        self._row = 0
        self._column = 0
        self._nickname = nickname
        self._color = Color.WHITE  # White by default (not racist I swear)
        self._status = PlayerStatusEnum.NOT_READY
        self._ap = 0
        self._special_ap = 0
        self._wins = 0
        self._losses = 0
        self._carrying_victim = NullModel()

    def __eq__(self, other):
        x = [other.ip == self.ip, other.nickname == self.nickname, other.row == self.row, other.column == self.column]
        return all(x)

    def info(self):
        print("### Player ###")
        print("Position: ({x}, {y})".format(x=self.row, y=self.column))
        print("AP: {ap}".format(ap=self.ap))
        print("Status: {status}".format(status=self.status))

    def _notify_position(self):
        for obs in self.observers:
            obs.player_position_changed(self.row, self.column)

    def _notify_ap(self):
        for obs in self.observers:
            obs.player_ap_changed(self.ap)

    def _notify_special_ap(self):
        for obs in self.observers:
            obs.player_special_ap_changed(self.special_ap)

    def _notify_status(self):
        for obs in self.observers:
            obs.player_status_changed(self.status)

    def _notify_wins(self):
        for obs in self.observers:
            obs.player_wins_changed(self.wins)

    def _notify_losses(self):
        for obs in self.observers:
            obs.player_losses_changed(self.losses)

    @property
    def observers(self) -> List[PlayerObserver]:
        return self._observers

    @property
    def row(self) -> int:
        return self._row

    def set_pos(self, row: int, column: int):
        self._row = row
        self._column = column
        self._notify_position()

    @property
    def column(self) -> int:
        return self._column

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
        self._notify_wins()

    @property
    def losses(self) -> int:
        return self._losses

    @losses.setter
    def losses(self, losses: int):
        self._losses = losses
        self._notify_losses()

    @property
    def ap(self) -> int:
        return self._ap

    @ap.setter
    def ap(self, ap: int):
        self._ap = ap
        self._notify_ap()

    @property
    def special_ap(self) -> int:
        return self._special_ap

    @special_ap.setter
    def special_ap(self, special_ap: int):
        self._special_ap = special_ap
        self._notify_special_ap()

    @property
    def status(self) -> PlayerStatusEnum:
        return self._status

    @status.setter
    def status(self, status: PlayerStatusEnum):
        self._status = status
        self._notify_status()

    @property
    def carrying_victim(self):
        return self._carrying_victim

    @carrying_victim.setter
    def carrying_victim(self, victim: VictimModel):
        self._carrying_victim = victim
        