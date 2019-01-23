import pygame

import src.constants.Color as Color
import src.constants.MainConstants as MainConst
from src.sprites.GridSprite import GridSprite
from src.sprites.CharacterSprite import CharacterSprite
from src.core.EventQueue import EventQueue


class GameBoard(pygame.sprite.Group):
    """Wrapper class for the Grid class. Contains methods specific for user interfacing."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((MainConst.SCREEN_RESOLUTION[0], MainConst.SCREEN_RESOLUTION[1]))
        self.rect = self.image.get_rect()
        self.grid = GridSprite(x_coord=self.rect.left, y_coord=self.rect.top)
        self.add(self.grid)

    def draw(self, screen: pygame.Surface):

        self.image.fill(Color.BLACK)
        self.grid.draw(self.image)
        screen.blit(self.image, self.rect)

    def update(self, event_q: EventQueue):
        for event in event_q:
            if event.type == pygame.MOUSEBUTTONUP:
                for tile_sprite in self.grid:

                    if tile_sprite.hover():
                        tile_sprite.tile_model.game_unit_sprites.add(CharacterSprite())

                   # else:
                        # some_sprite = tile_sprite.tile_model.find_character()
                        # tile_sprite.tile_model.remove_sprite_character(some_sprite)

        self.grid.update(event_q)
