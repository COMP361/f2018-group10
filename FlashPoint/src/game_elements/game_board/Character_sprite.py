import pygame
from src.Windows.UIComponents.FileImporter import FileImporter


class CharacterSprite(pygame.sprite.Sprite):

    def __init__(self):
        self.character_place = FileImporter.import_image("media/character.png")
        pygame.sprite.Sprite.__init__(self)
