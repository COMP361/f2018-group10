import pygame
from src.sprites.game_board import GameBoard
from src.core.event_queue import EventQueue
from src.UIComponents.file_importer import FileImporter
from src.models.game_units.poi_model import POIModel


class FalseAlarmSprite(pygame.sprite.Sprite):

    def __init__(self, poi: POIModel):
        super().__init__()
        self.image = FileImporter.import_image("src/media/all_markers/false_alarm.png")
        self.rect = self.image.get_rect()
        self.poi_model = poi
        self.row = poi.row
        self.column = poi.column
        self.tile_sprite = GameBoard.instance().grid.grid[poi.column][poi.row]

    def update(self, event_queue: EventQueue):
        new_x = self.tile_sprite.rect.x
        new_y = self.tile_sprite.rect.y
        self.rect.x = new_x
        self.rect.y = new_y

