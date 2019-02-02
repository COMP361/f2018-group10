import pygame

import src.constants.Color as Color
import src.constants.MainConstants as MainConst
from src.UIComponents.FileImporter import FileImporter
from src.game_elements.game_board.CharacterSprite import CharacterSprite
from src.game_elements.game_board.Grid import Grid
from src.core.EventQueue import EventQueue


class GameBoard(pygame.sprite.Group):
    """Wrapper class for the Grid class. Contains methods specific for user interfacing."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((MainConst.SCREEN_RESOLUTION[0], MainConst.SCREEN_RESOLUTION[1]))
        self.rect = self.image.get_rect()
        self.grid = Grid(x_coord=self.rect.left, y_coord=self.rect.top)
        self.add(self.grid)
        self.background = FileImporter.import_image("media/WoodBack.jpg")

    def draw(self, screen: pygame.Surface):
        #self.image.fill(Color.BLACK)
        self.image.blit(self.background, (0, 0))
        self.grid.draw(self.image)
        screen.blit(self.image, self.rect)

    def update(self, event_q: EventQueue):
        for event in event_q:
            if event.type == pygame.MOUSEBUTTONUP:
                for tile in self.grid:

                    if tile.hover():
                        tile.sprite_grp.add(CharacterSprite())

                    else:
                        some_sprite = tile.find_character()
                        tile.remove_sprite_character(some_sprite)

        self.grid.update(event_q)
