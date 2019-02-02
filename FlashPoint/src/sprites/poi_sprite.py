import pygame

from src.models.game_board import tile_model
from src.models.game_units import poi_model


class POISprite(pygame.sprite.Sprite):

    def __init__(self, tile: tile_model, poi: poi_model):
        super.__init__()
        self.tile_reference = tile
        self.poi_model = poi
