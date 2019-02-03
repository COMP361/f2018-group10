import pygame


class CharacterSprite(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
       # self.image = FileImporter.import_image("media/character.png")
        self.image = pygame.Surface((128, 128))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
