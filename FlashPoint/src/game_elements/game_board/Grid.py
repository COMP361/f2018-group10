from typing import List

import pygame

from src.game_elements.game_board.Tile import Tile


class Grid(pygame.sprite.Group):
    """Class to Group Tile objects together, and implement Grid logic in to what will form the GameBoard."""
    def __init__(self, *sprites: pygame.sprite.Sprite, screen: pygame.Surface=None, tile_size: int=64, tiles_x: int=12,
                 tiles_y: int=8):
        super().__init__(*sprites)
        self.height = tiles_y
        self.width = tiles_x
        self.screen = screen
        self.rect = pygame.Rect(screen.get_rect().left, screen.get_rect().top, tile_size*tiles_x, tile_size*tiles_y)
        self.grid = self._generate_grid()

    def _generate_grid(self, tile_size: int=64) -> List[List[Tile]]:
        """Initialize an 8x6 grid of Tiles, add to self Sprite Group."""
        grid = []
        x_coord = 0
        for i in range(0, self.width):
            grid.append([])
            y_coord = 0
            for j in range(0, self.height):
                grid[i].append(Tile(self.screen, self.rect.x + x_coord, self.rect.y + y_coord))
                grid[i][j].x_coordinate = i
                grid[i][j].y_coordinate = j
                self.add(grid[i][j])

                y_coord += tile_size

            x_coord += tile_size
        return grid
