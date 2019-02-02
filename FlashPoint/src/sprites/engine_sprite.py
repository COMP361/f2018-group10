import pygame

from src.models.game_board import tile_model


class EngineSprite(pygame.sprite.Sprite):

    def __init__(self, tile: tile_model):
        super.__init__()
        self.tile_reference = tile