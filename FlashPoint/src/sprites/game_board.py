import itertools

import pygame

import src.constants.main_constants as MainConst
from src.sprites.player_sprite import PlayerSprite
from src.UIComponents.rect_button import RectButton
from src.UIComponents.file_importer import FileImporter
from src.models.game_units.player_model import PlayerModel
from src.sprites.grid_sprite import GridSprite
from src.core.event_queue import EventQueue


class GameBoard(pygame.sprite.Group):
    """Wrapper class for the Grid class. Contains methods specific for user interfacing."""

    _instance = None

    def __init__(self, current_player: PlayerModel):
        if GameBoard._instance:
            raise Exception("GameBoard is a singleton")
        super().__init__()
        self.image = pygame.Surface((MainConst.SCREEN_RESOLUTION[0], MainConst.SCREEN_RESOLUTION[1]))
        self.rect = self.image.get_rect()
        self.grid = GridSprite(x_coord=self.rect.left, y_coord=self.rect.top, current_player=current_player)
        self.background = FileImporter.import_image("src/media/backgrounds/WoodBack.jpeg")
        self.top_ui = pygame.sprite.Group()
        GameBoard._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def draw(self, screen: pygame.Surface):
        self.image.blit(self.background, (0, 0))
        self.grid.draw(self.image)
        for sprite in self:
            if isinstance(sprite, PlayerSprite):
                pass
            self.image.blit(sprite.image, sprite.rect)

        # Blit the player sprite last, so that it's on top
        for sprite in self:
            if isinstance(sprite, PlayerSprite):
                self.image.blit(sprite.image, sprite.rect)

        for sprite in itertools.chain(self.grid, self.grid.walls):
            if isinstance(sprite, RectButton) and not sprite.enabled:
                pass
            else:
                sprite.draw_menu(self.image)

        for sprite in self.top_ui.sprites():
            self.image.blit(sprite.image, sprite.rect)

        screen.blit(self.image, self.rect)

    def update(self, event_q: EventQueue):
        self.grid.update(event_q)
        for sprite in self:
            sprite.update(event_q)

        for sprite in self.top_ui:
            sprite.update(event_q)
