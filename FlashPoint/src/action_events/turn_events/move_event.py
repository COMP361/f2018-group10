from typing import List
import time
import logging
from threading import Thread


from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.custom_event_enums import CustomEventEnum
from src.constants.state_enums import SpaceStatusEnum, SpaceKindEnum, DoorStatusEnum, VictimStateEnum, \
    GameKindEnum, PlayerRoleEnum, WallStatusEnum

from src.core.custom_event import CustomEvent
from src.core.event_queue import EventQueue
from src.models.game_board.door_model import DoorModel
from src.models.game_board.null_model import NullModel
from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.poi_model import POIModel
from src.models.game_units.victim_model import VictimModel

logger = logging.getLogger("FlashPoint")


class DijkstraTile(object):

    def __init__(self, tile_model: TileModel):
        game: GameStateModel = GameStateModel.instance()
        self.tile_model = game.game_board.get_tile_at(tile_model.row, tile_model.column)
        self.least_cost = 10000
        self.predecessor: DijkstraTile = NullModel()

    def __str__(self):
        dijkstra = "### Dijkstra Tile ###"
        tile_info = "Self: " + self.tile_model.__str__()
        least_cost = "Least cost: " + str(self.least_cost)
        if isinstance(self.predecessor, NullModel):
            pred_info = "Predecessor: " + self.predecessor.__str__() + "\n"
        else:
            pred_info = "Predecessor: ({row}, {column})\n".format(row=self.predecessor.tile_model.row, column=self.predecessor.tile_model.column)
        return '\n'.join([dijkstra, tile_info, least_cost, pred_info])


class PriorityQueue(object):

    def __init__(self):
        self._queue: List[DijkstraTile] = []

    def __str__(self):
        return ' '.join([str(i) for i in self._queue])

    def get_tiles(self) -> List[DijkstraTile]:
        return self._queue

    def is_empty(self) -> bool:
        if len(self._queue) == 0:
            return True
        return False

    def insert(self, d_tile: DijkstraTile):
        self._queue.append(d_tile)

    def _determine_return_index(self) -> int:
        """
        Obtain the index for the item
        to be returned from the queue

        :return:
        """
        item_to_return = self._queue[0]
        return_index = 0
        for index, item in enumerate(self._queue):
            if item.least_cost < item_to_return.least_cost:
                item_to_return = item
                return_index = index

        return return_index

    def poll(self) -> DijkstraTile:
        """
        Retrieve and remove the DijkstraTile
        with the least cost from the queue

        :return: same as above
        """
        index = self._determine_return_index()
        return self._queue.pop(index)

    def peek(self) -> DijkstraTile:
        """
        Retrieve the DijkstraTile with the
        least cost without removing
        it from the queue

        :return: same as above
        """
        index = self._determine_return_index()
        return self._queue[index]


