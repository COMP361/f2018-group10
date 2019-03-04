from typing import List

import pygame
from src.models.game_state_model import GameStateModel

from src.UIComponents.spritesheet import Spritesheet
from src.sprites.tile_sprite import TileSprite


class GridSprite(pygame.sprite.Group):
    """Class to Group Tile objects together, and implement Grid logic in to what will form the GameBoard."""
    def __init__(self, *sprites: pygame.sprite.Sprite,
                 x_coord: int, y_coord: int,
                 tile_size: int=128, tiles_x: int=10, tiles_y: int=8):
        super().__init__(*sprites)

        self._fire_image = Spritesheet("media/All Markers/fire.png", 1, 1).cell_images[0][0]
        self._smoke_image = Spritesheet("media/All Markers/smoke.png", 1, 1).cell_images[0][0]

        self.contains_player = False
        self.height = tiles_y
        self.width = tiles_x
        self.image = pygame.Surface((tile_size*tiles_x, tile_size*tiles_y)).convert_alpha()
        self.rect = self.image.get_rect().move((x_coord, y_coord))
        self.grid = self._generate_grid(tile_size)

    def _generate_grid(self, tile_size: int) -> List[List[TileSprite]]:
        """Initialize a grid of Tiles, add to self Sprite Group."""
        grid = []
        x_offset = 0
        tile_images = Spritesheet("media/boards/board1.png", 10, 8).cell_images

        for i in range(0, self.width):
            grid.append([])
            y_offset = 0
            for j in range(0, self.height):
                image = tile_images[j][i]
                tile = TileSprite(image, self._fire_image.copy(), self._smoke_image.copy(), self.rect.x, self.rect.y, x_offset, y_offset, j, i)
                grid[i].append(tile)
                self.add(grid[i][j])
                GameStateModel.instance().game_board.get_tile_at(j, i).add_observer(tile)

                y_offset += tile_size
            x_offset += tile_size
        return grid

    def draw(self, screen: pygame.Surface):
        for tile in self:
            tile.draw(screen)
