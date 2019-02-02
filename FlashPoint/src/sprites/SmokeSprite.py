import pygame

from src.models.game_board import TileModel
from src.models.game_units import SmokeModel


class SmokeSprite(pygame.sprite.Sprite):

    def __init__(self, tile: TileModel, smoke: SmokeModel):
        self.tile_reference = tile
        self.smoke_model = smoke