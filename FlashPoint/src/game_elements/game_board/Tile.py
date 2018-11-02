import pygame


class Tile(pygame.sprite.Sprite):

    def __init__(self):
        """Create a tile, not sure what the sprite size should be..."""
        super().__init__()
        self.image = pygame.Surface(64, 64)
        self.rect = self.image.get_rect()

