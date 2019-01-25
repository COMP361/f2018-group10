from typing import Optional

import pygame
from constants.enums.DirectionEnum import DirectionEnum
from core.exceptions.TilePositionOutOfBoundsException import TilePositionOutOfBoundsException

from src.constants.enums.SpaceKindEnum import SpaceKindEnum
from src.constants.enums.SpaceStatusEnum import SpaceStatusEnum


class TileModel(object):
    """Logical state of a Tile object."""

    def __init__(self, x_coord: int, y_coord: int, space_kind: SpaceKindEnum):
        self._x_coord = x_coord
        self._y_coord = y_coord
        self._space_kind = space_kind
        self._space_state = SpaceStatusEnum.SAFE
        self._hotspot = False
        self._game_unit_sprites = pygame.sprite.Group()

        self._adjacent_tiles = {
            DirectionEnum.NORTH: None,
            DirectionEnum.EAST: None,
            DirectionEnum.WEST: None,
            DirectionEnum.SOUTH: None,
        }

        self._adjacent_edge_object = {
            DirectionEnum.NORTH: None,
            DirectionEnum.EAST: None,
            DirectionEnum.WEST: None,
            DirectionEnum.SOUTH: None,
        }

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

    def game_unit_sprites(self):
        return self._game_unit_sprites

    def get_tile_in_direction(self, direction: DirectionEnum):
        """
        Get the TileModel in a specified direction.
        "raise TilePositionOutOfBoundsException: If there is no Tile in that direction.
        """
        tile = self._adjacent_tiles.get(direction, None)
        if not tile:
            raise TilePositionOutOfBoundsException(self, direction)
        return tile

    def get_wall_in_direction(self, direction: DirectionEnum):
        """
        Get the EdgeObstacle model
        :return:
        """
        pass

    # def add_game_unit_sprite(self, game_unit_sprite: GameUnitSprite):
    #     """TODO: Should check if valid sprite type."""
    #     self._game_unit_sprites.add(game_unit_sprite)

