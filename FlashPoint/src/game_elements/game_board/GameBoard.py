import pygame

import src.constants.Color as Color
import src.constants.MainConstants as MainConst
from src.game_elements.game_board.Grid import Grid


class GameBoard(pygame.sprite.Group):
    """Wrapper class for the Grid class. Contains methods specific for user interfacing."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((MainConst.SCREEN_RESOLUTION[0], MainConst.SCREEN_RESOLUTION[1]))
        self.rect = self.image.get_rect()
        self.grid = Grid(x_coord=self.rect.left, y_coord=self.rect.top)
        self.add(self.grid)

    def draw(self, screen: pygame.Surface):
        self.image.fill(Color.BLACK)
        self.grid.draw(self.image)
        screen.blit(self.image, self.rect)
