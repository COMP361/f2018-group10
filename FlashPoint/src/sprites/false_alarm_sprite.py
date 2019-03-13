import pygame
from src.UIComponents.file_importer import FileImporter
from src.models.game_units.poi_model import POIModel


class FalseAlarmSprite(pygame.sprite.Sprite):

    def __init__(self, poi: POIModel):
        super().__init__()
        self.image = FileImporter.import_image("media/all_markers/false_alarm.png")
        self.rect = self.image.get_rect()
        self.poi_model = poi
        self.row = poi.row
        self.column = poi.column

