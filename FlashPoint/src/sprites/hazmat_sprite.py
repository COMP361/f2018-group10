from typing import List

import pygame

from src.core.event_queue import EventQueue
from src.models.game_board.tile_model import TileModel
from src.observers.hazmat_observer import HazmatObserver
from src.sprites.game_board import GameBoard
from src.sprites.grid_sprite import GridSprite
from src.UIComponents.file_importer import FileImporter
import logging
logger = logging.getLogger("FlashPoint")


class HazmatSprite(HazmatObserver, pygame.sprite.Sprite):

    def __init__(self, tile_model: TileModel):
        super().__init__()
        self.grid: GridSprite = GameBoard.instance().grid
        self.tile_sprite = self.grid.grid[tile_model.column][tile_model.row]
        self.rect = self.tile_sprite.rect
        self.image = FileImporter.import_image("media/all_markers/hazmat.png")

    def hazmat_position_changed(self, row: int, col: int):
        logger.info(f"Hazmat moved: {row}, {col}")
        self.tile_sprite = GameBoard.instance().grid.grid[col][row]
        self.rect = self.tile_sprite.rect

    def update(self, event_queue: EventQueue):
        new_x = self.tile_sprite.rect.x
        new_y = self.tile_sprite.rect.y
        self.rect.x = new_x
        self.rect.y = new_y
