import pygame
from src.Windows.UIComponents.FileImporter import FileImporter


class character_sprite(pygame.sprite.Sprite):

    def __init__(self):
        self.character_place = FileImporter.import_image("media/position.png")
