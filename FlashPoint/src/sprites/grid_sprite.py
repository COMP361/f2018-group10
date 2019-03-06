from typing import List

import pygame

import src.constants.color as Color
from src.UIComponents.interactable import Interactable
from src.UIComponents.rect_button import RectButton
from src.core.event_queue import EventQueue
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel

from src.UIComponents.spritesheet import Spritesheet
from src.models.game_units.player_model import PlayerModel
from src.sprites.tile_sprite import TileSprite
from src.sprites.wall_sprite import WallSprite


class GridSprite(pygame.sprite.Group):
    """Class to Group Tile objects together, and implement Grid logic in to what will form the GameBoard."""
    def __init__(self, *sprites: pygame.sprite.Sprite,
                 x_coord: int, y_coord: int,
                 tile_size: int=128, tiles_x: int=10, tiles_y: int=8, current_player: PlayerModel):
        super().__init__(*sprites)
        self.current_player = current_player
        self._fire_image = Spritesheet("media/All Markers/fire.png", 1, 1).cell_images[0][0]
        self._smoke_image = Spritesheet("media/All Markers/smoke.png", 1, 1).cell_images[0][0]

        self.contains_player = False
        self.height = tiles_y
        self.width = tiles_x
        self.image = pygame.Surface((tile_size*tiles_x, tile_size*tiles_y)).convert_alpha()
        self.rect = self.image.get_rect().move((x_coord, y_coord))
        self.walls = []
        self.wall_buttons = []
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
                tile_sprite = TileSprite(image, self._fire_image, self._smoke_image, self.rect.x, self.rect.y, x_offset, y_offset, j, i)
                grid[i].append(tile_sprite)

                tile_model = GameStateModel.instance().game_board.get_tile_at(int(y_offset / 128), int(x_offset / 128))
                self.east_obstacle = tile_model.get_obstacle_in_direction("East")
                self.south_obstacle = tile_model.get_obstacle_in_direction("South")

                if self.east_obstacle:
                    if isinstance(self.east_obstacle, WallModel):
                        wall = WallSprite(tile_sprite, tile_model, self.current_player, (j, i, "East"))
                        wall.button = RectButton(x_offset + 128 -7, y_offset, 14, 125, Color.BLACK)
                        wall.button.on_click(wall.process_input)
                        self.wall_buttons.append(wall.button_input)
                        self.walls.append(wall)
                        tile_model.add_observer(wall)

                if self.south_obstacle:
                    if isinstance(self.south_obstacle, WallModel):
                        wall = WallSprite(tile_sprite, tile_model, self.current_player, (j, i, "South"))
                        wall.button = RectButton(x_offset, y_offset + 128 - 7, 125, 14, Color.BLACK)
                        wall.button.on_click(wall.process_input)
                        self.wall_buttons.append(wall.button_input)
                        self.walls.append(wall)
                        tile_model.add_observer(wall)

                self.add(grid[i][j])

                y_offset += tile_size
            x_offset += tile_size
        return grid

    def draw(self, screen: pygame.Surface):
        for sprite in self:
            if isinstance(sprite, RectButton) and not sprite.enabled:
                pass
            else:
                sprite.draw(screen)

        for wall in self.walls:
            wall.draw(screen)

        for wall_btn in self.wall_buttons:
            if wall_btn.enabled:
                wall_btn.draw(screen)

    def update(self, event_queue: EventQueue):
        for tile in self:
            tile.update(event_queue)

        for wall in self.walls:
            wall.update(event_queue)
