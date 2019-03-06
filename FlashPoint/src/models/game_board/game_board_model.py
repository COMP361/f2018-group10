import json
import random
from typing import List, Tuple, Dict

from src.models.game_board.edge_obstacle_model import EdgeObstacleModel
from src.models.game_board.null_model import NullModel
from src.models.game_units.poi_model import POIModel
from src.models.game_board.tile_model import TileModel
from src.constants.state_enums import GameKindEnum, SpaceKindEnum, SpaceStatusEnum, POIIdentityEnum, \
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
        self._tiles = self._init_all_tiles_family_classic() if game_type == GameKindEnum.FAMILY else None
        self._poi_bank = GameBoardModel._init_pois()
        self._active_pois = []

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
    def active_pois(self) -> List[POIModel]:
        return self._active_pois

    def remove_poi(self, poi: POIModel):
        if poi in self._active_pois:
            self._active_pois.remove(poi)

    @staticmethod
    def _init_pois():
        pois = []
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

    def set_single_obstacle(self, tiles: List[List[TileModel]], adjacency: Dict, obstacle: EdgeObstacleModel):
        first_pair, second_pair = adjacency['first_pair'], adjacency['second_pair']
        first_dirn, second_dirn = adjacency['first_dirn'], adjacency['second_dirn']
        for coord, direction in [(first_pair, first_dirn), (second_pair, second_dirn)]:
            if direction == 'NORTH':
                direction = "North"
            elif direction == 'EAST':
                direction = "East"
            elif direction == 'WEST':
                direction = "West"
            else:
                direction = "South"

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
            number = random.randint(0, len(self._poi_bank))
            poi = self._poi_bank.pop(number)
            # Location indices are inverted cause i wrote the list wrong lel
            poi.x_pos = locations[i][0]
            poi.y_pos = locations[i][1]
            self._active_pois.append(poi)
            self.get_tile_at(poi.x_pos, poi.y_pos).add_associated_model(poi)

    def get_movable_tiles(self,x:int,y:int,ap:int,movable_tiles= []) -> List[TileModel]:

        #ap = action points
        currentTile = self.get_tile_at(x,y)
        if ap >= 1:
            for key in currentTile.adjacent_edge_objects.keys():
                tile = currentTile.adjacent_tiles.get(key)
                obstacle = currentTile.adjacent_edge_objects.get(key)

                if isinstance(obstacle,NullModel):
                    ap_deduct = 2 if tile.space_status == SpaceStatusEnum.FIRE else 1
                    if tile.space_status == SpaceStatusEnum.FIRE:
                        movable_tiles = self.get_movable_tiles(tile.x_coord, tile.y_coord, ap - ap_deduct, movable_tiles)
                    else:
                        movable_tiles.append(tile)
                        movable_tiles = self.get_movable_tiles(tile.x_coord, tile.y_coord, ap - ap_deduct, movable_tiles)
                elif isinstance(obstacle, WallModel):
                    if tile.wall_status == WallStatusEnum.DESTROYED:
                        movable_tiles.append(tile)
                        movable_tiles = self.get_movable_tiles(tile.x_coord, tile.y_coord, ap - 1, movable_tiles)
                elif isinstance(obstacle, DoorModel):
                    if (tile.door_status == DoorStatusEnum.OPEN or tile.door_status == DoorStatusEnum.DESTROYED):
                        movable_tiles.append(tile)
                        movable_tiles = self.get_movable_tiles(tile.x_coord, tile.y_coord, ap - ap_deduct, movable_tiles)

        output = list(dict.fromkeys(movable_tiles))
        return output
