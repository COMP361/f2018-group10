import json
import random
from typing import List, Tuple

from src.models.game_units.poi_model import POIModel
from src.models.game_board.tile_model import TileModel
from src.constants.state_enums import GameKindEnum, SpaceKindEnum, SpaceStatusEnum, POIIdentityEnum


class GameBoardModel(object):
    """
    Class for aggregating all objects related to the game board itself, this means TileModels, PlayerModels
    etc. This class is created inside of GameStateModel.
    """

    def __init__(self, game_type: GameKindEnum):
        self._dimensions = (10, 8)
        self._tiles = self._init_all_tiles_family_classic() if game_type == GameKindEnum.FAMILY else None
        self._poi_bank = GameBoardModel._init_pois()
        self._active_pois = []

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
        outdoor = any([row == 0, row == self._dimensions[0], column == 0, column == self._dimensions[1]])
        return SpaceKindEnum.OUTDOOR if outdoor else SpaceKindEnum.INDOOR

    def _init_all_tiles_family_classic(self) -> List[TileModel]:
        """Create all tiles and set their adjacency. """
        tiles = []

        for i in range(self._dimensions[0]*self._dimensions[1]):
            row = i % self._dimensions[0]
            column = int(i / self._dimensions[0])
            tile_kind = self._determine_tile_kind(row, column)
            tile = TileModel(row, column, tile_kind)
            tiles.append(tile)

        # TODO: Abhijay: setting adjacency and creating walls/doors.
        return tiles

    def _init_all_tiles_experienced_classic(self):
        pass

    def get_tile_at(self, row: int, column: int) -> TileModel:
        """Grab the tilemodel at a given position"""
        index = row*self._dimensions[0] + column
        return self._tiles[index]

    def set_fires_family(self):
        """Set all necessary tiles to on fire when starting a classic family game."""
        locations = GameBoardModel._load_family_fire_locations()

        for location in locations:
            self.get_tile_at(location[1], location[0]).space_status = SpaceStatusEnum.FIRE

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
            poi.x_pos = locations[i][1]
            poi.y_pos = locations[i][0]
            self._active_pois.append(poi)
            self.get_tile_at(poi.x_pos, poi.y_pos).add_associated_model(poi)
