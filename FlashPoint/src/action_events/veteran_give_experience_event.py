from typing import List
import math

from src.action_events.action_event import ActionEvent
from src.constants.state_enums import PlayerRoleEnum
from src.controllers.move_controller import MoveController
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.victim_model import VictimModel


class VeteranGiveExperienceEvent(ActionEvent):

    def __init__(self, player: PlayerModel):
        super().__init__()
        self.c_player = player

    def execute(self, *args, **kwargs):
        """
        Give 1 free AP to the CURRENT player
        in the vicinity of the Veteran if applicable.
        Give the dodge ability to ALL the players
        in the vicinity of the Veteran if applicable,
        else take that ability away.

        :return:
        """
        self.game: GameStateModel = GameStateModel.instance()
        self.c_player = [player for player in self.game.players if player == self.c_player][0]
        self.board = self.game.game_board
        self.move_cont = MoveController.instance()
        # Check if there is a Veteran
        # amongst the players
        veteran = None
        for player in self.game.players:
            if player.role == PlayerRoleEnum.VETERAN:
                veteran = player

        if not veteran:
            return

        veteran_vicinity = self._determine_vicinity_veteran(veteran.row, veteran.column)
        if self.c_player == veteran:
            return

        can_player_reach_vet = self._can_player_reach_veteran(self.c_player, veteran, veteran_vicinity)
        if not can_player_reach_vet:
            # If player cannot reach Veteran,
            # they can no longer dodge
            self.c_player.allowed_to_dodge = False
            return

        # Current player can only
        # receive extra AP once per turn
        if not self.c_player.has_AP_from_veteran:
            self.c_player.ap = self.c_player.ap + 1
            self.c_player.has_AP_from_veteran = True

        # Player always allowed to dodge
        # as long as in vicinity of Veteran
        self.c_player.allowed_to_dodge = True

        # Give the rest of the players the
        # ability to dodge if they are in
        # the vicinity of the Veteran else
        # take that ability away
        for p in self.game.players:
            if p == veteran or p == self.c_player:
                continue

            can_player_reach_vet = self._can_player_reach_veteran(p, veteran, veteran_vicinity)
            if can_player_reach_vet:
                p.allowed_to_dodge = True
            else:
                p.allowed_to_dodge = False

    def _determine_vicinity_veteran(self, veteran_row: int, veteran_col: int) -> List[TileModel]:
        """
        Determine the 3-space radius to the Veteran.
        (includes the veteran's source tile)

        :return: List of tiles that belong to the
                3-space radius of the Veteran
        """
        veteran_vicinity = []
        for row_diff in range(-3, 4):
            for col_diff in range(-3, 4):
                distance_away = math.fabs(row_diff) + math.fabs(col_diff)
                if distance_away > 3:
                    continue

                candidate_row = veteran_row + row_diff
                candidate_col = veteran_col + col_diff
                is_in_bounds = self._is_tile_in_board(candidate_row, candidate_col)
                if not is_in_bounds:
                    continue

                candidate_tile = self.board.get_tile_at(candidate_row, candidate_col)
                veteran_vicinity.append(candidate_tile)

        return veteran_vicinity

    def _is_tile_in_board(self, row: int, column: int) -> bool:
        """
        Checking if the tile will be
        within the board

        :param row:
        :param column:
        :return: True if the tile will be in the board, False otherwise.
        """
        if row < 0 or row > 7:
            return False
        if column < 0 or column > 9:
            return False

        return True

    def _can_player_reach_veteran(self, player: PlayerModel, veteran: PlayerModel, veteran_vicinity: List[TileModel]) -> bool:
        """
        Determines whether the player
        can reach the veteran.

        :param player:
        :param veteran:
        :param veteran_vicinity: List of tiles in the vicinity of the Veteran.
        :return: True if the player can reach the Veteran, False otherwise.
        """
        # If the player is not in the
        # vicinity of the Veteran, player
        # cannot reach the Veteran.
        player_tile = self.board.get_tile_at(player.row, player.column)
        veteran_tile = self.board.get_tile_at(veteran.row, veteran.column)
        if player_tile not in veteran_vicinity:
            return False

        # Get the moveable tiles for the player
        self.board.reset_tiles_visit_count()
        ap = self._determine_player_ap_to_utilize(player)

        # Player is only allowed to move through
        # Safe tiles in an attempt to reach the Veteran
        self.move_cont.only_allow_safe_space = True
        moveable_tiles = self.move_cont._determine_reachable_tiles(player.row, player.column, ap)
        self.move_cont.only_allow_safe_space = False
        self.board.reset_tiles_visit_count()

        if veteran_tile in moveable_tiles:
            return True

        return False

    def _determine_player_ap_to_utilize(self, player: PlayerModel) -> int:
        """
        Determine the number of AP that the player
        can utilize in attempting to reach the Veteran.

        :param player:
        :return: AP that the player is allowed to spend
        """
        ap = player.ap
        # Rescue specialist's special AP are used for moving
        if player.role == PlayerRoleEnum.RESCUE:
            ap = ap + player.special_ap

        # Since the player has to reach the Veteran by moving
        # at most 3 spaces (all Safe spaces), the number of AP
        # that is required to reach the Veteran is at most 6
        # if carrying victim/hazmat or 3 if not carrying anything.
        # (leading a victim doesn't change the cost for moving)
        # Setting the number of points this way will make sure
        # that the moveable tiles obtained for the player will
        # be no more than 3 spaces away from the player.
        if isinstance(player.carrying_victim, VictimModel) or isinstance(player.carrying_hazmat, HazmatModel):
            max_ap_allowed = 6
        else:
            max_ap_allowed = 3

        if ap > max_ap_allowed:
            return max_ap_allowed
        else:
            return ap
