import pygame
from src.models.game_units import hazmat_model


class HazMatSprite(pygame.sprite.Sprite):

    def __init__(self, tile, hazmat: hazmat_model):
        super().__init__()
        self.tile_reference = tile
        self.hazmat_model = hazmat
