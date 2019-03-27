import pygame

from src.models.game_board.tile_model import TileModel
from src.sprites.game_board import GameBoard
from src.sprites.grid_sprite import GridSprite

from src.UIComponents.file_importer import FileImporter


class HazmatSprite(pygame.sprite.Sprite):

    def __init__(self, tile_model: TileModel):
        super().__init__()
        self.grid: GridSprite = GameBoard.instance().grid
        self.tile_model = tile_model
        self.tile_sprite = self.grid.grid[tile_model.column][tile_model.row]
        self.rect = self.tile_sprite.rect
        self.image = FileImporter.import_image("media/all_markers/hazmat.png")
