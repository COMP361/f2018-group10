import pygame
from src.sprites.game_board import GameBoard
from src.core.event_queue import EventQueue

from src.UIComponents.file_importer import FileImporter
from src.constants.state_enums import POIStatusEnum
from src.observers.poi_observer import POIObserver


class POISprite(pygame.sprite.Sprite, POIObserver):
    """Visual representation of a POI."""

    def __init__(self, row: int, column: int):
        super().__init__()
        self.image = FileImporter.import_image("media/all_markers/poi.png")
        self.rect = self.image.get_rect()
        self.row = row
        self.column = column
        self.tile_sprite = GameBoard.instance().grid.grid[column][row]

    def poi_status_changed(self, status: POIStatusEnum):
        pass

    def poi_position_changed(self, row: int, column: int):
        self.tile_sprite = GameBoard.instance().grid.grid[column][row]
        self.row = row
        self.column = column

    def update(self, event_queue: EventQueue):
        new_x = self.tile_sprite.rect.x
        new_y = self.tile_sprite.rect.y
        self.rect.x = new_x
        self.rect.y = new_y
