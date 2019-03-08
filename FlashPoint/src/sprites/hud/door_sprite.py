from typing import Tuple

import pygame
import src.constants.color as Color
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.action_events.turn_events.chop_event import ChopEvent
from src.action_events.turn_events.close_door_event import CloseDoorEvent
from src.action_events.turn_events.open_door_event import OpenDoorEvent
from src.constants.state_enums import WallStatusEnum, DoorStatusEnum
from src.models.game_board.door_model import DoorModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.observers.door_observer import DoorObserver
from src.sprites.tile_sprite import TileSprite
from src.UIComponents.text import Text
from src.action_events.turn_events.turn_event import TurnEvent


class DoorSprite(pygame.sprite.Sprite, DoorObserver):

    def __init__(self, door_model: DoorModel, orientation: str, tile_sprite: TileSprite, tile_model: TileModel, id: Tuple[int, int, str]):
        super().__init__()
        self.orientation = orientation
        self._game: GameStateModel = GameStateModel.instance()
        self._current_player = self._game.players_turn
        self._button = None
        self.tile_model = tile_model
        self.open = False
        self.closed = False
        self.destroyed = False
        self.id = id
        self.door_model = door_model
        self.door_model.add_observer(self)

        if self.door_model.door_status == DoorStatusEnum.OPEN:
            self.door_model.open_door()
        else:
            self.door_model.close_door()
        self.marker  = None
        self.tile_sprite = tile_sprite
        self._prev_x = self.tile_sprite.rect.x
        self._prev_y = self.tile_sprite.rect.y
        self.button_input = RectButton(self.tile_sprite.rect.x+100, self.tile_sprite.rect.y+100, 100, 25, Color.BLACK, 0, Text(pygame.font.SysFont('Arial', 20), "Interact", Color.ORANGE))
        self.button_input.disable()

        #self.button_input.on_click(self.wall_chop)


    @property
    def player(self) -> PlayerModel:
        return self._current_player

    @property
    def button(self):
        return self._button

    @button.setter
    def button(self, button):
        self._button = button

    # def wall_chop(self):
    #     self.button_input.disable()
    #     print("Francisdadasdad")

    def process_input(self):
        # if self.check():
        self.button_input.enable()

    def check(self) -> bool:
        valid_to_open_close = TurnEvent.has_required_AP(self.player.ap, 2)
        if not valid_to_open_close:
            return False

        player_tile = self._game.game_board.get_tile_at(self.player.y_pos, self.player.x_pos)

        if self.door_model not in player_tile.adjacent_edge_objects.values():
            return False

        door_status = self.door_model.door_status
        if door_status == DoorStatusEnum.DESTROYED:
            return False

        return True

    def instantiate_event(self):
        if self.door_model.door_status == DoorStatusEnum.OPEN:
            CloseDoorEvent(self.door_model, self.player).execute()
        elif self.door_model.door_status == DoorStatusEnum.CLOSED:
            OpenDoorEvent(self.door_model, self.player).execute()

    def update(self, event_queue):
        if self.button_input.enabled:
            self.button_input.on_click(self.instantiate_event)

        diff_x = self.tile_sprite.rect.x - self._prev_x
        diff_y = self.tile_sprite.rect.y - self._prev_y
        self._button.rect.move_ip((diff_x, diff_y))
        self._prev_x = self.tile_sprite.rect.x
        self._prev_y = self.tile_sprite.rect.y
        self.button_input.rect.x = self.tile_sprite.rect.x + 14
        self.button_input.rect.y = self.tile_sprite.rect.y + 50

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

        if self.orientation == "vertical":
            x_offset1 = -22
            y_offset1 = 40

        if self.orientation == "horizontal":
            x_offset1 = 34
            y_offset1 = -18

        if self.destroyed:
            self.marker = RectLabel(self.button.rect.x+x_offset1 , self.button.rect.y+y_offset1, 50, 50,
                               "media/Threat_Markers/damageMarker.png")
            self.marker.draw(screen)
        if self.open:
            self.marker = RectLabel(self.button.rect.x+x_offset1, self.button.rect.y+y_offset1, 50, 50,
                               "media/Door_Markers/Open_Door.png")
            self.marker.draw(screen)
        if self.closed:
            self.marker = RectLabel(self.button.rect.x+x_offset1, self.button.rect.y+y_offset1, 50, 50,
                               "media/Door_Markers/Closed_Door.png")
            self.marker.draw(screen)
