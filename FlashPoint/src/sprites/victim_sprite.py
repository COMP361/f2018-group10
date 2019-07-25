import pygame
from src.sprites.game_board import GameBoard
from src.constants.state_enums import VictimStateEnum
from src.core.event_queue import EventQueue
from src.observers.victim_observer import VictimObserver
from src.UIComponents.file_importer import FileImporter
import logging

logger = logging.getLogger("FlashPoint")


class VictimSprite(pygame.sprite.Sprite, VictimObserver):

    """Visual representation of a Victim."""

    def __init__(self, row: int, column: int):
        super().__init__()
        self.image = FileImporter.import_image("src/media/all_markers/victim.png")

        self.rect = self.image.get_rect()
        self.row = row
        self.column = column
        self.tile_sprite = GameBoard.instance().grid.grid[column][row]

    def victim_state_changed(self, state: VictimStateEnum):
        if state == VictimStateEnum.LOST:
            self.kill()
        elif state == VictimStateEnum.RESCUED:
            self.kill()
        elif state == VictimStateEnum.TREATED:
            treat = FileImporter.import_image("src/media/all_markers/treated.png")
            self.image.blit(treat, (0,0))

    def victim_position_changed(self, row: int, column: int):
        self.tile_sprite = GameBoard.instance().grid.grid[column][row]
        self.row = row
        self.column = column

    def update(self, event_queue: EventQueue):
        new_x = self.tile_sprite.rect.x
        new_y = self.tile_sprite.rect.y
        self.rect.x = new_x
        self.rect.y = new_y
