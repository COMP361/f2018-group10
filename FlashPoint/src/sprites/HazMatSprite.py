import pygame
from src.models.game_board.TileModel import TileModel
from src.models.game_units import HazMatModel


class HazMatSprite(pygame.sprite.Sprite()):

    def __init__(self, tile: TileModel, hazmat: HazMatModel):
        super().__init__()
        self.tile_reference = tile
        self.hazmat_model = hazmat
