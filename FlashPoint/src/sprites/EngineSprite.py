import pygame

from src.models.game_board import TileModel


class EngineSprite(pygame.sprite.Sprite):

    def __init__(self, tile: TileModel):
        super.__init__()
        self.tile_reference = tile