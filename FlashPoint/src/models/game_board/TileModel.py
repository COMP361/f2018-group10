import pygame

from typing import Optional

from models.game_board.EdgeObstacleModel import EdgeObstacleModel
from models.game_board.NullTileModel import NullTileModel
from src.constants.enums.DirectionEnum import DirectionEnum
from src.core.exceptions.TilePositionOutOfBoundsException import TilePositionOutOfBoundsException
from src.sprites import CharacterSprite, FireSprite, SmokeSprite, HazMatSprite, VehicleSprite, VictimSprite
from src.sprites.GameUnitSprite import GameUnitSprite
from src.constants.enums.SpaceKindEnum import SpaceKindEnum
from src.constants.enums.SpaceStatusEnum import SpaceStatusEnum
from src.sprites.POISprite import POISprite
from src.sprites.HazMatSprite import HazMatSprite


class TileModel(object):
    """Logical state of a Tile object."""

    def __init__(self, x_coord: int, y_coord: int, space_kind: SpaceKindEnum):
        self._x_coord = x_coord
        self._y_coord = y_coord
        self._space_kind = space_kind
        self._space_state = SpaceStatusEnum.SAFE
        self._is_hotspot = False
        self._game_unit_sprites = pygame.sprite.Group()

        self._adjacent_tiles = {
            DirectionEnum.NORTH: NullTileModel(),
            DirectionEnum.EAST: NullTileModel(),
            DirectionEnum.WEST: NullTileModel(),
            DirectionEnum.SOUTH: NullTileModel(),
        }

        self._adjacent_edge_objects = {
            DirectionEnum.NORTH: NullTileModel(),
            DirectionEnum.EAST: NullTileModel(),
            DirectionEnum.WEST: NullTileModel(),
            DirectionEnum.SOUTH: NullTileModel(),
        }

    def __str__(self):
        return f"Tile at: ({self.x_coord}, {self.y_coord})."

    @property
    def x_coord(self):
        return self._x_coord

    @property
    def y_coord(self):
        return self._y_coord

    @property
    def space_kind(self):
        return self._space_kind

    @property
    def space_state(self):
        return self._space_state

    @property
    def is_hotspot(self):
        return self._is_hotspot

    @property
    def game_unit_sprites(self):
        return self._game_unit_sprites

    @property
    def adjacent_tiles(self):
        return self._adjacent_tiles

    @property
    def adjacent_edge_objects(self):
        return self._adjacent_edge_objects

    @property
    def north_tile(self):
        """
        Get the TileModel to the North of this one.
        :raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
        """
        tile = self._adjacent_tiles.get(DirectionEnum.NORTH, None)
        if not tile:
            raise TilePositionOutOfBoundsException(self, DirectionEnum.NORTH)
        return tile

    @north_tile.setter
    def north_tile(self, tile):
        self._adjacent_tiles[DirectionEnum.NORTH] = tile

    @property
    def east_tile(self):
        """
        Get the TileModel to the North of this one.
        :raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
        """
        tile = self._adjacent_tiles.get(DirectionEnum.EAST, None)
        if not tile:
            raise TilePositionOutOfBoundsException(self, DirectionEnum.EAST)
        return tile

    @east_tile.setter
    def east_tile(self, tile):
        self._adjacent_tiles[DirectionEnum.EAST] = tile

    @property
    def west_tile(self):
        """
        Get the TileModel to the  of this one.
        :raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
        """
        tile = self._adjacent_tiles.get(DirectionEnum.WEST, None)
        if not tile:
            raise TilePositionOutOfBoundsException(self, DirectionEnum.WEST)
        return tile

    @west_tile.setter
    def west_tile(self, tile):
        self._adjacent_tiles[DirectionEnum.WEST] = tile

    @property
    def south_tile(self):
        """
        Get the TileModel to the South of this one.
        :raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
        """
        tile = self._adjacent_tiles.get(DirectionEnum.SOUTH, None)
        if not tile:
            raise TilePositionOutOfBoundsException(self, DirectionEnum.SOUTH)
        return tile

    @south_tile.setter
    def south_tile(self, tile):
        self._adjacent_tiles[DirectionEnum.SOUTH] = tile

    def set_adjacent_edge_obstacle(self, direction: DirectionEnum, edge_obstacle: EdgeObstacleModel):
        self._adjacent_edge_objects[direction] = edge_obstacle

    def get_tile_in_direction(self, direction: DirectionEnum):
        """
        Get the TileModel in a specified direction.
        "raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
        """
        tile = self._adjacent_tiles.get(direction, None)
        if not tile:
            raise TilePositionOutOfBoundsException(self, direction)
        return tile

    def get_obstacle_in_direction(self, direction: DirectionEnum) -> Optional['TileModel']:
        """
        Get the EdgeObstacle model
        :return: EdgeObstacleModel in the direction specified, or None.
        """
        return self._adjacent_edge_objects.get(direction, None)

    # def add_game_unit_sprite(self, game_unit_sprite: GameUnitSprite):
    #     """TODO: Should check if valid sprite type."""
    #     self._game_unit_sprites.add(game_unit_sprite)


    def add_game_unit_sprite(self, game_unit_sprite: GameUnitSprite):
        """TODO: Make sure to add raising exceptions if the added game sprite is illegal"""
        type = game_unit_sprite.get_sprite()

        if self._space_kind == SpaceKindEnum.INDOOR:
            # Means only legal sprites on tiles should be POI, Character, Fire, Smoke, Hazmat

            if isinstance(type, POISprite) or isinstance(type, CharacterSprite) or isinstance(type, FireSprite) or isinstance(
                    type, SmokeSprite) or isinstance(type, HazMatSprite) or isinstance(type, VictimSprite):
                self._game_unit_sprites.add(game_unit_sprite)

        elif self._space_kind == SpaceKindEnum.OUTDOOR:
            # means we can also have Vehicle Models.
            # Cannot have fire, smoke , hazmat or POI out of th

            if isinstance(type, VehicleSprite) or isinstance(type, CharacterSprite):
                self._game_unit_sprites.add(game_unit_sprite)