class MoveEvent(TurnEvent):

    def __init__(self, dest: TileModel, moveable_tiles: List[TileModel]):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        # Check if player is commanding
        if game.command[0] and game.players_turn == game.command[0]:
            self.source: PlayerModel = game.command[0]
            self.fireman: PlayerModel = game.command[1]
        else:
            self.source = None
            self.fireman: PlayerModel = game.players_turn
        self.source_tile = None
        self.destination = game.game_board.get_tile_at(dest.row, dest.column)
        self.moveable_tiles = []
        for m_tile in moveable_tiles:
            self.moveable_tiles.append(game.game_board.get_tile_at(m_tile.row, m_tile.column))
        self.dijkstra_tiles: List[DijkstraTile] = []

    def _init_dijkstra_tiles(self, dest: TileModel):
        """
        Initialization of the DijkstraTile objects.
        The source tile will have distance 0 from source
        while others are initialized with large distance.

        :return: initialized list of Dijkstra tiles
        """
        src = self.game.game_board.get_tile_at(self.fireman.row, self.fireman.column)
        if src not in self.moveable_tiles:
            self.moveable_tiles.append(src)

        for t in self.moveable_tiles:
            self.dijkstra_tiles.append(DijkstraTile(t))

        for d_tile in self.dijkstra_tiles:
            if d_tile.tile_model.row == self.fireman.row and d_tile.tile_model.column == self.fireman.column:
                self.source_tile = d_tile
                self.source_tile.least_cost = 0
            if d_tile.tile_model.row == dest.row and d_tile.tile_model.column == dest.column:
                self.destination = d_tile

    def execute(self):
        logger.info(f"Executing MoveEvent from ({self.fireman.row}, "
                    f"{self.fireman.column}) to ({self.destination.row}, {self.destination.column})")
        self.game: GameStateModel = GameStateModel.instance()
        # initialize the Dijkstra tiles
        self._init_dijkstra_tiles(self.destination)
        # Insert the Dijkstra tiles
        # into the priority queue
        pq = PriorityQueue()
        for d_tile in self.dijkstra_tiles:
            pq.insert(d_tile)

        # Get the Dijkstra tile with the least cost.
        # Go through the list of all the Dijkstra tiles
        # and if any of those are adjacent to the current
        # tile, attempt to relax the cost to travel between
        # those tiles.
        while not pq.is_empty():
            current_d_tile = pq.peek()
            adjacent_tiles = current_d_tile.tile_model.adjacent_tiles
            for d_tile in pq.get_tiles():
                for direction, tile in adjacent_tiles.items():
                    if isinstance(tile, NullModel):
                        continue
                    if d_tile.tile_model.row == tile.row and d_tile.tile_model.column == tile.column:
                        self.relax_cost(direction, current_d_tile, d_tile)

            pq.poll()

        shortest_path = self.shortest_path()
        self.traverse_shortest_path(shortest_path)

    def relax_cost(self, direction: str, first_tile: DijkstraTile, second_tile: DijkstraTile):
        """
        If there is a cheaper way to get to the second tile
        from the first tile, the least cost of the second
        tile is changed to reflect that.

        :param direction: Direction from the first tile to the second
        :param first_tile:
        :param second_tile:
        :return:
        """
        if not self._is_path_clear(first_tile.tile_model, direction):
            return

        if second_tile.tile_model.space_status != SpaceStatusEnum.FIRE:
            # Can pass either Safe/Smoke to method
            cost_to_travel = self._determine_cost_to_move(second_tile.tile_model)
        else:
            if self._can_go_into_fire():
                cost_to_travel = self._determine_cost_to_move(second_tile.tile_model)
            else:
                return

        # If it is cheaper to take this new way from
        # the first tile, change the least cost for
        # the second tile to reflect that.
        if second_tile.least_cost > first_tile.least_cost + cost_to_travel:
            second_tile.least_cost = first_tile.least_cost + cost_to_travel
            second_tile.predecessor = first_tile

        return

    def shortest_path(self) -> List[DijkstraTile]:
        """
        Find the shortest path from the player's
        location to the destination chosen.

        :return:
        """
        # destination is same as the source,
        # shortest path involves destination only
        if self.destination == self.source_tile:
            return [self.destination]

        # backtrack from the destination to
        # get to the source (source will have
        # no predecessor). keep adding the
        # Dijkstra tiles to the path (it will
        # be in the reverse order).
        path = []
        tile_to_visit = self.destination
        path.append(tile_to_visit)
        should_stop = False
        while not should_stop:
            tile_to_visit = tile_to_visit.predecessor
            if isinstance(tile_to_visit, NullModel) or isinstance(tile_to_visit.predecessor, NullModel):
                should_stop = True

            path.append(tile_to_visit)

        # the source tile of the path
        # (located at the end of the
        # list) is the source tile of
        # this SPECIFIC path.
        #
        # if it does not match the
        # given source, then there is no
        # path between the source of the
        # graph and the destination.
        #
        # else, reverse the list to get
        # the path source->.....->destination
        # and return that
        if path[-1] == self.source_tile:
            path.reverse()
            return path

        else:
            return []

    def traverse_shortest_path(self, shortest_path: List[DijkstraTile]):
        """
        Make the fireman traverse the shortest
        path found - subtracting AP along the way,
        flipping POIs, saving victims and disposing
        hazmats (if we get out of the building).

        :param shortest_path:
        :return:
        """
        shortest_path.pop(0)
        for d_tile in shortest_path:
            self._deduct_player_points(d_tile.tile_model)
            self.resolve_hazmat_while_traveling(d_tile.tile_model)
            self.resolve_victim_while_traveling(d_tile.tile_model)

            # update the position of the fireman
            self.fireman.set_pos(d_tile.tile_model.row, d_tile.tile_model.column)

            # Check the associated models of the tile.
            # If it contains any POIs, flip them over.
            for assoc_model in d_tile.tile_model.associated_models:
                if isinstance(assoc_model, POIModel):
                    # If the POI is a False Alarm, simply remove it
                    # from the board and the tile. If it is a Victim,
                    # remove the POI from the board, tile and
                    # add a Victim in its place.
                    self.game.game_board.flip_poi(assoc_model)

            # Put to sleep so that we can see the
            # player move through the individual tiles
            time.sleep(0.75)

    def resolve_hazmat_while_traveling(self, target_tile: TileModel):
        """
        If player goes out of the building carrying
        a hazmat, dispose of that hazmat.

        :param target_tile: tile player is heading to
        :return:
        """
        if target_tile.space_kind == SpaceKindEnum.INDOOR:
            return

        if isinstance(self.fireman.carrying_hazmat, HazmatModel):
            self.fireman.carrying_hazmat.set_pos(-7, -7)
            self.fireman.carrying_hazmat = NullModel()

    def resolve_victim_while_traveling(self, target_tile: TileModel):
        """
        Family mode:
        If victim carried outside of building, victim has been saved.
        Experienced mode:
        If victim carried/led to ambulance, victim has been saved.

        Both cases:
        Increment number of victims saved in game state and
        dissociate victim from player.

        :param target_tile: Tile to which player travels with the victim
        :return:
        """
        if self.game.rules == GameKindEnum.EXPERIENCED:
            if target_tile.space_kind != SpaceKindEnum.AMBULANCE_PARKING:
                return

            # Target space is an Ambulance Parking spot.
            # If the target space does not match either
            # of the ambulance's current location tiles,
            # then the victim has not been brought to the
            # ambulance.
            game_board = self.game.game_board
            amb_first_tile = game_board.get_tile_at(game_board.ambulance.row, game_board.ambulance.column)
            amb_second_tile = game_board.get_other_parking_tile(amb_first_tile)
            eq_to_first = target_tile.row == amb_first_tile.row and target_tile.column == amb_first_tile.column
            eq_to_second = target_tile.row == amb_second_tile.row and target_tile.column == amb_second_tile.column
            if not eq_to_first and not eq_to_second:
                return

        # Family mode:
        # If the target tile is indoors,
        # we don't have to resolve the victim.
        else:
            if target_tile.space_kind == SpaceKindEnum.INDOOR:
                return

        # For Experienced mode, we only reach here
        # if the target space is equal to one of
        # the ambulance's current location tiles.
        if isinstance(self.fireman.carrying_victim, VictimModel):
            self.fireman.carrying_victim.state = VictimStateEnum.RESCUED
            thread = Thread(target=self.countdown)
            thread.start()
            self.game.victims_saved = self.game.victims_saved + 1
            # remove the victim from the list of active POIs on the board
            # and disassociate the victim from the player
            self.game.game_board.remove_poi_or_victim(self.fireman.carrying_victim)
            self.fireman.carrying_victim = NullModel()

        if isinstance(self.fireman.leading_victim, VictimModel):
            thread = Thread(target=self.countdown)
            thread.start()
            self.fireman.leading_victim.state = VictimStateEnum.RESCUED
            self.game.victims_saved = self.game.victims_saved + 1
            self.game.game_board.remove_poi_or_victim(self.fireman.leading_victim)
            self.fireman.leading_victim = NullModel()

    def countdown(self):
        EventQueue.post(CustomEvent(CustomEventEnum.ENABLE_VICTIM_SAVED_PROMPT))
        time.sleep(5)
        EventQueue.post(CustomEvent(CustomEventEnum.DISABLE_VICTIM_SAVED_PROMPT))

    def _deduct_player_points(self,tile_model:TileModel):
        """
        Deduct player points according to space status
        and player carrying victim/hazmat. (leading a
        victim does not change the points to deduct)

        :param tile_model: tile player is moving to
        :return:
        """
        pts_to_deduct = self._determine_cost_to_move(tile_model)

        if self.source:
            target = self.source
        else:
            target = self.fireman

        # If the fireman is a Rescue Specialist, subtract
        # from the special AP first and then from AP.
        # If any other type of fireman, just subtract from AP.
        if target.role == PlayerRoleEnum.RESCUE:
            while target.special_ap > 0 and pts_to_deduct > 0:
                target.special_ap = target.special_ap - 1
                pts_to_deduct = pts_to_deduct - 1

            if pts_to_deduct > 0:
                target.ap = target.ap - pts_to_deduct

        else:
            target.ap = target.ap - pts_to_deduct

    def _can_go_into_fire(self) -> bool:
        """
        Determines whether player can go
        into fire. If the player is:
        1. carrying a victim or
        2. carrying a hazmat or
        3. leading a victim or
        4. is a doge
        then he/she cannot go into the fire.

        :return: True if player can go into this
                fire space, False otherwise.
        """
        if isinstance(self.fireman.carrying_victim, VictimModel):
            return False
        if isinstance(self.fireman.carrying_hazmat, HazmatModel):
            return False
        if isinstance(self.fireman.leading_victim, VictimModel):
            return False
        if self.fireman.role == PlayerRoleEnum.DOGE:
            return False

        return True

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
        src_tile = self.game.game_board.get_tile_at(self.fireman.row, self.fireman.column)
        movement_dirn = self._determine_movement_direction(src_tile, target_tile)
        obstacle = src_tile.get_obstacle_in_direction(movement_dirn)
        is_damaged_wall = isinstance(obstacle, WallModel) and obstacle.wall_status == WallStatusEnum.DAMAGED
        is_doge = self.fireman.role == PlayerRoleEnum.DOGE

        space_status = target_tile.space_status
        cost_to_move = 1
        if space_status != SpaceStatusEnum.FIRE:
            if isinstance(self.fireman.carrying_victim, VictimModel):
                # If a Doge drags a victim, it costs 4 AP.
                if is_doge:
                    cost_to_move = 4
                else:
                    cost_to_move = 2

            if isinstance(self.fireman.carrying_hazmat, HazmatModel):
                cost_to_move = 2

            # It takes the Doge 2 AP to squeeze through a damaged wall.
            if is_doge and is_damaged_wall:
                cost_to_move = 2

        else:
            cost_to_move = 2

        return cost_to_move

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
        is_carrying_victim = isinstance(self.fireman.carrying_victim, VictimModel)
        # there is a destroyed door or a destroyed wall or no obstacle or an open door or a damaged wall
        if self.fireman.role == PlayerRoleEnum.DOGE:
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
            nb_src_tile: TileModel = src_tile.get_tile_in_direction(dirn)
            if isinstance(nb_src_tile, NullModel):
                continue

            if nb_src_tile.row == dest_tile.row and nb_src_tile.column == dest_tile.column:
                return dirn
