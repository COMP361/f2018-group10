import pygame

import src.constants.MainConstants as MainConst
from src.game_elements.game_board.Grid import Grid


class GameBoard(pygame.sprite.Group):
    """Wrapper class for the Grid class. Contains methods specific for user interfacing."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((MainConst.SCREEN_RESOLUTION[0]*2/3, MainConst.SCREEN_RESOLUTION[1]*0.8))
        self.rect = self.image.get_rect().move((500, 100))

        self.is_scrolling = -1                              # Need 2 clicks to become 1 (True)
        self.mouse_pos = (0, 0)                             # Store the mouse pos to determine direction
        self._init_sprites()

    def _init_sprites(self):
        self.add(Grid(x_coord=self.rect.left, y_coord=self.rect.top, screen=self.image))
