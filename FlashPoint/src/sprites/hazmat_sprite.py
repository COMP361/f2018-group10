import pygame

from src.UIComponents.file_importer import FileImporter
from src.core.event_queue import EventQueue
from src.observers.hazmat_observers import HazmatObservers


class HazmatSprite(pygame.sprite.Sprite, HazmatObservers):

    def __init__(self, row: int, column: int):
        super().__init__()
        self.image = FileImporter.import_image("media/other_markers/Hazmat_Marker.png")
        self.rect = self.image.get_rect()
        self.row = row
        self.column = column

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)


    def hazmat_status_changed(self):
        pass
