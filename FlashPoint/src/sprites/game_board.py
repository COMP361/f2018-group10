import pygame

import src.constants.main_constants as MainConst
from src.action_events.fire_placement_event import FirePlacementEvent
from src.UIComponents.file_importer import FileImporter
from src.models.game_units.player_model import PlayerModel
from src.sprites.grid_sprite import GridSprite
from src.core.event_queue import EventQueue


class GameBoard(pygame.sprite.Group):
    """Wrapper class for the Grid class. Contains methods specific for user interfacing."""

    def __init__(self, current_player: PlayerModel):
        super().__init__()
        self._fire_placement_event = FirePlacementEvent()
        self._fire_placement_event.execute()

        self.image = pygame.Surface((MainConst.SCREEN_RESOLUTION[0], MainConst.SCREEN_RESOLUTION[1]))
        self.rect = self.image.get_rect()
        self.grid = GridSprite(x_coord=self.rect.left, y_coord=self.rect.top, current_player=current_player)
        self.add(self.grid)
        self.background = FileImporter.import_image("media/backgrounds/WoodBack.jpeg")

    def draw(self, screen: pygame.Surface):
        self.image.blit(self.background, (0, 0))
        self.grid.draw(self.image)
        screen.blit(self.image, self.rect)

    def update(self, event_q: EventQueue):
        self.grid.update(event_q)
