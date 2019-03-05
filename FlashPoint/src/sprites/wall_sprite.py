from typing import Tuple

import pygame

from src.UIComponents.rect_label import RectLabel
from src.constants.state_enums import WallStatusEnum
from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.observers.wall_observer import WallObserver
from src.sprites.tile_sprite import TileSprite


class WallSprite(pygame.sprite.Sprite, WallObserver):


    def __init__(self, tile_sprite: TileSprite, tile_model: TileModel , current_player: PlayerModel, id : Tuple[int, int, str]):
        super().__init__()
        self._game: GameStateModel = GameStateModel.instance()
        self._current_player = current_player
        self.button = None
        self.tile_model = tile_model
        self.damaged = False
        self.destroyed = False
        self.id = id

        for wall in self.tile_model.adjacent_edge_objects:
            if wall.id == self.id:
                wall.add_observer(self)
        self.tile_sprite = tile_sprite
        self._prev_x = self.tile_sprite.rect.x
        self._prev_y = self.tile_sprite.rect.y

        #if self.button:
         #   self.button.onclick(self.proccess_input)

    def process_input(self, current_player: PlayerModel):
        pass

    def update(self, event_queue):
        diff_x = self.tile_sprite.rect.x - self._prev_x
        diff_y = self.tile_sprite.rect.y - self._prev_y
        self.button.rect.move_ip((diff_x, diff_y))
        self._prev_x = self.tile_sprite.rect.x
        self._prev_y = self.tile_sprite.rect.y

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
