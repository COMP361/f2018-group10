import json
import random
import time
from typing import List, Tuple, Dict

from src.constants.main_constants import BOARD_DIMENSIONS
from src.models.game_board.edge_obstacle_model import EdgeObstacleModel
from src.models.game_board.null_model import NullModel
from src.models.game_units.poi_model import POIModel
from src.models.game_board.tile_model import TileModel
from src.constants.state_enums import GameKindEnum, SpaceKindEnum, SpaceStatusEnum, POIIdentityEnum, DirectionEnum, \
    DoorStatusEnum, WallStatusEnum
from src.models.game_board.wall_model import WallModel
from src.models.game_board.door_model import DoorModel

class GameBoardModel(object):
    """
    Class for aggregating all objects related to the game board itself, this means TileModels, PlayerModels
    etc. This class is created inside of GameStateModel.
    """

    def __init__(self, game_type: GameKindEnum):
        self._dimensions = (8, 10)
        self._ambulance_spots = []
        self._engine_spots = []
        self._tiles = self._init_all_tiles_family_classic() if game_type == GameKindEnum.FAMILY else None
        self._poi_bank = GameBoardModel._init_pois()
        self._active_pois = []
        self.set_initial_poi_family()

    def get_tiles(self) -> List[List[TileModel]]:
        return self._tiles

    @property
    def tiles(self) -> List[TileModel]:
        tile_list = []
        for row in range(len(self._tiles)):
            for column in range(len(self._tiles[row])):
                tile_list.append(self.get_tile_at(row, column))
        return tile_list

    @property
    def ambulance_spots(self) -> List[Tuple[TileModel]]:
        return self._ambulance_spots

    @property
    def engine_spots(self) -> List[Tuple[TileModel]]:
        return self._engine_spots

    @property
    def active_pois(self):
        return self._active_pois

    def add_poi_or_victim(self, poi_or_victim):
        self._active_pois.append(poi_or_victim)

    def remove_poi_or_victim(self, poi_or_victim):
        # Put to sleep briefly so that POI or
        # victim can be seen before it is removed.
        time.sleep(0.5)
        if poi_or_victim in self._active_pois:
            if poi_or_victim.row >= 0 and poi_or_victim.column >= 0:
                poi_or_victim.set_position(-7, -7)
            self._active_pois.remove(poi_or_victim)

    def get_random_poi_from_bank(self) -> POIModel:
        number = random.randint(0, len(self._poi_bank)-1)
        poi = self._poi_bank.pop(number)
        return poi

    @staticmethod
    def _init_pois():
        pois = []
        # POIs initialized with negative coordinates
        # since they are not on the board
        for i in range(5):
            pois.append(POIModel(POIIdentityEnum.VICTIM))
        for i in range(5):
            pois.append(POIModel(POIIdentityEnum.FALSE_ALARM))
        return pois

    @staticmethod
    def _load_family_fire_locations() -> List[Tuple[int, int]]:
        """Load the locations of the fires as a list of tuples from json file."""
        with open("media/board_layouts/family_fire_locations.json", "r", encoding="utf-8") as f:
            return [tuple(x) for x in json.load(f)]

    def _determine_tile_kind(self, row: int, column: int) -> SpaceKindEnum:
        """Return whether this tile should be indoor or outdoor based on the positions."""
        outdoor = any([row == 0, row == self._dimensions[0]-1, column == 0, column == self._dimensions[1]-1])
        return SpaceKindEnum.OUTDOOR if outdoor else SpaceKindEnum.INDOOR

    def _init_all_tiles_family_classic(self) -> List[List[TileModel]]:
        """Create all tiles and set their adjacency. """
        tiles = []

        for i in range(self._dimensions[0]):
            tiles.append([])
            for j in range(self._dimensions[1]):
                tile_kind = self._determine_tile_kind(i, j)
                tile = TileModel(i, j, tile_kind)
                tiles[i].append(tile)

        # setting tile adjacencies
        self.set_adjacencies(tiles)

        # setting the top and bottom walls on the outside of the house
        for top, bottom in [(0, 1), (6, 7)]:
            for i in range(1, 9):
                wall = WallModel(top, i, "South")
                tiles[top][i].set_adjacent_edge_obstacle("South", wall)
                tiles[bottom][i].set_adjacent_edge_obstacle("North", wall)

        # setting the left and right walls on the outside of the house
        for left, right in [(0, 1), (8, 9)]:
            for i in range(1, 7):
                wall = WallModel(i, left, "East")
                tiles[i][left].set_adjacent_edge_obstacle("East", wall)
                tiles[i][right].set_adjacent_edge_obstacle("West", wall)

        # setting the ambulance and engine parking spaces
        with open("media/board_layouts/engine_ambulance_locations.json", "r") as f:
            parking_spots = json.load(f)
            
        for park_spot in parking_spots:
            first_x, first_y = park_spot['first_tile']
            second_x, second_y = park_spot['second_tile']
            first_tile = tiles[first_x][first_y]
            second_tile = tiles[second_x][second_y]
            if park_spot['parking_type'] == "Ambulance":
                first_tile.space_kind = SpaceKindEnum.AMBULANCE_PARKING
                second_tile.space_kind = SpaceKindEnum.AMBULANCE_PARKING
                self.ambulance_spots.append((first_tile, second_tile))
            else:
                first_tile.space_kind = SpaceKindEnum.ENGINE_PARKING
                second_tile.space_kind = SpaceKindEnum.ENGINE_PARKING
                self.engine_spots.append((first_tile, second_tile))

        # setting the doors present on the outside of the house EXPLICITLY
        with open("media/board_layouts/outside_door_locations.json", "r") as f:
            outside_doors = json.load(f)

        for out_door_adj in outside_doors:
            door = DoorModel(out_door_adj['first_pair'][0], out_door_adj['first_pair'][1], out_door_adj['first_dirn'], DoorStatusEnum.OPEN)
            self.set_single_obstacle(tiles, out_door_adj, door)

        # setting the walls and doors present inside the house
        with open("media/board_layouts/tiles_adjacencies.json", "r") as f:
            inner_adjacencies = json.load(f)

        for adjacency in inner_adjacencies:
            if adjacency['obstacle_type'] == 'wall':
                obstacle = WallModel(adjacency['first_pair'][0], adjacency['first_pair'][1], adjacency['first_dirn'])
            else:
                obstacle = DoorModel(adjacency['first_pair'][0], adjacency['first_pair'][1], adjacency['first_dirn'])

            self.set_single_obstacle(tiles, adjacency, obstacle)

        return tiles

    def set_adjacencies(self, tiles: List[List[TileModel]]):
        extended_grid = []
        for row in tiles:
            extended_grid.append([NullModel()] + row + [NullModel()])

        row_length = len(tiles[0])
        extra_top_row = [NullModel() for x in range(row_length + 2)]
        extra_bottom_row = [NullModel() for x in range(row_length + 2)]
        extended_grid = [extra_top_row] + extended_grid + [extra_bottom_row]

        for i in range(1, len(extended_grid) - 1):
            for j in range(1, len(extended_grid[0]) - 1):
                extended_grid[i][j].north_tile = extended_grid[i - 1][j]
                extended_grid[i][j].east_tile = extended_grid[i][j + 1]
                extended_grid[i][j].west_tile = extended_grid[i][j - 1]
                extended_grid[i][j].south_tile = extended_grid[i + 1][j]

    def set_single_tile_adjacencies(self, tile: TileModel):
        # set north tile
        if tile.row == 0:
            tile.set_adjacent_tile("North", NullModel())
        else:
            tile.set_adjacent_tile("North", self.get_tile_at(tile.row - 1, tile.column))

        # set east tile
        if tile.column == BOARD_DIMENSIONS[1] - 1:
            tile.set_adjacent_tile("East", NullModel())
        else:
            tile.set_adjacent_tile("East", self.get_tile_at(tile.row, tile.column + 1))

        # set west tile
        if tile.column == 0:
            tile.set_adjacent_tile("West", NullModel())
        else:
            tile.set_adjacent_tile("West", self.get_tile_at(tile.row, tile.column - 1))

        # set south tile
        if tile.row == BOARD_DIMENSIONS[0] - 1:
            tile.set_adjacent_tile("South", NullModel())
        else:
            tile.set_adjacent_tile("South", self.get_tile_at(tile.row + 1, tile.column))

    def set_single_obstacle(self, tiles: List[List[TileModel]], adjacency: Dict, obstacle: EdgeObstacleModel):
        first_pair, second_pair = adjacency['first_pair'], adjacency['second_pair']
        first_dirn, second_dirn = adjacency['first_dirn'], adjacency['second_dirn']
        for coord, direction in [(first_pair, first_dirn), (second_pair, second_dirn)]:
            tiles[coord[0]][coord[1]].set_adjacent_edge_obstacle(direction, obstacle)

    def _init_all_tiles_experienced_classic(self):
        pass

    def get_tile_at(self, row: int, column: int) -> TileModel:
        """Grab the TileModel at a given position"""
        return self._tiles[row][column]

    def set_fires_family(self):
        """Set all necessary tiles to on fire when starting a classic family game."""
        locations = GameBoardModel._load_family_fire_locations()

        for location in locations:
            self.get_tile_at(location[0], location[1]).space_status = SpaceStatusEnum.FIRE

    def set_initial_poi_family(self):
        """
        Set active POI's and their positions for a family game.
        Set all initial POIlocations for a family game.
        Returns the locations that were randomly chosen for reuse in the PlacePOIEvent
        """

        locations = [[2, 4], [5, 1], [5, 8]]

        for i in range(3):
            poi = self.get_random_poi_from_bank()
            # Location indices are inverted cause i wrote the list wrong lel
            row = locations[i][0]
            column = locations[i][1]
            poi.set_position(row, column)
            self._active_pois.append(poi)
            self.get_tile_at(row, column).add_associated_model(poi)

    def distance_between_tiles(self, first_tile: TileModel, second_tile: TileModel) -> int:
        return abs(first_tile.row - second_tile.row) + abs(first_tile.column - second_tile.column)

    def find_closest_parking_spots(self, parking_type: str, current_tile: TileModel) -> List[TileModel]:
        """
        Find the closest parking spot to a given position.

        :param parking_type: "Engine" or "Ambulance"
        :param current_tile:
        :return: A list of the closest parking spots (the closer tile for each parking spot)
        """
        min_distance = 100
        if parking_type == "Ambulance":
            parking_spots = self.ambulance_spots
        elif parking_type == "Engine":
            parking_spots = self.engine_spots
        else:
            pass

        spot_distances = {}
        for park_spot in parking_spots:
            first_tile = park_spot[0]
            second_tile = park_spot[1]

            dist_from_first_tile = self.distance_between_tiles(current_tile, first_tile)
            dist_from_second_tile = self.distance_between_tiles(current_tile, second_tile)
            # the smaller distance from the two tiles of the
            # parking spot will denote the overall distance
            # from the parking spot
            dist_from_spot = min(dist_from_first_tile, dist_from_second_tile)

            # determining the closer tile from the
            # two tiles of the parking spot
            if dist_from_first_tile < dist_from_second_tile:
                closer_tile_on_spot = first_tile
            else:
                closer_tile_on_spot = second_tile

            spot_key = first_tile.__str__() + second_tile.__str__()
            # a dictionary which maps the key of the spot to
            # the distance from that spot and the closer tile
            # of that spot
            spot_distances[spot_key] = (dist_from_spot, closer_tile_on_spot)

            # determining the minimum distance
            if dist_from_spot < min_distance:
                min_distance = dist_from_spot

        # make a list of the
        # closest parking spots
        closest_spots = []
        for spot_key, value in spot_distances.items():
            distance = value[0]
            closer_tile_on_spot = value[1]
            if distance == min_distance:
                closest_spots.append(closer_tile_on_spot)

        return closest_spots

    def reset_tiles_visit_count(self):
        for tile in self.tiles:
            tile.visit_count = 0
