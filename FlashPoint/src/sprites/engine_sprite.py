from typing import List

import pygame

from src.core.event_queue import EventQueue
from src.models.game_units.player_model import PlayerModel
from src.sprites.game_board import GameBoard
from src.UIComponents.file_importer import FileImporter
from src.constants.state_enums import VehicleOrientationEnum
from src.sprites.tile_sprite import TileSprite
from src.observers.vehicle_observer import VehicleObserver


class EngineSprite(pygame.sprite.Sprite, VehicleObserver):

    def notify_passengers(self, passengers: List[PlayerModel]):
        pass

    def __init__(self, orientation: VehicleOrientationEnum, tile_sprite: TileSprite):
        super().__init__()
        self.image = FileImporter.import_image("src/media/Vehicles/Fire_Engine.png")
        self.rect = self.image.get_rect()
        self.tile_sprite = tile_sprite
        self.row = tile_sprite.row
        self.column = tile_sprite.column
        self.orientation = orientation

        if self.orientation == VehicleOrientationEnum.VERTICAL:
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect()

    def notify_vehicle_pos(self, orientation: VehicleOrientationEnum, row: int, column: int):
        self.tile_sprite = GameBoard.instance().grid.grid[column][row]
        self.row = row
        self.column = column

        # Fix the orientation if needed
        if self.orientation == VehicleOrientationEnum.VERTICAL and orientation == VehicleOrientationEnum.HORIZONTAL:
            self.image = pygame.transform.rotate(self.image, -90)
        elif self.orientation == VehicleOrientationEnum.HORIZONTAL and orientation == VehicleOrientationEnum.VERTICAL:
            self.image = pygame.transform.rotate(self.image, 90)

        self.orientation = orientation

    def update(self, event_queue: EventQueue):
        new_x = self.tile_sprite.rect.x
        new_y = self.tile_sprite.rect.y
        self.rect.x = new_x
        self.rect.y = new_y
