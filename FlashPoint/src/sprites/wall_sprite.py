from typing import Tuple

import pygame
import src.constants.color as Color
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.action_events.turn_events.chop_event import ChopEvent
from src.constants.state_enums import WallStatusEnum
from src.core.event_queue import EventQueue
from src.core.flashpoint_exceptions import NotEnoughAPException, ModelNotAdjacentException, \
    WallAlreadyDestroyedException
from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.observers.wall_observer import WallObserver
from src.sprites.tile_sprite import TileSprite
from src.UIComponents.text import Text
from src.action_events.turn_events.turn_event import TurnEvent

class WallSprite(pygame.sprite.Sprite, WallObserver):

    def __init__(self, tile_sprite: TileSprite, tile_model: TileModel, current_player: PlayerModel,
                 id: Tuple[int, int, str]):
        super().__init__()

        self._game: GameStateModel = GameStateModel.instance()
        self._current_player = self._game.players_turn
        self._button = None
        self.tile_model = tile_model
        self.damaged = False
        self.destroyed = False
        self.id = id
        self.wall_model = None
        self.chop_direction = ""
        for direction, wall in self.tile_model.adjacent_edge_objects.items():
            if isinstance(wall, WallModel):
                if wall.id == self.id:
                    wall.add_observer(self)
                    self.wall_model = wall
                    self.chop_direction = direction
                    break

        self.tile_sprite = tile_sprite
        self._prev_x = self.tile_sprite.rect.x
        self._prev_y = self.tile_sprite.rect.y
        self.button_input = RectButton(self.tile_sprite.rect.x + 50, self.tile_sprite.rect.y + 50, 200, 25, Color.BLACK,
                                       0, Text(pygame.font.SysFont('Arial', 20), "CHoP tHaT MF wAlL", Color.ORANGE))
        self.button_input.disable()



    @property
    def player(self) -> PlayerModel:
        return self._current_player

    @property
    def button(self):
        return self._button

    @button.setter
    def button(self, button):
        self._button = button

    def process_input(self):
        if self.check():
            self.button_input.enable()

    def check(self) -> bool:

        valid_to_chop = TurnEvent.has_required_AP(self.player.ap, 2)
        if not valid_to_chop:
            # raise NotEnoughAPException("chop the wall", 2)
            return False

        player_tile = self._game.game_board.get_tile_at(self.player.x_pos, self.player.y_pos)

        if self.wall_model not in player_tile.adjacent_edge_objects.values():
            # raise ModelNotAdjacentException("wall", self.player.x_pos, self.player.y_pos)
            return False

        wall_status = self.wall_model.wall_status
        if wall_status == WallStatusEnum.DESTROYED:
            # raise WallAlreadyDestroyedException()
            return False

        return True

    def instantiate_event(self):
        ChopEvent(self.player, self.wall_model, self.chop_direction)

    def update(self, event_queue):
        if self.button_input.enabled:
            self.button_input.on_click()
        if self.destroyed is False and self.damaged is True:
            self.button_input.on_click(self.wall_status_changed, WallStatusEnum.DESTROYED)
        elif self.destroyed is False and self.damaged is False:
            self.button_input.on_click(self.wall_status_changed, WallStatusEnum.DAMAGED)

        diff_x = self.tile_sprite.rect.x - self._prev_x
        diff_y = self.tile_sprite.rect.y - self._prev_y
        self._button.rect.move_ip((diff_x, diff_y))
        self._prev_x = self.tile_sprite.rect.x
        self._prev_y = self.tile_sprite.rect.y
        self.button_input.rect.x = self.tile_sprite.rect.x - 50
        self.button_input.rect.y = self.tile_sprite.rect.y + 50
        for event in event_queue:
            if event.type == pygame.MOUSEBUTTONUP:

                if not ((self.button_input.rect.x <= pygame.mouse.get_pos()[0] <= self.button_input.rect.x + 200) and (
                        self.button_input.rect.y <= pygame.mouse.get_pos()[1] <= self.button_input.rect.y + 25)):
                    self.button_input.disable()
        self._button.update(event_queue)
        self.button_input.update(event_queue)

    def wall_status_changed(self, status: WallStatusEnum):
        if status == WallStatusEnum.DAMAGED:
            self.damaged = True
        elif status == WallStatusEnum.DESTROYED:
            self.damaged = False
            self.destroyed = True
        else:
            raise Exception("Wall status changed back to Intact")

    def draw(self, screen):
        self.button.draw(screen)
        if self.damaged:
            marker = RectLabel(self.button.rect.x, self.button.rect.y + 30, 28, 28,
                               "media/Threat_Markers/damageMarker.png")
            marker.draw(screen)
        elif self.destroyed:
            marker = RectLabel(self.button.rect.x, self.button.rect.y + 30 + 28 + 5, 28, 28,
                               "media/Threat_Markers/damageMarker.png")
            marker.draw(screen)
