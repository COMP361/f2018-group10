import pygame

from src.models.game_board import tile_model
from src.models.game_units import fire_model


class FireSprite(pygame.sprite.Sprite):

    def __init__(self, tile: tile_model, fire: fire_model):
        super.__init__()
        self.tile_reference = tile
        self.fire_model = fire