from typing import List

import pygame

from src.game_elements.game_board.Tile import Tile


class Grid(pygame.sprite.Group):
    """Class to Group Tile objects together, and implement Grid logic in to what will form the GameBoard."""
    def __init__(self, *sprites: pygame.sprite.Sprite, height: int=6, width: int=8):
        super().__init__(*sprites)
        self.height = height
        self.width = width
        self.grid = self._generate_grid()

    def draw(self, surface: pygame.Surface):
        """Draw all Tiles in the grid."""
        for row in self.grid:
            for tile in row:
                surface.blit(tile, tile.rect)

    def _generate_grid(self) -> List[List[Tile]]:
        """Initialize an 8x6 grid of Tiles, add to self Sprite Group."""
        grid = [[]]
        for i in range(0, self.height):
            for j in range(0, self.width):
                grid[i][j] = Tile()
                self.add(grid[i][j])

        return grid


