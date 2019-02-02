import pygame

from src.models.game_board import tile_model
from src.constants.state_enums import VehicleKindEnum
from src.models.game_units import vehicle_model


class VehicleSprite(pygame.sprite.Sprite):
    def __init__(self, tile: tile_model, vehicle_kind: VehicleKindEnum, vehicle_model: vehicle_model):
        super().__init__(vehicle_model)
        self.tile_reference = tile
        self._vehicle = vehicle_kind
        self.vehicle_model = vehicle_model

    def get_vehicle_kind(self):
        return self._vehicle
