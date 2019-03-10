from abc import ABC
from typing import List

from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import SpaceStatusEnum, POIIdentityEnum, SpaceKindEnum
from src.models.game_board.null_model import NullModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.poi_model import POIModel
from src.models.game_units.victim_model import VictimModel


class DijkstraTile(object):

    def __init__(self, tile_model: TileModel):
        self.tile_model = tile_model
        self.least_cost = 10000
        self.predecessor = NullModel()

    def __str__(self):
        # return f"{self.tile_model.__str__()}\nLeast cost: {self.least_cost}\nPredecessor: {self.predecessor.__str__()}\n"
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
        self.game: GameStateModel = GameStateModel.instance()
        self.fireman: PlayerModel = self.game.players_turn
        self.source_tile = self.game.game_board.get_tile_at(self.fireman.row, self.fireman.column)
        self.destination = dest
        self.moveable_tiles = moveable_tiles
        self.dijkstra_tiles: List[DijkstraTile] = []

    def _init_dijkstra_tiles(self, dest: TileModel):
        """
        Initialization of the DijkstraTile objects.
        The source tile will have distance 0 from source
        while others are initialized with large distance.

        :return: initialized list of Dijkstra tiles
        """
        d_source = DijkstraTile(self.source_tile)
        d_source.least_cost = 0
        self.source_tile = d_source
        self.dijkstra_tiles.append(self.source_tile)
        for t in self.moveable_tiles:
            self.dijkstra_tiles.append(DijkstraTile(t))

        for d_tile in self.dijkstra_tiles:
            # if d_tile.tile_model.row == self.fireman.row and d_tile.tile_model.column == self.fireman.column:
            #     print("Source tile set")
            #     self.source_tile = d_tile
            #     self.source_tile.least_cost = 0
            if d_tile.tile_model.row == dest.row and d_tile.tile_model.column == dest.column:
                self.destination = d_tile
                break

    def execute(self):
        # initialize the Dijkstra tiles
        self._init_dijkstra_tiles(self.destination)
        print("Dijkstra tiles set:")
        [print(d_tile) for d_tile in self.dijkstra_tiles]
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
            for d_tile in pq.get_tiles():
                if d_tile.tile_model in current_d_tile.tile_model.adjacent_tiles.values():
                    self.relax_cost(current_d_tile, d_tile)
            pq.poll()

        shortest_path = self.shortest_path()
        print("Path taken:")
        [print(p_tile) for p_tile in shortest_path]
        self.traverse_shortest_path(shortest_path)
        print("After moving:")
        print(self.fireman)
        return

    def relax_cost(self, first_tile: DijkstraTile, second_tile: DijkstraTile):
        """
        If there is a cheaper way to get to the second tile
        from the first tile, the least cost of the second
        tile is changed to reflect that.

        :param first_tile:
        :param second_tile:
        :return:
        """
        cost_to_travel = 0
        # Two separate cases depending on whether
        # fireman is carrying a victim or not.

        # fireman is carrying a victim
        if isinstance(self.fireman.carrying_victim, VictimModel):
            if second_tile.tile_model.space_status != SpaceStatusEnum.FIRE:
                cost_to_travel = 2

        # fireman is not carrying a victim
        else:
            if second_tile.tile_model.space_status != SpaceStatusEnum.FIRE:
                cost_to_travel = 1
            else:
                cost_to_travel = 2

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
        flipping POIs and saving victims if we have
        reached the outside of the building.

        :param shortest_path:
        :return:
        """
        shortest_path.pop(0)
        for d_tile in shortest_path:
            # Two separate cases depending on whether
            # fireman is carrying a victim or not

            # Fireman is carrying a victim
            # 2 AP to carry victim through Safe or
            # Smoke space. If victim carried outside
            # of building, victim has been saved.
            # Increment number of victims saved in game
            # state and dissociate victim from player.
            if isinstance(self.fireman.carrying_victim, VictimModel):
                if d_tile.tile_model.space_status != SpaceStatusEnum.FIRE:
                    self.fireman.ap -= 2
                    if d_tile.tile_model.space_kind != SpaceKindEnum.INDOOR:
                        self.game.victims_saved += 1
                        self.fireman.carrying_victim = NullModel()

            # fireman is not carrying a victim
            else:
                if d_tile.tile_model.space_status != SpaceStatusEnum.FIRE:
                    self.fireman.ap -= 1
                else:
                    self.fireman.ap -= 2

            # update the position of the fireman
            self.fireman.set_pos(d_tile.tile_model.row, d_tile.tile_model.column)

            # Check the associated models of the tile.
            # If it contains any POIs, flip them over.
            # If the POI is a False Alarm, remove it.
            for assoc_model in d_tile.tile_model.associated_models:
                if isinstance(assoc_model, POIModel):
                    assoc_model.reveal()
                    if assoc_model.identity == POIIdentityEnum.FALSE_ALARM:
                        d_tile.tile_model.remove_associated_model(assoc_model)
                        self.game.game_board.remove_poi_or_victim(assoc_model)


# class MoveEvent(TurnEvent):
#
#     def __init__(self, fireman: PlayerModel, destination: TileModel, moveable_tiles: List[TileModel]):
#         super().__init__()
#         self.fireman = fireman
#         self.game: GameStateModel = GameStateModel.instance()
#         self.source_tile = DijkstraTile(self.game.game_board.get_tile_at(self.fireman.row, self.fireman.column))
#         self.destination = DijkstraTile(destination)
#         moveable_tiles.remove(self.source_tile)
#         self.moveable_tiles = moveable_tiles
#
#     def execute(self):
#         """Guessing what has to be done is to make everything sync up with the networking"""
#         # initialize the Djikstra tiles and
#         # insert them into the priority queue
#         dijkstra_tiles = self._init_dijkstra_tiles()
#         pq = PriorityQueue()
#         for d_tile in dijkstra_tiles:
#             pq.insert(d_tile)
#
#         while not pq.is_empty():
#             current_d_tile = pq.peek()
#             for d_tile in dijkstra_tiles:
#                 if d_tile in current_d_tile.tile_model.adjacent_tiles:
#                     self.relax_cost(current_d_tile, d_tile, pq)
#
#             pq.poll()
#
#
    # def _init_dijkstra_tiles(self):
    #     """
    #     Initialization of the DjikstraTile objects.
    #     The source tile will have distance 0 from source
    #     while others are initialized with large distance.
    #
    #     :return: initialized list of Dijkstra tiles
    #     """
    #     dijkstra_tiles = []
    #     source_tile = DijkstraTile(self.source_tile)
    #     source_tile.least_cost = 0
    #     dijkstra_tiles.append(source_tile)
    #
    #     for t in self.moveable_tiles:
    #         dijkstra_tiles.append(DijkstraTile(t))
    #
    #     return dijkstra_tiles
#
#     def relax_cost(self, first_tile: DijkstraTile, second_tile: DijkstraTile, pq: PriorityQueue):
#         """
#         If there is a cheaper way to get to the second tile
#         from the first tile, the least cost of the second
#         tile is changed to reflect that.
#
#         :param first_tile:
#         :param second_tile:
#         :return:
#         """
#         cost_to_travel = 0
#         # Two separate cases depending on whether
#         # fireman is carrying a victim or not
#
#         # fireman is carrying a victim
#         if isinstance(self.fireman.carrying_victim, VictimModel):
#             if second_tile.tile_model.space_status != SpaceStatusEnum.FIRE:
#                 cost_to_travel = 2
#
#         # fireman is not carrying a victim
#         else:
#             if second_tile.tile_model.space_status != SpaceStatusEnum.FIRE:
#                 cost_to_travel = 1
#             else:
#                 cost_to_travel = 2
#
#         if second_tile.least_cost > first_tile.least_cost + cost_to_travel:
#             second_tile.least_cost = first_tile.least_cost + cost_to_travel
#             second_tile.predecessor = first_tile
#
#     def shortest_path(self):

