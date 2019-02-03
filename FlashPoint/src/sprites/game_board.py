import pygame


import src.constants.color as Color
import src.constants.main_constants as MainConst
from src.UIComponents.file_importer import FileImporter
from src.sprites.grid_sprite import GridSprite
from src.sprites.player_sprite import PlayerSprite
from src.core.event_queue import EventQueue


class GameBoard(pygame.sprite.Group):
    """Wrapper class for the Grid class. Contains methods specific for user interfacing."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((MainConst.SCREEN_RESOLUTION[0], MainConst.SCREEN_RESOLUTION[1]))
        self.rect = self.image.get_rect()
        self.grid = GridSprite(x_coord=self.rect.left, y_coord=self.rect.top)
        self.add(self.grid)
        self.background = FileImporter.import_image("media/WoodBack.jpg")

    def draw(self, screen: pygame.Surface):

        self.image.blit(self.background, (0, 0))
        self.grid.draw(self.image)
        screen.blit(self.image, self.rect)

    def update(self, event_q: EventQueue):
        # for event in event_q:
        #     if event.type == pygame.MOUSEBUTTONUP:
        #         for tile_sprite in self.grid:
        #
        #             if tile_sprite.hover():
        #                 tile_sprite.tile_model.game_unit_sprites.add(CharacterSprite())

                   # else:
                        # some_sprite = tile_sprite.tile_model.find_character()
                        # tile_sprite.tile_model.remove_sprite_character(some_sprite)

        self.grid.update(event_q)
