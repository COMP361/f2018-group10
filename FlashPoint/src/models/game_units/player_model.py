from typing import Tuple, List, Union

import src.constants.color as Color
from src.models.game_board.null_model import NullModel
from src.models.game_units.victim_model import VictimModel
from src.observers.player_observer import PlayerObserver
from src.constants.state_enums import PlayerStatusEnum, PlayerRoleEnum, GameKindEnum
from src.models.model import Model


class PlayerModel(Model):

    def __init__(self, ip: str, nickname: str):
        super().__init__()
        self._ip = ip
        self._row = -1
        self._column = -1
        self._nickname = nickname
        self._color = Color.WHITE  # White by default (not racist I swear)
        self._status = PlayerStatusEnum.NOT_READY
        self._ap = 0
        self._special_ap = 0
        self._wins = 0
        self._losses = 0
        self._carrying_victim = NullModel()
        self._role: PlayerRoleEnum = PlayerRoleEnum.FAMILY

    def __eq__(self, other):
        x = [other.ip == self.ip, other.nickname == self.nickname]
        return all(x)

    def __str__(self):
        player_pos = "Player position: ({row}, {column})".format(row=self.row, column=self.column)
        player_ap = "Player AP: {ap}".format(ap=self.ap)
        player_carrying_victim = "Victim with player: {victim}".format(victim=self.carrying_victim.__str__())
        player_status = "Player status: {status}".format(status=self.status)
        player_color = "Player color: {color}\n".format(color=self.color)
        return '\n'.join([player_pos, player_ap, player_carrying_victim, player_status, player_color])

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

    def _notify_carry(self):
        for obs in self.observers:
            obs.player_carry_changed(self.carrying_victim)

    def _notify_role(self):
        for obs in self.observers:
            obs.player_role_changed(self.role)

    @property
    def observers(self) -> List[PlayerObserver]:
        return self._observers

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, new_role: PlayerRoleEnum):
        self._role = new_role
        self._notify_role()

    @property
    def row(self) -> int:
        return self._row

    def set_pos(self, row: int, column: int):
        # If the player is carrying a victim,
        # update their position as well
        self._row = row
        self._column = column
        if isinstance(self.carrying_victim, VictimModel):
            self.carrying_victim.set_pos(row, column)
        self._notify_position()

    def set_initial_ap(self, game_kind: GameKindEnum):
        """Set the initial AP for this player"""
        self.ap = 4

        if game_kind == GameKindEnum.EXPERIENCED:
            # TODO: Set AP based on role.
            pass

    @property
    def column(self) -> int:
        return self._column

    @property
    def has_pos(self) -> bool:
        return (self.row >= 0) and (self.column >= 0)

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
    def carrying_victim(self) -> Union[VictimModel, NullModel]:
        return self._carrying_victim

    @carrying_victim.setter
    def carrying_victim(self, victim: VictimModel):
        self._carrying_victim = victim
        self._notify_carry()
