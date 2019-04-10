import logging
import math
from typing import List

from src.UIComponents.interactable import Interactable
from src.constants.state_enums import PlayerRoleEnum, PlayerStatusEnum
from src.controllers.controller import Controller
from src.controllers.move_controller import MoveController
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.victim_model import VictimModel
from src.observers.player_observer import PlayerObserver
from src.sprites.game_board import GameBoard
from src.sprites.tile_sprite import TileSprite

logger = logging.getLogger("FlashPoint")


class VeteranController(Controller, PlayerObserver):
    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)
        if VeteranController._instance:
            raise Exception("VeteranController is a singleton")

        self.game_board_sprite = GameBoard.instance()

        for player in GameStateModel.instance().players:
            player.add_observer(self)

        self.move_cont = MoveController(current_player)
        self.game: GameStateModel = GameStateModel.instance()
        self.board = self.game.game_board
        self.game.add_observer(self)
        # Force notify observers
        self.game.state = self.game.state
        VeteranController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def _disable_all_menus(self):
        grid = self.game_board_sprite.grid.grid
        for column in range(len(grid)):
            for row in range(len(grid[column])):
                tile = grid[column][row]
                tile.disable_all()

    @staticmethod
    def __del__():
        VeteranController._instance = None
        MoveController._instance = None

    def veteran_give_experience(self):
        """
        Give 1 free AP to the CURRENT player
        in the vicinity of the Veteran if applicable.
        Give the dodge ability to ALL the players
        in the vicinity of the Veteran if applicable,
        else take that ability away.

        :return:
        """
        # Check if there is a Veteran
        # amongst the players
        veteran = None
        for player in self.game.players:
            if player.role == PlayerRoleEnum.VETERAN:
                veteran = player

        if not veteran:
            return

        veteran_vicinity = self._determine_vicinity_veteran(veteran.row, veteran.column)
        if self._current_player == veteran:
            return

        can_player_reach_vet = self._can_player_reach_veteran(self._current_player, veteran, veteran_vicinity)
        if not can_player_reach_vet:
            # If player cannot reach Veteran,
            # they can no longer dodge
            self._current_player.allowed_to_dodge = False
            return

        # Current player can only
        # receive extra AP once per turn
        if not self._current_player.has_AP_from_veteran:
            self._current_player.ap = self._current_player.ap + 1
            self._current_player.has_AP_from_veteran = True

        # Player always allowed to dodge
        # as long as in vicinity of Veteran
        self._current_player.allowed_to_dodge = True

        # Give the rest of the players the
        # ability to dodge if they are in
        # the vicinity of the Veteran else
        # take that ability away
        for p in self.game.players:
            if p == veteran or p == self._current_player:
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

    def process_input(self, tile_sprite: TileSprite):
        pass

    def run_checks(self, tile_model: TileModel) -> bool:
        pass

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        pass

    def player_status_changed(self, status: PlayerStatusEnum):
        pass

    def player_ap_changed(self, updated_ap: int):
        self.veteran_give_experience()

    def player_special_ap_changed(self, updated_ap: int):
        self.veteran_give_experience()

    def player_position_changed(self, row: int, column: int):
        self.veteran_give_experience()

    def player_wins_changed(self, wins: int):
        pass

    def player_losses_changed(self, losses: int):
        pass

    def player_carry_changed(self, carry):
        self.veteran_give_experience()

    def player_role_changed(self, role: PlayerRoleEnum):
        self.veteran_give_experience()

    def player_leading_victim_changed(self, leading_victim):
        self.veteran_give_experience()
