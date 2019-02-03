import pygame

from src.models.game_board import tile_model
from src.models.game_units import victim_model


class VictimSprite(pygame.sprite.Sprite):

    def __init__(self, tile: tile_model, victim: victim_model):

        super.__init__()
        self.tile_reference = tile
        self.victim_model = victim
