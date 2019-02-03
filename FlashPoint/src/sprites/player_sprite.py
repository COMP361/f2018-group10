import pygame

from src.models.game_board.tile_model import TileModel
from src.models.game_units.player_model import PlayerModel


class PlayerSprite(pygame.sprite.Sprite):

    def __init__(self, tile: TileModel, player: PlayerModel):
        super().__init__()

        self.player_model = player
        # self.image = FileImporter.import_image("media/character.png")
        self.tile_reference = tile
        self.image = pygame.Surface((128, 128))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
