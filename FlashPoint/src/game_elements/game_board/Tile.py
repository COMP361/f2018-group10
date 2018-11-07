import pygame


class Tile(pygame.sprite.Sprite):

    def __init__(self, screen: pygame.Surface, size: int=64):
        """Create a tile, not sure what the sprite size should be..."""
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface([size, size])
        self.rect = self.image.get_rect()
        self.rect.move_ip(600, 100)
        self.is_hovered = False
        self.x_coordinate = 0
        self.y_coordinate = 0
        self._initialize()

    def _initialize(self):
        """Eventually this might have some randomization logic? Dunno how we'll generate boards :( """
        self.image.fill((100, 100, 100), self.rect)  # eventually this will be an actual tile image.

    def check_mouse_over(self):
        mouse = pygame.mouse.get_pos()
        rect = self.rect
        return rect.x+rect.w > mouse[0] > rect.x and rect.y+rect.h > mouse[1] > rect.y

    def update(self):
        if self.check_mouse_over():
            if not self.is_hovered:
                self.is_hovered = True
                self.image.fill((255, 255, 0))
        else:
            self.image.fill((100, 100, 100))
            self.is_hovered = False
