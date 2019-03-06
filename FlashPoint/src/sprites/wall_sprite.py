from typing import Tuple

import pygame
import src.constants.color as Color
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.constants.state_enums import WallStatusEnum
from src.core.event_queue import EventQueue
from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.observers.wall_observer import WallObserver
from src.sprites.tile_sprite import TileSprite
from src.UIComponents.text import Text


class WallSprite(pygame.sprite.Sprite, WallObserver):

    def __init__(self, tile_sprite: TileSprite, tile_model: TileModel, current_player: PlayerModel, id : Tuple[int, int, str]):
        super().__init__()

        self._game: GameStateModel = GameStateModel.instance()
        self._current_player = self._game.players_turn
        self._button = None
        self.tile_model = tile_model
        self.damaged = False
        self.destroyed = False
        self.id = id
        for wall in self.tile_model.adjacent_edge_objects.values():
            if isinstance(wall, WallModel):
                if wall.id == self.id:
                    wall.add_observer(self)
        self.tile_sprite = tile_sprite
        self._prev_x = self.tile_sprite.rect.x
        self._prev_y = self.tile_sprite.rect.y
        self.button_input = RectButton(self.tile_sprite.rect.x+128, self.tile_sprite.rect.y+128, 200, 25, Color.BLACK, 0, Text(pygame.font.SysFont('Arial', 20), "CHoP tHaT MF wAlL", Color.ORANGE))
        self.button_input.disable()

    @property
    def button(self):
        return self._button

    @button.setter
    def button(self, button):
        self._button = button

    def process_input(self):

        self.button_input.enable()

    def update(self, event_queue):
        for event in event_queue:
            if event.type == pygame.MOUSEBUTTONUP:
                if not (self.button_input.rect.x >= pygame.mouse.get_pos()[0] >= self.button_input.rect.x + 200) and not(
                        self.button_input.rect.y >= pygame.mouse.get_pos()[1] >= self.button_input.rect.y + 25):
                    self.button_input.disable()
        diff_x = self.tile_sprite.rect.x - self._prev_x
        diff_y = self.tile_sprite.rect.y - self._prev_y
        self._button.rect.move_ip((diff_x, diff_y))
        self._prev_x = self.tile_sprite.rect.x
        self._prev_y = self.tile_sprite.rect.y
        self.button_input.rect.x = self.tile_sprite.rect.x
        self.button_input.rect.y = self.tile_sprite.rect.y
        self._button.update(event_queue)


    def wall_status_changed(self, status: WallStatusEnum):
        if status == WallStatusEnum.DAMAGED:
            self.damaged = True
        elif status == WallStatusEnum.DESTROYED:
            self.destroyed = True
        else:
            raise Exception("Wall status changed back to Intact")

    def draw(self, screen):
        self.button.draw(screen)
        if self.damaged:
            marker = RectLabel(self.button.rect.x, self.button.rect.y+30, 28, 28, "media/Threat_Markers/damageMarker.png")
            marker.draw(screen)
        if self.destroyed:
            marker = RectLabel(self.button.rect.x, self.button.rect.y+30+28+5, 28, 28, "media/Threat_Markers/damageMarker.png")
            marker.draw(screen)
