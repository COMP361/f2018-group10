import pygame

from src.models.game_board import tile_model
from src.models.game_units.ambulance_model import AmbulanceModel


class AmbulanceSprite(pygame.sprite.Sprite):

    def __init__(self, tile: tile_model, ambulance: AmbulanceModel):
        super.__init__()
        self.tile_reference = tile
        self.ambulance_model = ambulance
