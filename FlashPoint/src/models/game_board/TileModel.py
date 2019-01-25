import pygame

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
        self._hotspot = False
        self._game_unit_sprites = pygame.sprite.Group()
        self._adjacent_tiles = []
        self._adjacent_walls = []

    @property
    def game_unit_sprites(self):
        return self._game_unit_sprites

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
