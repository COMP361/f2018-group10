import pygame

<<<<<<< HEAD:FlashPoint/src/sprites/VehicleSprite.py
from src.models.game_board import TileModel
from src.constants.enums.vehicle_kind_enum import VehicleKindEnum
from src.models.game_units import VehicleModel
=======
from src.models.game_board import tile_model
from src.constants.enums.VehicleKindEnum import VehicleKindEnum
from src.models.game_units import vehicle_model
>>>>>>> GSD-Alek:FlashPoint/src/sprites/vehicle_sprite.py


class VehicleSprite(pygame.sprite.Sprite):

    def __init__(self, tile: tile_model, vehicle_kind: VehicleKindEnum, vehicle_model: vehicle_model):
        super.__init__()
        self.tile_reference = tile
        self._vehicle = vehicle_kind
        self.vehicle_model = vehicle_model


    def get_vehicle_kind(self):
        return self._vehicle
