import pygame

from src.models.game_board import TileModel
from src.models.game_units.AmbulanceModel import AmbulanceModel


class AmbulanceSprite(pygame.sprite.Sprite):

    def __init__(self, tile: TileModel, ambulance: AmbulanceModel):
        super.__init__()
        self.tile_reference = tile
        self.ambulance_model = ambulance
