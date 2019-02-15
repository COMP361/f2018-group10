import json
import random
from typing import List, Tuple

from src.models.game_units.poi_model import POIModel
from src.models.game_board.tile_model import TileModel
from src.constants.state_enums import GameKindEnum, SpaceKindEnum, SpaceStatusEnum, POITypeEnum


class GameBoardModel(object):
    """
    Class for aggregating all objects related to the game board itself, this means TileModels, PlayerModels
    etc. This class is created inside of GameStateModel.
    """

    def __init__(self, game_type: GameKindEnum):
        self._tiles = self._init_all_tiles_family_classic() if game_type == GameKindEnum.FAMILY else None
        self._dimensions = (10, 8)

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
            self.get_tile_at(location[0], location[1]).space_status = SpaceStatusEnum.FIRE

    def set_poi_family(self) -> List[Tuple[int, int]]:
        """
        Set all poi locations for a family game.
        Returns the locations that were randomly chosen for reuse in the PlacePOIEvent
        Chooses 3 POI's with probability 1/3 of being a false alarm and 2/3 of being a victim
        """
        pois = []
        for i in range(3):
            number = random.randint(1, 3)
            poi_type = POITypeEnum.FALSE_ALARM if number == 1 else POITypeEnum.VICTIM
            pois.append(POIModel(poi_type))

        # TODO: Would add the POI to the tiles here, but not sure how we're dealing with composition in Tile yet.

