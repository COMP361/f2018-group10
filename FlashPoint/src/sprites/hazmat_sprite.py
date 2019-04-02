from typing import List

import pygame

from src.constants.state_enums import SpaceStatusEnum
from src.models.model import Model
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_board.tile_model import TileModel
from src.sprites.game_board import GameBoard
from src.sprites.grid_sprite import GridSprite
from src.observers.tile_observer import TileObserver
from src.UIComponents.file_importer import FileImporter


class HazmatSprite(TileObserver, pygame.sprite.Sprite):

    def __init__(self, tile_model: TileModel):
        super().__init__()
        self.grid: GridSprite = GameBoard.instance().grid
        self.tile_model = tile_model
        self.tile_sprite = self.grid.grid[tile_model.column][tile_model.row]
        self.tile_model.add_observer(self)
        self.rect = self.tile_sprite.rect
        self.image = FileImporter.import_image("media/all_markers/hazmat.png")

    def tile_assoc_models_changed(self, assoc_models: List[Model]):
        for model in assoc_models:
            if isinstance(model, HazmatModel):
                return
        # If HazmatModel no longer exists in the associated models, remove it
        self.kill()

    def tile_status_changed(self, status: SpaceStatusEnum, is_hotspot: bool):
        pass
