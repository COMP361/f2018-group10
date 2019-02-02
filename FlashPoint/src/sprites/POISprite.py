import pygame

from src.models.game_board import TileModel
from src.models.game_units import POIModel


class POISprite(pygame.sprite.Sprite):

    def __init__(self, tile: TileModel, poi: POIModel):
        super.__init__()
        self.tile_reference = tile
        self.poi_model = poi
