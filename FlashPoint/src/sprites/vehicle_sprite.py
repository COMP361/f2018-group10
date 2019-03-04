import pygame

from src.constants.state_enums import VehicleKindEnum
from src.models.game_units import vehicle_model


class VehicleSprite(pygame.sprite.Sprite):
    def __init__(self, vehicle_kind: VehicleKindEnum):
        super().__init__(vehicle_model)
        self._vehicle = vehicle_kind
