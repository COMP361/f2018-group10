from typing import Tuple

import pygame
import src.constants.color as Color
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.constants.state_enums import WallStatusEnum

from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.observers.wall_observer import WallObserver
from src.sprites.tile_sprite import TileSprite
from src.UIComponents.text import Text


class WallSprite(pygame.sprite.Sprite, WallObserver):

    def __init__(self, wall_model: WallModel, orientation: str, tile_sprite: TileSprite, tile_model: TileModel,
                 id: Tuple[int, int, str]):
        super().__init__()
        self.orientation = orientation
        self._game: GameStateModel = GameStateModel.instance()
        self._current_player = self._game.players_turn
        self._button = None
        self.tile_model = tile_model
        self.id = id
        self.wall_model = wall_model
        self.wall_model.add_observer(self)

        self.damaged = self.wall_model.wall_status == WallStatusEnum.DAMAGED
        self.destroyed = self.wall_model.wall_status == WallStatusEnum.DESTROYED
        self.tile_sprite = tile_sprite
        self._prev_x = self.tile_sprite.rect.x
        self._prev_y = self.tile_sprite.rect.y
        self.button_input = RectButton(self.tile_sprite.rect.x, self.tile_sprite.rect.y, 100, 25, Color.WOOD, 0,
                                       Text(pygame.font.SysFont('Agency FB', 20), "Chop Wall", Color.GREEN2))
        pygame.draw.rect(self.button_input.image,Color.YELLOW,[0,0,100,25],3)
        self.button_input.disable()
        self.can_chop = False

    @property
    def direction(self) -> str:
        return self.id[2]

    @property
    def wall(self):
        return self.wall_model

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
        self.button_input.rect.x = self.tile_sprite.rect.x + 14
        self.button_input.rect.y = self.tile_sprite.rect.y + 50

        for event in event_queue:
            if event.type == pygame.MOUSEBUTTONUP:
                if not ((self.button_input.rect.x <= pygame.mouse.get_pos()[0] <= self.button_input.rect.x + 100) and (
                        self.button_input.rect.y <= pygame.mouse.get_pos()[1] <= self.button_input.rect.y + 25)):
                    self.button_input.disable()
                    self.can_chop = False

        self._button.update(event_queue)
        self.button_input.update(event_queue)

    def wall_status_changed(self, status: WallStatusEnum):
        if status == WallStatusEnum.DAMAGED:
            self.damaged = True
        elif status == WallStatusEnum.DESTROYED:
            self.damaged = False
            self.destroyed = True

    def draw_menu(self, screen):
        self.button.draw(screen)
        if self.can_chop:
            self.button_input.draw(screen)

    def draw(self, screen):
        x_offset1 = 0 if self.orientation == "vertical" else 25
        y_offset1 = 0 if self.orientation == "horizontal" else 25
        x_offset2 = 0 if self.orientation == "vertical" else 50
        y_offset2 = 0 if self.orientation == "horizontal" else 50

        if self.damaged:
            marker = RectLabel(self.button.rect.x + x_offset1, self.button.rect.y + y_offset1, 28, 28,
                               "media/Threat_Markers/damageMarker.png")
            marker.draw(screen)
        elif self.destroyed:
            marker = RectLabel(self.button.rect.x + x_offset2, self.button.rect.y + y_offset2, 28, 28,
                               "media/Threat_Markers/damageMarker.png")
            marker.draw(screen)
            marker = RectLabel(self.button.rect.x + x_offset1, self.button.rect.y + y_offset1, 28, 28,
                               "media/Threat_Markers/damageMarker.png")
            marker.draw(screen)

    def disable_chop(self):
        self.can_chop = False

    def enable_chop(self):
        self.can_chop = True
