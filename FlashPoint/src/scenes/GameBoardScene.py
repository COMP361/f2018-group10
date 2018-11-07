import pygame

from src.game_elements.game_board.GameBoard import GameBoard


class GameBoardScene(object):
    """Scene for displaying the main game view"""
    def __init__(self, screen: pygame.display):
        """:param screen : The display passed from main on which to draw the Scene."""
        self.active_sprites = pygame.sprite.Group()   # Maybe add separate groups for different things later
        self.screen = screen
        self._render()

    def _render(self):
        """Initialize all sprites to this board."""
        self.active_sprites.add(GameBoard(screen=self.screen))

    def draw(self):
        self.active_sprites.draw(self.screen)

    def update(self):
        self.active_sprites.update()
