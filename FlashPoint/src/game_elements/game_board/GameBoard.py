import pygame

from src.game_elements.game_board.Grid import Grid


class GameBoard(pygame.sprite.Group):

    def __init__(self, *sprites: pygame.sprite.Sprite):
        super().__init__(*sprites)
        self._grid = Grid()
