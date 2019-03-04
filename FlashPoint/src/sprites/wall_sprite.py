import pygame

from src.UIComponents.rect_button import RectButton
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel


class Wall(pygame.sprite):

    def __init__(self, x_pos: int, y_pos: int):
        self._game: GameStateModel = GameStateModel.instance()
        self.tile = self._game.game_board.get_tile_at(x_pos, y_pos)
        self.east_obstacle = self.tile.get_obstacle_in_direction("East")

        if self.east_obstacle:

            if isinstance(self.east_obstacle, WallModel):
                self.create_wall(x_pos + 128 - 7, y_pos, 14, 125)

        if self.east_obstacle:

            if isinstance(self.east_obstacle, WallModel):
                self.create_wall(x_pos, y_pos + 128 - 7, 125, 14)

    def create_wall(self, x, y, width, height):
        box_size = (width, height)
        self.this_img = RectButton(x, y, box_size[0], box_size[1])

        self.sprite_grp.add(self.this_img)
