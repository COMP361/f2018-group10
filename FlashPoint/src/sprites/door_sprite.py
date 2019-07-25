from typing import Tuple

import pygame
import src.constants.color as Color
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.constants.state_enums import DoorStatusEnum
from src.models.game_board.door_model import DoorModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.observers.door_observer import DoorObserver
from src.sprites.tile_sprite import TileSprite
from src.UIComponents.text import Text


class DoorSprite(pygame.sprite.Sprite, DoorObserver):

    def __init__(self, door_model: DoorModel, orientation: str, tile_sprite: TileSprite, tile_model: TileModel,
                 id: Tuple[int, int, str]):
        super().__init__()
        self.orientation = orientation
        self._game: GameStateModel = GameStateModel.instance()
        self._current_player = self._game.players_turn
        self._button = None
        self.tile_model = tile_model
        self.id = id
        self.door_model = door_model
        self.door_model.add_observer(self)

        self.open = self.door_model.door_status == DoorStatusEnum.OPEN
        self.closed = self.door_model.door_status == DoorStatusEnum.CLOSED
        self.destroyed = self.door_model.door_status == DoorStatusEnum.DESTROYED

        self.marker = None
        self.tile_sprite = tile_sprite
        self._prev_x = self.tile_sprite.rect.x
        self._prev_y = self.tile_sprite.rect.y
        self.button_input = RectButton(self.tile_sprite.rect.x + 100, self.tile_sprite.rect.y + 100, 100, 25,
                                       Color.WOOD, 0, Text(pygame.font.SysFont('Agency FB', 15), "Interact", Color.GREEN2))
        pygame.draw.rect(self.button_input.image,Color.YELLOW,[0,0,100,25],3)
        self.button_input.disable()
        self.menu_shown = False

    @property
    def direction(self) -> str:
        return self.id[2]

    @property
    def player(self) -> PlayerModel:
        return self._current_player

    @property
    def button(self):
        return self._button

    @button.setter
    def button(self, button):
        self._button = button

    def update(self, event_queue):
        diff_x = self.tile_sprite.rect.x - self._prev_x
        diff_y = self.tile_sprite.rect.y - self._prev_y
        self._button.rect.move_ip((diff_x, diff_y))
        self._prev_x = self.tile_sprite.rect.x
        self._prev_y = self.tile_sprite.rect.y
        self.button_input.rect.x = self.tile_sprite.rect.x + 100
        self.button_input.rect.y = self.tile_sprite.rect.y + 100

        for event in event_queue:
            if event.type == pygame.MOUSEBUTTONUP:
                if not ((self.button_input.rect.x <= pygame.mouse.get_pos()[0] <= self.button_input.rect.x + 100) and (
                        self.button_input.rect.y <= pygame.mouse.get_pos()[1] <= self.button_input.rect.y + 25)):
                    self.button_input.disable()

        self._button.update(event_queue)
        self.button_input.update(event_queue)

    def door_status_changed(self, status: DoorStatusEnum):
        if status == DoorStatusEnum.DESTROYED:
            self.destroyed = True
            self.open = False
            self.closed = False
        elif status == DoorStatusEnum.CLOSED:
            self.closed = True
            self.open = False
            self.destroyed = False
        elif status == DoorStatusEnum.OPEN:
            self.open = True
            self.closed = False
            self.destroyed = False
        else:
            raise Exception("Door status ERROR")

    def draw(self, screen):
        self.button.draw(screen)
        x_offset1 = 0
        y_offset1 = 0

        if self.menu_shown:
            if self.button_input.enabled:
                screen.blit(self.button_input.image, self.button_input.rect)

        if self.orientation == "vertical":
            x_offset1 = -22
            y_offset1 = 40

        if self.orientation == "horizontal":
            x_offset1 = 34
            y_offset1 = -18

        if self.destroyed:
            self.marker = RectLabel(self.button.rect.x + x_offset1, self.button.rect.y + y_offset1, 50, 50,
                                    "src/media/Threat_Markers/damageMarker.png")
            self.marker.draw(screen)
        if self.open:
            self.marker = RectLabel(self.button.rect.x + x_offset1, self.button.rect.y + y_offset1, 50, 50,
                                    "src/media/Door_Markers/Open_Door.png")
            self.marker.draw(screen)
        if self.closed:
            self.marker = RectLabel(self.button.rect.x + x_offset1, self.button.rect.y + y_offset1, 50, 50,
                                    "src/media/Door_Markers/Closed_Door.png")
            self.marker.draw(screen)
