import pygame

from src.models.game_board import tile_model
from src.models.game_units import smoke_model


class SmokeSprite(pygame.sprite.Sprite):

    def __init__(self, tile: tile_model, smoke: smoke_model):
        self.tile_reference = tile
        self.smoke_model = smoke