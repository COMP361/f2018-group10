import pygame

from typing import Optional

from src.models.game_board.edge_obstacle_model import EdgeObstacleModel
from src.models.game_board.null_tile_model import NullTileModel

from src.sprites.fire_sprite import FireSprite
from src.sprites.smoke_sprite import SmokeSprite
from src.sprites.vehicle_sprite import VehicleSprite
from src.sprites.victim_sprite import VictimSprite
from src.sprites.game_unit_sprite import GameUnitSprite
from src.sprites.poi_sprite import POISprite
from src.sprites.hazmat_sprite import HazMatSprite

from src.constants.state_enums import DirectionEnum
from src.constants.state_enums import SpaceKindEnum
from src.constants.state_enums import SpaceStatusEnum


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
    #
    # @property
    # def north_tile(self):
    #     """
    #     Get the TileModel to the North of this one.
    #     :raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
    #     """
    #     tile = self._adjacent_tiles.get(DirectionEnum.NORTH, None)
    #     if not tile:
    #         raise TilePositionOutOfBoundsException(self, DirectionEnum.NORTH)
    #     return tile
    #
    # @north_tile.setter
    # def north_tile(self, tile):
    #     self._adjacent_tiles[DirectionEnum.NORTH] = tile
    #
    # @property
    # def east_tile(self):
    #     """
    #     Get the TileModel to the North of this one.
    #     :raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
    #     """
    #     tile = self._adjacent_tiles.get(DirectionEnum.EAST, None)
    #     if not tile:
    #         raise TilePositionOutOfBoundsException(self, DirectionEnum.EAST)
    #     return tile
    #
    # @east_tile.setter
    # def east_tile(self, tile):
    #     self._adjacent_tiles[DirectionEnum.EAST] = tile
    #
    # @property
    # def west_tile(self):
    #     """
    #     Get the TileModel to the  of this one.
    #     :raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
    #     """
    #     tile = self._adjacent_tiles.get(DirectionEnum.WEST, None)
    #     if not tile:
    #         raise TilePositionOutOfBoundsException(self, DirectionEnum.WEST)
    #     return tile
    #
    # @west_tile.setter
    # def west_tile(self, tile):
    #     self._adjacent_tiles[DirectionEnum.WEST] = tile
    #
    # @property
    # def south_tile(self):
    #     """
    #     Get the TileModel to the South of this one.
    #     :raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
    #     """
    #     tile = self._adjacent_tiles.get(DirectionEnum.SOUTH, None)
    #     if not tile:
    #         raise TilePositionOutOfBoundsException(self, DirectionEnum.SOUTH)
    #     return tile
    #
    # @south_tile.setter
    # def south_tile(self, tile):
    #     self._adjacent_tiles[DirectionEnum.SOUTH] = tile

    def set_adjacent_edge_obstacle(self, direction: DirectionEnum, edge_obstacle: EdgeObstacleModel):
        self._adjacent_edge_objects[direction] = edge_obstacle

    # def get_tile_in_direction(self, direction: DirectionEnum):
    #     """
    #     Get the TileModel in a specified direction.
    #     "raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
    #     """
    #     tile = self._adjacent_tiles.get(direction, None)
    #     if not tile:
    #         raise TilePositionOutOfBoundsException(self, direction)
    #     return tile

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
