import logging
from typing import List

import src.constants.color as Color
from src.UIComponents.interactable import Interactable
from src.action_events.turn_events.move_event import DijkstraTile, PriorityQueue, MoveEvent
from src.constants.state_enums import PlayerStatusEnum, PlayerRoleEnum, WallStatusEnum, VehicleOrientationEnum
from src.controllers.controller import Controller
from src.core.flashpoint_exceptions import TilePositionOutOfBoundsException
from src.core.networking import Networking
from src.models.game_board.wall_model import WallModel
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_units.poi_model import POIModel

from src.models.game_units.victim_model import VictimModel
from src.observers.player_observer import PlayerObserver
from src.core.event_queue import EventQueue
from src.models.game_board.null_model import NullModel
from src.observers.vehicle_observer import VehicleObserver
from src.sprites.tile_sprite import TileSprite
from src.models.game_units.player_model import PlayerModel
from src.constants.state_enums import DoorStatusEnum, SpaceStatusEnum, GameStateEnum
from src.models.game_board.door_model import DoorModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.sprites.game_board import GameBoard

logger = logging.info("FlashPoint")


class MoveController(VehicleObserver, PlayerObserver, Controller):

    def notify_passengers(self, passengers: List[PlayerModel]):
        self._update_moveable_tiles()

    def notify_vehicle_pos(self, orientation: VehicleOrientationEnum, row: int, column: int):
        pass

    def notify_active_poi(self, active_pois: List[POIModel]):
        pass

    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)

        if MoveController._instance:
            raise Exception("MoveController is a singleton")

        self.game_board_sprite = GameBoard.instance()
        self.current_player = current_player
        self._only_allow_safe_space = False
        ap = self.current_player.ap
        # Rescue specialist's special AP are used for moving
        if self.current_player.role == PlayerRoleEnum.RESCUE:
            ap = ap + self.current_player.special_ap

        self.moveable_tiles = self._determine_reachable_tiles(
            self.current_player.row, self.current_player.column, ap)
        self.current_player.add_observer(self)
        GameStateModel.instance().game_board.reset_tiles_visit_count()
        GameStateModel.instance().game_board.ambulance.add_observer(self)
        GameStateModel.instance().game_board.engine.add_observer(self)
        MoveController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    @property
    def only_allow_safe_space(self) -> bool:
        return self._only_allow_safe_space

    @only_allow_safe_space.setter
    def only_allow_safe_space(self, permission: bool):
        self._only_allow_safe_space = permission
        logger.info("Move controller: Allowing only safe space: {tf}".format(tf=permission))

    @property
    def target(self) -> PlayerModel:
        game: GameStateModel = GameStateModel.instance()
        source: PlayerModel = game.command[0]
        if source and self.current_player == source:
            return [player for player in game.players if player == game.command[1]][0]
        return self.current_player

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

        # If the player is riding a vehicle, they
        # cannot move until they dismount the vehicle
        game: GameStateModel = GameStateModel.instance()
        engine = game.game_board.engine
        ambulance = game.game_board.ambulance
        player_tile = game.game_board.get_tile_at(self.current_player.row, self.current_player.column)
        if self.current_player in engine.passengers:
            return [player_tile]

        if self.current_player in ambulance.passengers:
            return [player_tile]

        # moveable_tiles will be the
        # final list returned.
        moveable_tiles = []
        pq = PriorityQueue()
        is_carrying_victim = False
        is_carrying_hazmat = False
        if isinstance(self.target.carrying_victim, VictimModel):
            is_carrying_victim = True

        if isinstance(self.target.carrying_hazmat, HazmatModel):
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
                can_travel_to = self._check_and_relax(direction, current_d_tile, d_tile, ap-current_d_tile.least_cost)
                # If it is possible to travel to the second tile,
                # add it to the moveable tiles and insert it into
                # the Priority Queue
                if can_travel_to:
                    moveable_tiles.append(d_tile.tile_model)
                    pq.insert(d_tile)

            pq.poll()

        return moveable_tiles

    def _check_and_relax(self, direction: str, first_tile: DijkstraTile, second_tile: DijkstraTile, ap: int) -> bool:
        """
        Check if the player can move from the first tile
        to the second depending on the AP they have. Update
        the least cost to get to the second tile accordingly.

        :param first_tile:
        :param second_tile:
        :return: A boolean indicating whether it is possible to
        reach the second tile from the first, keeping in mind
        all the restrictions.
        """
        if ap < 1:
            return False

        is_leading_victim = isinstance(self.target.leading_victim, VictimModel)

        has_obstacle = first_tile.tile_model.has_obstacle_in_direction(direction)
        obstacle = first_tile.tile_model.get_obstacle_in_direction(direction)
        # If the path from the first tile to the second is not hindered by anything
        # then there exists the **possibility** of moving to the second tile.
        # Two cases then depending on whether the player is heading into a non-fire/fire space.
        if not self._is_path_clear(first_tile.tile_model, direction):
            return False

        second_tile_status = second_tile.tile_model.space_status
        # heading into a Safe/Smoke space
        if second_tile_status != SpaceStatusEnum.FIRE:
            if self._can_go_into_safe_smoke(ap, first_tile, second_tile):
                return True

        # heading into a Fire space
        else:
            # When moving to a tile with fire, determine the reachable tiles
            # from this tile itself. Since the source tile is included in
            # the moveable tiles list, if the length of the list < 2, then
            # we cannot go anywhere from this fire tile and therefore it
            # would not be valid to add it to the list. Return False.
            if self._can_go_into_fire(ap, second_tile.tile_model):
                moveable_tiles_from_fire = self._determine_reachable_tiles(second_tile.tile_model.row, second_tile.tile_model.column, ap-2)
                if len(moveable_tiles_from_fire) < 2:
                    return False

                cost_to_move = self._determine_cost_to_move(second_tile.tile_model)
                if self._could_update_least_cost(cost_to_move, first_tile, second_tile):
                    return True

        return False

    def _is_path_clear(self, tile_model: TileModel, dirn: str) -> bool:
        """
        Determines if there is an obstacle blocking the
        way from the tile in the direction 'dirn'.

        :param tile_model: tile the player is moving from
        :param dirn: direction from tile in which moving
        :return: True if the path from the first tile to
                the second is clear, False otherwise.
        """
        has_obstacle = tile_model.has_obstacle_in_direction(dirn)
        obstacle = tile_model.get_obstacle_in_direction(dirn)
        is_open_door = isinstance(obstacle, DoorModel) and obstacle.door_status == DoorStatusEnum.OPEN
        is_damaged_wall = isinstance(obstacle, WallModel) and obstacle.wall_status == WallStatusEnum.DAMAGED
        is_carrying_victim = isinstance(self.target.carrying_victim, VictimModel)
        # there is a destroyed door or a destroyed wall or no obstacle or an open door or a damaged wall
        if self.current_player.role == PlayerRoleEnum.DOGE:
            if not has_obstacle or is_open_door or is_damaged_wall:
                # The Doge is not allowed to carry a
                # victim through a damaged wall.
                if is_carrying_victim and is_damaged_wall:
                    return False
                else:
                    return True

        # there is a destroyed door or a destroyed wall or no obstacle or an open door
        else:
            if not has_obstacle or is_open_door:
                return True

        return False

    def _can_go_into_fire(self, ap: int, target_tile: TileModel) -> bool:
        """
        Determines whether player can go
        into fire. If the player is:
        1. carrying a victim or
        2. carrying a hazmat or
        3. leading a victim or
        4. is a doge or
        5. ap < cost to move
        then he/she cannot go into the fire.

        :param ap: player's AP
        :return: True if player can go into this
                fire space, False otherwise.
        """
        if self._only_allow_safe_space:
            return False
        if isinstance(self.target.carrying_victim, VictimModel):
            return False
        if isinstance(self.target.carrying_hazmat, HazmatModel):
            return False
        if isinstance(self.target.leading_victim, VictimModel):
            return False
        if self.target.role == PlayerRoleEnum.DOGE:
            return False

        cost_to_move = self._determine_cost_to_move(target_tile)
        if ap < cost_to_move:
            return False

        return True

    def _can_go_into_safe_smoke(self, ap: int, first_tile: DijkstraTile, second_tile: DijkstraTile) -> bool:
        """
        Determines whether player can go
        into safe/smoke space.

        :param ap: player's AP
        :param first_tile: tile player is moving from
        :param second_tile: tile player is moving to
        :return: True if player can go into this
                safe/smoke space, False otherwise.
        """
        if self._only_allow_safe_space:
            if second_tile.tile_model.space_status == SpaceStatusEnum.SMOKE:
                return False

        # Can pass either Safe or Smoke to method
        cost_to_move = self._determine_cost_to_move(second_tile.tile_model)
        if ap < cost_to_move:
            return False

        return self._could_update_least_cost(cost_to_move, first_tile, second_tile)

    def _determine_cost_to_move(self, target_tile: TileModel) -> int:
        """
        Determine the cost to move
        into a space depending on the
        space status and player carrying
        victim/hazmat. (leading a victim
        does not change the cost to move)

        :param target_tile:
        :return: cost to move into target tile
        """
        game: GameStateModel = GameStateModel.instance()
        src_tile = game.game_board.get_tile_at(self.target.row, self.target.column)
        movement_dirn = self._determine_movement_direction(src_tile, target_tile)
        obstacle = src_tile.get_obstacle_in_direction(movement_dirn)
        is_damaged_wall = isinstance(obstacle, WallModel) and obstacle.wall_status == WallStatusEnum.DAMAGED
        is_doge = self.current_player.role == PlayerRoleEnum.DOGE

        space_status = target_tile.space_status
        cost_to_move = 1
        if space_status != SpaceStatusEnum.FIRE:
            if isinstance(self.target.carrying_victim, VictimModel):
                # If a Doge drags a victim, it costs 4 AP.
                if is_doge:
                    cost_to_move = 4
                else:
                    cost_to_move = 2

            if isinstance(self.target.carrying_hazmat, HazmatModel):
                cost_to_move = 2

            # It takes the Doge 2 AP to squeeze through a damaged wall.
            if is_doge and is_damaged_wall:
                cost_to_move = 2

        else:
            cost_to_move = 2

        return cost_to_move

    def _could_update_least_cost(self, cost_to_move: int, first_tile: DijkstraTile, second_tile: DijkstraTile) -> bool:
        """
        Determine whether the least cost of the
        second tile could be updated while attempting
        to move from the 1st tile to the 2nd tile.

        :param cost_to_move: cost to move from 1st tile to 2nd tile
        :param first_tile: tile player is moving from
        :param second_tile: tile player is moving to
        :return: True if the least cost of the 2nd tile could be updated, False otherwise.
        """
        if second_tile.least_cost > first_tile.least_cost + cost_to_move:
            second_tile.least_cost = first_tile.least_cost + cost_to_move
            return True

        return False

    def _determine_movement_direction(self, src_tile: TileModel, dest_tile: TileModel) -> str:
        """
        Determine the direction from the
        source tile to the destination tile

        :param src_tile:
        :param dest_tile:
        :return: string representation of movement direction
        """
        directions = ["North", "East", "West", "South"]
        for dirn in directions:
            try:
                nb_src_tile: TileModel = src_tile.get_tile_in_direction(dirn)
                if nb_src_tile.row == dest_tile.row and nb_src_tile.column == dest_tile.column:
                    return dirn

            except TilePositionOutOfBoundsException:
                continue

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
            self.target.row, self.target.column, ap)
        GameStateModel.instance().game_board.reset_tiles_visit_count()

    def player_status_changed(self, status: PlayerStatusEnum):
        pass
