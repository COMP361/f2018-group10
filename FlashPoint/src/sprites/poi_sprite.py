import pygame
from constants.state_enums import POIStatusEnum
from src.observers.poi_observer import POIObserver


class POISprite(pygame.sprite.Sprite, POIObserver):
    """Visual representation of a POI."""

    def __init__(self):
        super().__init__()

    def poi_status_changed(self, status: POIStatusEnum):
        pass

    def poi_position_changed(self, row: int, column: int):
        pass
