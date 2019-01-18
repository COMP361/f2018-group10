import pygame

from src.constants.enums.SpaceKind import SpaceKind
from src.constants.enums.SpaceState import SpaceState


class TileModel(object):
    """Logical state of a Tile object."""

    def __init__(self, x_coord: int, y_coord: int, space_kind: SpaceKind):
        self._x_coord = x_coord
        self._y_coord = y_coord
        self._space_kind = space_kind
        self._space_state = SpaceState.SAFE
        self._hotspot = False
        self._game_unit_sprites = pygame.sprite.Group()
        self._adjacent_tiles = []
        self._adjacent_walls = []

    @property
    def game_unit_sprites(self):
        return self._game_unit_sprites

    # def add_game_unit_sprite(self, game_unit_sprite: GameUnitSprite):
    #     """TODO: Should check if valid sprite type."""
    #     self._game_unit_sprites.add(game_unit_sprite)

