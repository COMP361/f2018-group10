import pygame


class GameBoardScene(object):
    """Scene for displaying the main game view"""
    def __init__(self, screen: pygame.display):
        """:param screen : The display passed from main on which to draw the Scene."""
        self.active_sprites = pygame.sprite.Group()     # Maybe add separate groups for different things later
        self.screen = screen

    def draw(self):
        self.active_sprites.draw(self.screen)
