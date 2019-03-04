from datetime import datetime
import pygame

import src.constants.color as Color
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.observers.game_state_observer import GameStateObserver
from src.scenes.game_board_scene import GameBoardScene


class NotifyPlayerTurn(pygame.sprite.Sprite,GameStateObserver):

    def __init__(self, current_player: PlayerModel):
        self.enabled = False
        self.image = pygame.Surface([300,150])
        self.image.fill(Color.ORANGE)
        self.rect = self.image.get_rect()
        self.rect.move_ip(500, 500)
        self._current_player = current_player

        GameStateModel.instance().observers.append(self)

    def draw(self, screen: pygame.display):
        if self.enabled:
            screen.blit(self.image, self.image.get_rect())


    def notify_player_index(self, player_index: int):

        self.enabled = GameBoardScene._game.players[player_index] == self._current_player
        if self.enabled:
            GameBoardScene._current_sprite.turn = True
            GameBoardScene._current_sprite.start = datetime.now()






