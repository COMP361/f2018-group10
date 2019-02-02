from typing import List

import pygame

from src.game_elements.game_board.Tile import Tile


class Grid(pygame.sprite.Group):

    """Class to Group Tile objects together, and implement Grid logic in to what will form the GameBoard."""
    def __init__(self, *sprites: pygame.sprite.Sprite,
                 x_coord: int, y_coord: int,
                 tile_size: int=128, tiles_x: int=12, tiles_y: int=8):
        super().__init__(*sprites)
        self.contains_player = False
        self.height = tiles_y
        self.width = tiles_x
        self.image = pygame.Surface((tile_size*tiles_x, tile_size*tiles_y))
        self.rect = self.image.get_rect().move((x_coord, y_coord))
        self.grid = self._generate_grid(tile_size)

    def _generate_grid(self, tile_size) -> List[List[Tile]]:
        """Initialize an grid of Tiles, add to self Sprite Group."""
        grid = []
        x_coord = 0
        for i in range(0, self.width):
            grid.append([])
            y_coord = 0
            for j in range(0, self.height):
                grid[i].append(Tile(self.rect.x, self.rect.y, x_coord, y_coord))
                grid[i][j].x_coordinate = i
                grid[i][j].y_coordinate = j
                self.add(grid[i][j])

                y_coord += tile_size
            x_coord += tile_size
        return grid

    def draw(self, screen: pygame.Surface):
        for tile in self:
            tile.draw(screen)
