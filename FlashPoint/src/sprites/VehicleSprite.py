import pygame

from src.models.game_board import TileModel
from src.constants.enums.VehicleKindEnum import VehicleKindEnum
from src.models.game_units import VehicleModel


class VehicleSprite(pygame.sprite.Sprite):

    def __init__(self, tile: TileModel, vehicle_kind: VehicleKindEnum, vehicle_model: VehicleModel):
        super.__init__()
        self.tile_reference = tile
        self._vehicle = vehicle_kind
        self.vehicle_model = vehicle_model


    def get_vehicle_kind(self):
        return self._vehicle
