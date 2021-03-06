import json
import logging
import random
from typing import List, Tuple, Dict

import src.constants.media_constants as MEDIA_CONSTS
from src.constants.main_constants import BOARD_DIMENSIONS
from src.constants.state_enums import SpaceKindEnum, SpaceStatusEnum, POIIdentityEnum, \
    DoorStatusEnum, POIStatusEnum, VictimStateEnum, ArrowDirectionEnum, VehicleOrientationEnum, GameBoardTypeEnum
from src.core.random_board_generator import BoardGenerator
from src.models.game_board.door_model import DoorModel
from src.models.game_board.edge_obstacle_model import EdgeObstacleModel
from src.models.game_board.null_model import NullModel
from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_units.ambulance_model import AmbulanceModel
from src.models.game_units.engine_model import EngineModel
from src.models.game_units.poi_model import POIModel
from src.models.game_units.victim_model import VictimModel
from src.models.model import Model

logger = logging.getLogger("FlashPoint")


class GameBoardModel(Model):
    """
    Class for aggregating all objects related to the game board itself, this means TileModels, PlayerModels
    etc. This class is created inside of GameStateModel.
    """

    def __init__(self, board_type: GameBoardTypeEnum, board_info=None):
        super().__init__()
        self._dimensions = (8, 10)
        self._ambulance_spots = []
        self._engine_spots = []
        self._board_type = board_type
        logger.info("Game board type: {bt}".format(bt=board_type))

        self._board_info = board_info

        self._tiles = None
        if self._board_type:
            self._tiles = self._determine_board_tiles()

        self._poi_bank = GameBoardModel._init_pois()
        self._active_pois = []
        self._ambulance = AmbulanceModel((8, 10))
        self._engine = EngineModel((8, 10))
        self._hotspot_bank: int = 0
        self._is_loaded = False

    def notify_all_observers(self):
        self._notify_active_poi()
        self._notify_walls_and_tiles()

    def _notify_walls_and_tiles(self):

        for tile in self.tiles:
            for obs in tile.observers:
                obs.tile_status_changed(tile.space_status)

            for edge in tile.adjacent_edge_objects.values():
                if isinstance(edge, NullModel):
                    continue

                if isinstance(edge, WallModel):
                    for obs in edge.observers:
                        obs.wall_status_changed(edge.wall_status)
                elif isinstance(edge, DoorModel):
                    for obs in edge.observers:
                        obs.door_status_changed(edge.door_status)

    # def _notify_pois(self):
    #     for poi in self.active_pois:
    #         for obs in poi.observers:
    #             obs.poi_status_changed(poi.status)
    #             obs.poi_position_changed(poi.row, poi.column)

    def _notify_active_poi(self):
        for obs in self._observers:
            obs.notify_active_poi(self._active_pois)

    def get_tiles(self) -> List[List[TileModel]]:
        return self._tiles

    @property
    def is_loaded(self) -> bool:
        """Return whether this board was loaded from a file"""
        return self._is_loaded

    @is_loaded.setter
    def is_loaded(self, loaded: bool):
        self._is_loaded = loaded

    @property
    def board_type(self):
        return self._board_type

    @property
    def dimensions(self) -> Tuple[int, int]:
        return self._dimensions

    @property
    def ambulance(self) -> AmbulanceModel:
        return self._ambulance

    @property
    def engine(self) -> EngineModel:
        return self._engine

    @property
    def hotspot_bank(self) -> int:
        return self._hotspot_bank

    @hotspot_bank.setter
    def hotspot_bank(self, num_hotspots: int):
        self._hotspot_bank = num_hotspots
        logger.info("{nh} hotspots left in bank".format(nh=num_hotspots))

    @property
    def tiles(self) -> List[TileModel]:
        tile_list = []
        for row in range(len(self._tiles)):
            for column in range(len(self._tiles[row])):
                tile_list.append(self.get_tile_at(row, column))
        return tile_list
    @tiles.setter
    def tiles(self, tiles):
        self._tiles = tiles

    @property
    def ambulance_spots(self) -> List[Tuple[TileModel]]:
        return self._ambulance_spots

    @ambulance_spots.setter
    def ambulance_spots(self, ambulance_spots: List[Tuple[TileModel]]):
        self._ambulance_spots = ambulance_spots

    @property
    def engine_spots(self) -> List[Tuple[TileModel]]:
        return self._engine_spots

    @engine_spots.setter
    def engine_spots(self, engine_spots: List[Tuple[TileModel]]):
        self._engine_spots = engine_spots

    @property
    def active_pois(self):
        return self._active_pois

    @active_pois.setter
    def active_pois(self, pois: List[POIModel]):
        self._active_pois = pois

    def add_poi_or_victim(self, poi_or_victim):
        self._active_pois.append(poi_or_victim)
        self._notify_active_poi()

    def remove_poi_or_victim(self, poi_or_victim):
        # Put to sleep briefly so that POI or
        # victim can be seen before it is removed.
        if poi_or_victim in self._active_pois:
            if isinstance(poi_or_victim, POIModel):
                poi_or_victim.status = POIStatusEnum.LOST
            # elif isinstance(poi_or_victim, VictimModel):
            #     poi_or_victim.state = VictimStateEnum.LOST
            else:
                pass
            self._active_pois.remove(poi_or_victim)
            self._notify_active_poi()

    def get_random_poi_from_bank(self) -> POIModel:
        number = random.randint(0, len(self._poi_bank)-1)
        poi = self._poi_bank[number]
        return poi

    @property
    def poi_bank(self) -> List[POIModel]:
        return self._poi_bank

    @poi_bank.setter
    def poi_bank(self, bank: List[POIModel]):
        self._poi_bank = bank

    def remove_from_poi_bank(self, poi: POIModel):
        self._poi_bank.remove(poi)

    def get_poi_from_bank_by_index(self, index: int) -> POIModel:
        return self._poi_bank[index]

    @staticmethod
    def _init_pois():
        pois = []
        # POIs initialized with negative coordinates
        # since they are not on the board
        for i in range(10):
            pois.append(POIModel(POIIdentityEnum.VICTIM))
        for i in range(5):
            pois.append(POIModel(POIIdentityEnum.FALSE_ALARM))
        return pois

    @staticmethod
    def _load_family_fire_locations() -> List[Tuple[int, int]]:
        """Load the locations of the fires as a list of tuples from json file."""
        with open(MEDIA_CONSTS.FAMILY_FIRE_LOCATIONS, "r", encoding="utf-8") as f:
            return [tuple(x) for x in json.load(f)]

    def _determine_tile_kind(self, row: int, column: int) -> SpaceKindEnum:
        """Return whether this tile should be indoor or outdoor based on the positions."""
        outdoor = any([row == 0, row == self._dimensions[0]-1, column == 0, column == self._dimensions[1]-1])
        return SpaceKindEnum.OUTDOOR if outdoor else SpaceKindEnum.INDOOR

    def _determine_board_tiles(self) -> List[List[TileModel]]:
        """
        Determines the tiles for the board depending
        on the board type: Original, Alternative, Random

        :return: A list of list of tile models that will act as the board
        """
        amb_engine_parking_fname = ""
        outside_doors_fname = ""
        inside_walls_doors_fname = ""
        if self.board_type == GameBoardTypeEnum.ORIGINAL:
            amb_engine_parking_fname = MEDIA_CONSTS.ORIGINAL_AMBULANCE_ENGINE_LOCATIONS
            outside_doors_fname = MEDIA_CONSTS.ORIGINAL_OUTSIDE_DOOR_LOCATIONS
            inside_walls_doors_fname = MEDIA_CONSTS.ORIGINAL_INSIDE_WALLS_DOORS

        elif self.board_type == GameBoardTypeEnum.ALTERNATIVE:
            amb_engine_parking_fname = MEDIA_CONSTS.ALTERNATIVE_AMBULANCE_ENGINE_LOCATIONS
            outside_doors_fname = MEDIA_CONSTS.ALTERNATIVE_OUTSIDE_DOOR_LOCATIONS
            inside_walls_doors_fname = MEDIA_CONSTS.ALTERNATIVE_INSIDE_WALLS_DOORS

        elif self.board_type == GameBoardTypeEnum.RANDOM:
            if not self._board_info:
                BoardGenerator(8, 6, 1, 3).generate_inside_walls_doors()
            amb_engine_parking_fname = MEDIA_CONSTS.ORIGINAL_AMBULANCE_ENGINE_LOCATIONS
            outside_doors_fname = MEDIA_CONSTS.ORIGINAL_OUTSIDE_DOOR_LOCATIONS
            inside_walls_doors_fname = "media/board_layouts/random_inside_walls_doors.json"

        return self._init_all_tiles_board(amb_engine_parking_fname, outside_doors_fname, inside_walls_doors_fname)

    def _init_all_tiles_board(self, amb_engine_parking_fname: str, outside_doors_fname: str, inside_walls_doors_fname: str) -> List[List[TileModel]]:
        """
        Create all tiles for the board and set their adjacencies.

        :param amb_engine_parking_fname: Name of file that contains details about the ambulance
                                        and engine parking spaces
        :param outside_doors_fname: Name of file that contains details about the outside doors
        :param inside_walls_doors_fname: Name of file that contains details about the inside walls/doors
        :return: A list of list of tile models that will act as the board
        """
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
        self.set_parking_spaces(amb_engine_parking_fname, tiles)

        # setting the doors present on the outside of the house EXPLICITLY
        self.set_outside_doors(outside_doors_fname, tiles)

        # setting the walls and doors present inside the house
        self.set_inside_walls_doors(inside_walls_doors_fname, tiles)

        # setting the arrow directions given for the inside tiles
        self.set_all_tiles_arrows(MEDIA_CONSTS.TILE_ARROW_DIRECTIONS, tiles)

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
                extended_grid[i][j].set_adjacent_tile("North", extended_grid[i - 1][j])
                extended_grid[i][j].set_adjacent_tile("East", extended_grid[i][j + 1])
                extended_grid[i][j].set_adjacent_tile("West", extended_grid[i][j - 1])
                extended_grid[i][j].set_adjacent_tile("South", extended_grid[i + 1][j])

    def set_parking_spaces(self, parking_spaces_file: str, tiles: List[List[TileModel]]):
        """
        Sets the Ambulance and Engine parking spaces of the board
        and adds those spaces to the ambulance spots list and
        engine spots list.

        :param parking_spaces_file: Name of JSON file containing the details of the parking spaces.
        :param tiles: tiles of the board
        :return:
        """
        with open(parking_spaces_file, "r") as f:
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

    def set_outside_doors(self, outside_doors_file: str, tiles: List[List[TileModel]]):
        """
        Set the doors present on the outside of the house.

        :param outside_doors_file: Name of JSON file containing the details of the outside doors.
        :param tiles: tiles of the board
        :return:
        """
        with open(outside_doors_file, "r") as f:
            outside_doors = json.load(f)

        for out_door_adj in outside_doors:
            door = DoorModel(out_door_adj['first_pair'][0], out_door_adj['first_pair'][1], out_door_adj['first_dirn'], DoorStatusEnum.OPEN)
            self.set_single_obstacle(tiles, out_door_adj, door)

    def set_inside_walls_doors(self, inside_walls_doors_file: str, tiles: List[List[TileModel]]):
        """
        Set the walls and doors present inside the house.

        :param inside_walls_doors_file: Name of the JSON file containing the details of the inside walls/doors.
        :param tiles: tiles of the board
        :return:
        """
        if not self._board_info:
            with open(inside_walls_doors_file, "r") as f:
                inner_adjacencies = json.load(f)
                if self.board_type == GameBoardTypeEnum.RANDOM:
                    self._board_info = inner_adjacencies
        else:
            inner_adjacencies = self._board_info
        for adjacency in inner_adjacencies:
            if adjacency['obstacle_type'] == 'wall':
                obstacle = WallModel(adjacency['first_pair'][0], adjacency['first_pair'][1], adjacency['first_dirn'])
            else:
                obstacle = DoorModel(adjacency['first_pair'][0], adjacency['first_pair'][1], adjacency['first_dirn'])

            self.set_single_obstacle(tiles, adjacency, obstacle)

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

    def get_tile_at(self, row: int, column: int) -> TileModel:
        """Grab the TileModel at a given position"""
        return self._tiles[row][column]

    def set_fires_family(self):
        """Set all necessary tiles to on fire when starting a family game."""
        locations = GameBoardModel._load_family_fire_locations()

        for location in locations:
            self.get_tile_at(location[0], location[1]).space_status = SpaceStatusEnum.FIRE

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

    def set_all_tiles_arrows(self, tile_arrows_file: str, tiles: List[List[TileModel]]):
        """
        Set the arrow direction for all the tiles of the board.

        :param tile_arrows_file: Name of JSON file containing details about arrows of the tiles.
        :param tiles: tiles of the board
        :return:
        """
        with open(tile_arrows_file, "r") as f:
            all_tiles_arrows = [tuple(x) for x in json.load(f)]

        for row_num, row in enumerate(all_tiles_arrows):
            for col_num, tile_dirn in enumerate(row):
                if tile_dirn == "North":
                    tile_dirn = ArrowDirectionEnum.NORTH
                elif tile_dirn == "North-East":
                    tile_dirn = ArrowDirectionEnum.NORTH_EAST
                elif tile_dirn == "East":
                    tile_dirn = ArrowDirectionEnum.EAST
                elif tile_dirn == "South-East":
                    tile_dirn = ArrowDirectionEnum.SOUTH_EAST
                elif tile_dirn == "South":
                    tile_dirn = ArrowDirectionEnum.SOUTH
                elif tile_dirn == "South-West":
                    tile_dirn = ArrowDirectionEnum.SOUTH_WEST
                elif tile_dirn == "West":
                    tile_dirn = ArrowDirectionEnum.WEST
                elif tile_dirn == "North-West":
                    tile_dirn = ArrowDirectionEnum.NORTH_WEST
                else:
                    tile_dirn = ArrowDirectionEnum.NO_DIRECTION

                tiles[row_num][col_num].arrow_dirn = tile_dirn

    def get_other_parking_tile(self, first_tile: TileModel) -> TileModel:
        """Get the other parking spot tile if this one is a parking tile"""
        parking_type = first_tile.space_kind
        if parking_type not in [SpaceKindEnum.AMBULANCE_PARKING, SpaceKindEnum.ENGINE_PARKING]:
            raise Exception("Tile is not a parking space!")

        if first_tile.row == 0 or first_tile.row == self.dimensions[0] - 1:
            offset = 1 if first_tile.column < self.dimensions[1] - 1 else -1
            potential_tile = self.get_tile_at(first_tile.row, first_tile.column + offset)

            if potential_tile.space_kind == parking_type:
                return potential_tile

            offset = -1 if first_tile.column > 0 else 1
            potential_tile = self.get_tile_at(first_tile.row, first_tile.column + offset)

            if potential_tile.space_kind == parking_type:
                return potential_tile
        elif first_tile.column == 0 or first_tile.column == self.dimensions[1] - 1:
            offset = 1 if first_tile.row < self.dimensions[0] - 1 else -1
            potential_tile = self.get_tile_at(first_tile.row + offset, first_tile.column)

            if potential_tile.space_kind == parking_type:
                return potential_tile

            offset = -1 if first_tile.row > 0 else 1
            potential_tile = self.get_tile_at(first_tile.row + offset, first_tile.column)

            if potential_tile.space_kind == parking_type:
                return potential_tile

    def get_parking_space_orientation(self, spot: Tuple[TileModel, TileModel]) -> VehicleOrientationEnum:
        if any(tile.space_kind not in [SpaceKindEnum.ENGINE_PARKING, SpaceKindEnum.AMBULANCE_PARKING] for tile in spot):
            raise Exception("Tried to get orientation on tiles that are not Parking Spaces!")

        if spot[0].row == spot[1].row + 1 or spot[0].row == spot[1].row - 1:
            return VehicleOrientationEnum.VERTICAL
        else:
            return VehicleOrientationEnum.HORIZONTAL

    def get_distance_to_parking_spot(self, vehicle_type: str, destination: Tuple[TileModel, TileModel]):
        vehicle = self.ambulance if vehicle_type == "AMBULANCE" else self.engine
        origin_first_tile = self.get_tile_at(vehicle.row, vehicle.column)
        origin_second_tile = self.get_other_parking_tile(origin_first_tile)
        origin_spot = (origin_first_tile, origin_second_tile)

        first_orientation = self.get_parking_space_orientation(origin_spot)
        second_orientation = self.get_parking_space_orientation(destination)

        # Grab the rows/columns of each tile. If after removing duplicates theres only 1 entry, then the same.
        rows = set([tile.row for tile in origin_spot + destination])
        columns = set([tile.column for tile in origin_spot + destination])

        if len(rows) == 1 or len(columns) == 1:
            return 0

        return 1 if first_orientation != second_orientation else 2

    def flip_poi(self, poi: POIModel):
        """Reveal a POI adding Victims if necessary"""
        new_victim = None
        tile_model = self.get_tile_at(poi.row, poi.column)
        # If the POI is a Victim, instantiate a VictimModel
        # and add it to the tile, board.
        if poi.identity == POIIdentityEnum.VICTIM:
            new_victim = VictimModel(VictimStateEnum.ON_BOARD)
            new_victim.set_pos(poi.row, poi.column)
            tile_model.add_associated_model(new_victim)
            self.add_poi_or_victim(new_victim)
        poi.reveal(new_victim)

        tile_model.remove_associated_model(poi)
        self.remove_poi_or_victim(poi)
