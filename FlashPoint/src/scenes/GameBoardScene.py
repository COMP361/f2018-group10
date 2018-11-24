import pygame

from src.game_elements.game_board.GameBoard import GameBoard


class GameBoardScene(object):
    """Scene for displaying the main game view"""
    def __init__(self, screen: pygame.display):
        """:param screen : The display passed from main on which to draw the Scene."""
        self.screen = screen
        self.active_sprites = pygame.sprite.Group()   # Maybe add separate groups for different things later
        self.game_board = GameBoard()
        self.active_sprites.add(self.game_board.grid)

    def draw(self):
        """Draw all currently active sprites."""
        self.game_board.draw(self.screen)
        self.active_sprites.draw(self.game_board.image)

    def update(self):
        """Call the update() function of everything in this class."""
        self.active_sprites.update()
        self.game_board.update()
