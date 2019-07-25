
import pygame
from src.models.game_units.victim_model import VictimModel
from src.sprites.victim_sprite import VictimSprite
from src.models.game_units.poi_model import POIModel
from src.sprites.game_board import GameBoard
from src.core.event_queue import EventQueue

from src.UIComponents.file_importer import FileImporter
from src.constants.state_enums import POIStatusEnum, POIIdentityEnum
from src.observers.poi_observer import POIObserver


class POISprite(pygame.sprite.Sprite, POIObserver):
    """Visual representation of a POI."""

    def __init__(self, poi: POIModel):
        super().__init__()
        self.image = FileImporter.import_image('src/media/all_markers/poi128.png')
        self.small_image = FileImporter.import_image("src/media/all_markers/poi.png")
        self.rect = self.image.get_rect()
        self.poi_model = poi
        self.row = poi.row
        self.column = poi.column
        self.poi_model.add_observer(self)
        self.tile_sprite = GameBoard.instance().grid.grid[poi.column][poi.row]

        self.counter = 80

    def poi_status_changed(self, status: POIStatusEnum, victim: VictimModel):
        if status == POIStatusEnum.REVEALED and victim:
            if self.poi_model.identity == POIIdentityEnum.VICTIM:
                # Replace this sprite with a victim sprite.
                victim_sprite = VictimSprite(victim.row, victim.column)
                victim.add_observer(victim_sprite)
                for group in self.groups():
                    group.add(victim_sprite)
        self.kill()

    def poi_position_changed(self, row: int, column: int):
        self.tile_sprite = GameBoard.instance().grid.grid[column][row]
        self.row = row
        self.column = column

    def update(self, event_queue: EventQueue):
        new_x = self.tile_sprite.rect.x
        new_y = self.tile_sprite.rect.y
        self.rect.x = new_x
        self.rect.y = new_y
        self.counter -= 1
        if self.counter <= 0:
            self.image = self.small_image
