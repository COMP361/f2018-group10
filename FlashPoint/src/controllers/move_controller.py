from typing import List

import src.constants.color as Color
from src.UIComponents.interactable import Interactable
from src.action_events.turn_events.move_event import DijkstraTile, PriorityQueue, MoveEvent
from src.constants.state_enums import PlayerStatusEnum, PlayerRoleEnum
from src.controllers.controller import Controller
from src.core.networking import Networking
from src.models.game_units.hazmat_model import HazmatModel

from src.models.game_units.victim_model import VictimModel
from src.observers.player_observer import PlayerObserver
from src.core.event_queue import EventQueue
from src.models.game_board.null_model import NullModel
from src.sprites.tile_sprite import TileSprite
from src.models.game_units.player_model import PlayerModel
from src.constants.state_enums import DoorStatusEnum, SpaceStatusEnum, GameStateEnum
from src.models.game_board.door_model import DoorModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.sprites.game_board import GameBoard


class MoveController(PlayerObserver, Controller):

    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)

        if MoveController._instance:
            raise Exception("MoveController is a singleton")

        self.game_board_sprite = GameBoard.instance()
        self.current_player = current_player
        ap = self.current_player.ap
        # Rescue specialist's special AP are used for moving
        if self.current_player.role == PlayerRoleEnum.RESCUE:
            ap = ap + self.current_player.special_ap

        self.moveable_tiles = self._determine_reachable_tiles(
            self.current_player.row, self.current_player.column, ap)
        self.current_player.add_observer(self)
        GameStateModel.instance().game_board.reset_tiles_visit_count()

        MoveController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def _determine_reachable_tiles(self, row: int, column: int, ap: int) -> List[TileModel]:
        """
        Determines the list of tiles the player can
        move to based on their position and AP.
        (Includes the tile the player is located
        at presently i.e. the source tile)

        :param row: Current row of the player.
        :param column: Current column of the player.
        :param ap: Current AP of the player.
        :return: The list of tiles the player can move to based on their position and AP.
        """
        # Convention followed:
        # d_tile refers to a DijkstraTile
        # tile refers to a TileModel

        # moveable_tiles will be the
        # final list returned.
        moveable_tiles = []
        pq = PriorityQueue()
        is_carrying_victim = False
        is_carrying_hazmat = False
        if isinstance(self.current_player.carrying_victim, VictimModel):
            is_carrying_victim = True

        if isinstance(self.current_player.carrying_hazmat, HazmatModel):
            is_carrying_hazmat = True

        is_carrying_something = is_carrying_victim or is_carrying_hazmat

        # Get the tiles of the board. Remove the source tile
        # from the list since it has to be initialised as a
        # Dijkstra tile with least_cost = 0.
        game: GameStateModel = GameStateModel.instance()
        tiles = game.game_board.tiles
        tiles.remove(game.game_board.get_tile_at(row, column))
        # A dictionary to keep track of all the Dijkstra tiles.
        # The row, column acts as the key.
        dijkstra_tiles = {}
        for tile in tiles:
            dijkstra_tiles[str(tile.row) + ", " + str(tile.column)] = DijkstraTile(tile)

        src: TileModel = GameStateModel.instance().game_board.get_tile_at(row, column)
        moveable_tiles.append(src)
        source_tile = DijkstraTile(src)
        source_tile.least_cost = 0
        dijkstra_tiles[str(src.row) + ", " + str(src.column)] = source_tile
        pq.insert(source_tile)

        # Insert tiles into the PriorityQueue and keep
        # relaxing the cost to move between them until
        # the PriorityQueue is empty.
        while not pq.is_empty():
            current_d_tile = pq.peek()
            # Get the tiles adjacent to the current tile
            # and check if they can be relaxed.
            for direction, tile in current_d_tile.tile_model.adjacent_tiles.items():
                if isinstance(tile, NullModel):
                    continue
                d_tile = dijkstra_tiles.get(str(tile.row) + ", " + str(tile.column))
                can_travel_to = self._check_and_relax(direction, current_d_tile, d_tile, is_carrying_something, ap-current_d_tile.least_cost)
                # If it is possible to travel to the second tile,
                # add it to the moveable tiles and insert it into
                # the Priority Queue
                if can_travel_to:
                    moveable_tiles.append(d_tile.tile_model)
                    pq.insert(d_tile)

            pq.poll()

        return moveable_tiles

    def _check_and_relax(self, direction: str, first_tile: DijkstraTile, second_tile: DijkstraTile, is_carrying_something: bool, ap: int) -> bool:
        """
        Check if the player can move from the first tile
        to the second depending on whether they are carrying
        something or not and the AP they have. Update the least
        cost to get to the second tile accordingly.

        :param first_tile:
        :param second_tile:
        :return: A boolean indicating whether it is possible to
        reach the second tile from the first, keeping in mind
        all the restrictions.
        """
        if ap < 1:
            return False

        is_leading_victim = isinstance(self.current_player.leading_victim, VictimModel)

        has_obstacle = first_tile.tile_model.has_obstacle_in_direction(direction)
        obstacle = first_tile.tile_model.get_obstacle_in_direction(direction)
        # If the path from the first tile to the second is not hindered by anything
        # (i.e. there is a destroyed door or a destroyed wall or an open door or no obstacle)
        # then there exists the **possibility** of moving to the second tile.
        # Two cases then depending on whether the player is carrying a victim/hazmat or not.
        if not has_obstacle or (isinstance(obstacle, DoorModel) and obstacle.door_status == DoorStatusEnum.OPEN):
            second_tile_status = second_tile.tile_model.space_status
            # carrying a victim/hazmat
            if is_carrying_something:
                if second_tile_status != SpaceStatusEnum.FIRE and ap - 2 >= 0:
                    if second_tile.least_cost > first_tile.least_cost + 2:
                        second_tile.least_cost = first_tile.least_cost + 2
                        return True

            # not carrying a victim/hazmat
            else:
                if second_tile_status != SpaceStatusEnum.FIRE and ap - 1 >= 0:
                    if second_tile.least_cost > first_tile.least_cost + 1:
                        second_tile.least_cost = first_tile.least_cost + 1
                        return True

                # If moving to a tile with fire, determine the reachable tiles
                # from this tile itself. Since the source tile is included in
                # the moveable tiles list, if the length of the list < 2, then
                # we cannot go anywhere from this fire tile and therefore it
                # would not be valid to add it to the list. Return False.
                # (Also, cannot go to fire tile if leading a victim)
                if second_tile_status == SpaceStatusEnum.FIRE and not is_leading_victim and ap - 2 >= 0:
                    moveable_tiles_from_fire = self._determine_reachable_tiles(second_tile.tile_model.row, second_tile.tile_model.column, ap-2)
                    if len(moveable_tiles_from_fire) < 2:
                        return False

                    if second_tile.least_cost > first_tile.least_cost + 2:
                        second_tile.least_cost = first_tile.least_cost + 2
                        return True

        return False

    def _apply_highlight(self):
        for column in range(len(self.game_board_sprite.grid.grid)):  # First make them all hover_color to red
            for row in range(len(self.game_board_sprite.grid.grid[column])):

                tile_model = GameStateModel.instance().game_board.get_tile_at(row, column)
                tile = self.game_board_sprite.grid.grid[column][row]
                if self.run_checks(tile_model):
                    tile.highlight_color = Color.GREEN
                elif not self.run_checks(tile_model):
                    tile.highlight_color = None

    def run_checks(self, tile_model: TileModel) -> bool:
        if self.current_player != GameStateModel.instance().players_turn:
            return False
        return tile_model in self.moveable_tiles

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        if not self.run_checks(tile_model):
            menu_to_close.disable()
            return

        event = MoveEvent(tile_model, self.moveable_tiles)

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().send_to_server(event)

        menu_to_close.disable()

    def process_input(self, tile_sprite: TileSprite):
        tile_model = GameStateModel.instance().game_board.get_tile_at(tile_sprite.row, tile_sprite.column)

        if not self.run_checks(tile_model):
            tile_sprite.move_button.disable()
            return

        tile_sprite.move_button.enable()
        tile_sprite.move_button.on_click(self.send_event_and_close_menu, tile_model, tile_sprite.move_button)

    def update(self, event_queue: EventQueue):
        if GameStateModel.instance().state != GameStateEnum.MAIN_GAME:
            return
        self._apply_highlight()

    def player_ap_changed(self, updated_ap: int):
        self._update_moveable_tiles()

    def player_position_changed(self, x_pos: int, y_pos: int):
        self._update_moveable_tiles()

    def player_carry_changed(self, carry):
        self._update_moveable_tiles()

    def player_leading_victim_changed(self, leading_victim):
        self._update_moveable_tiles()

    def player_wins_changed(self, wins: int):
        pass

    def player_losses_changed(self, losses: int):
        pass

    def player_role_changed(self, role):
        pass
    def player_special_ap_changed(self, updated_ap: int):
        # If the player is not a Rescue Specialist/CAFS, a change
        # in the special AP will not affect the moveable tiles.
        if self.current_player.role not in [PlayerRoleEnum.RESCUE, PlayerRoleEnum.CAFS]:
            return

        self._update_moveable_tiles()

    def _update_moveable_tiles(self):
        GameStateModel.instance().game_board.reset_tiles_visit_count()
        ap = self.current_player.ap
        # Rescue specialist's special AP are used for moving
        if self.current_player.role == PlayerRoleEnum.RESCUE:
            ap = ap + self.current_player.special_ap

        self.moveable_tiles = self._determine_reachable_tiles(
            self.current_player.row, self.current_player.column, ap)
        GameStateModel.instance().game_board.reset_tiles_visit_count()

    def player_status_changed(self, status: PlayerStatusEnum):
        pass
