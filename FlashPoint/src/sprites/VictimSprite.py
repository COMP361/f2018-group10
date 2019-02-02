import pygame

from src.models.game_board import TileModel
from src.models.game_units import VictimModel


class VictimSprite(pygame.sprite.Sprite):

    def __init__(self, tile: TileModel, victim: VictimModel):

        super.__init__()
        self.tile_reference = tile
        self.victim_model = victim
