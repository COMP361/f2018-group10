from typing import List

import src.constants.color as Color
from src.action_events.turn_events.move_event import DijkstraTile, PriorityQueue
from src.constants.state_enums import PlayerStatusEnum

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


class MoveController(PlayerObserver):

    def player_carry_changed(self, carry):
        GameStateModel.instance().game_board.reset_tiles_visit_count()
        self.moveable_tiles = self._determine_reachable_tiles(
            self.current_player.row, self.current_player.column, self.current_player.ap)
        GameStateModel.instance().game_board.reset_tiles_visit_count()

    _instance = None

    def __init__(self, current_player: PlayerModel):
        if MoveController._instance:
            raise Exception("MoveController is a singleton")
        self.game_board_sprite = GameBoard.instance()
        self.current_player = current_player
        self.moveable_tiles = self._determine_reachable_tiles(
            self.current_player.row, self.current_player.column, self.current_player.ap)
        self.current_player.add_observer(self)
        GameStateModel.instance().game_board.reset_tiles_visit_count()
        MoveController._instance = self
        self.move_to = None
        self.is_moveable = False

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
        if isinstance(self.current_player.carrying_victim, VictimModel):
            is_carrying_victim = True

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
                can_travel_to = self._check_and_relax(direction, current_d_tile, d_tile, is_carrying_victim, ap-current_d_tile.least_cost)
                # If it is possible to travel to the second tile,
                # add it to the moveable tiles and insert it into
                # the Priority Queue
                if can_travel_to:
                    moveable_tiles.append(d_tile.tile_model)
                    pq.insert(d_tile)

            pq.poll()

        return moveable_tiles

    def _check_and_relax(self, direction: str, first_tile: DijkstraTile, second_tile: DijkstraTile, is_carrying_victim: bool, ap: int) -> bool:
        """
        Check if the player can move from the first tile
        to the second depending on whether they are carrying
        a victim or not and the AP they have. Update the least
        cost to get to the second tile accordingly.

        :param first_tile:
        :param second_tile:
        :return: A boolean indicating whether it is possible to
        reach the second tile from the first, keeping in mind
        all the restrictions.
        """
        if ap < 1:
            return False

        has_obstacle = first_tile.tile_model.has_obstacle_in_direction(direction)
        obstacle = first_tile.tile_model.get_obstacle_in_direction(direction)
        # If the path from the first tile to the second is not hindered by anything
        # (i.e. there is a destroyed door or a destroyed wall or an open door or no obstacle)
        # then there exists the **possibility** of moving to the second tile.
        # Two cases then depending on whether the player is carrying a victim or not.
        if not has_obstacle or (isinstance(obstacle, DoorModel) and obstacle.door_status == DoorStatusEnum.OPEN):
            second_tile_status = second_tile.tile_model.space_status
            # carrying a victim
            if is_carrying_victim:
                if second_tile_status != SpaceStatusEnum.FIRE and ap - 2 >= 0:
                    if second_tile.least_cost > first_tile.least_cost + 2:
                        second_tile.least_cost = first_tile.least_cost + 2
                        return True

            # not carrying a victim
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
                if second_tile_status == SpaceStatusEnum.FIRE and ap - 2 >= 0:
                    moveable_tiles_from_fire = self._determine_reachable_tiles(second_tile.tile_model.row, second_tile.tile_model.column, ap-2)
                    if len(moveable_tiles_from_fire) < 2:
                        return False

                    if second_tile.least_cost > first_tile.least_cost + 2:
                        second_tile.least_cost = first_tile.least_cost + 2
                        return True

        return False

    def _run_checks(self, tile_model: TileModel) -> bool:
        if self.current_player != GameStateModel.instance().players_turn:
            return False
        # self._determine_reachable_tiles(self.current_player.row, self.current_player.column, self.current_player.ap)
        return tile_model in self.moveable_tiles

    def process_input(self, tile_sprite: TileSprite):
        tile_model = GameStateModel.instance().game_board.get_tile_at(tile_sprite.row, tile_sprite.column)

        # close the menu when other tile is clicked
        if self.move_to:
            self.move_to.disable_move()
            self.move_to = None

        if not self._run_checks(tile_model):
            tile_sprite.disable_move()
            self.is_moveable = False
            return

        self.move_to = tile_sprite
        self.move_to.enable_move()
        self.is_moveable = True

    def update(self, event_queue: EventQueue):
        if GameStateModel.instance().state != GameStateEnum.MAIN_GAME:
            return

        for column in range(len(self.game_board_sprite.grid.grid)):  # First make them all hover_color to red
            for row in range(len(self.game_board_sprite.grid.grid[column])):

                tile_model = GameStateModel.instance().game_board.get_tile_at(row, column)
                tile = self.game_board_sprite.grid.grid[column][row]
                if self._run_checks(tile_model):
                    tile.highlight_color = Color.GREEN
                elif not self._run_checks(tile_model):
                    tile.highlight_color = None

    def player_status_changed(self, status: PlayerStatusEnum):
        pass

    def player_ap_changed(self, updated_ap: int):
        GameStateModel.instance().game_board.reset_tiles_visit_count()
        self.moveable_tiles = self._determine_reachable_tiles(
            self.current_player.row, self.current_player.column, self.current_player.ap)
        GameStateModel.instance().game_board.reset_tiles_visit_count()

    def player_special_ap_changed(self, updated_ap: int):
        pass

    def player_position_changed(self, x_pos: int, y_pos: int):
        GameStateModel.instance().game_board.reset_tiles_visit_count()
        self.moveable_tiles = self._determine_reachable_tiles(
            self.current_player.row, self.current_player.column, self.current_player.ap)
        GameStateModel.instance().game_board.reset_tiles_visit_count()

    def player_wins_changed(self, wins: int):
        pass

    def player_losses_changed(self, losses: int):
        pass
