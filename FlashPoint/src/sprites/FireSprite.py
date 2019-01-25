import pygame

from src.models.game_board import TileModel
from src.models.game_units import FireModel


class FireSprite(pygame.sprite.Sprite):

    def __init__(self, tile: TileModel, fire: FireModel):
        super.__init__()
        self.tile_reference = tile
        self.fire_model = fire