import pygame
import time
from threading import Thread
import src.constants.color as Color
from constants.state_enums import GameStateEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.observers.game_state_observer import GameStateObserver


class NotifyPlayerTurn(pygame.sprite.Sprite, GameStateObserver):

    def __init__(self, current_player: PlayerModel, current_sprite: pygame.sprite.Sprite):
        super().__init__()
        self.enabled = False
        self.countdown_thread = Thread(target=self.countdown, args=(10,))
        self.image = pygame.Surface([250, 50])
        self.font_time = pygame.font.SysFont('Agency FB', 25)
        bg = pygame.image.load('media/GameHud/wood2.png')
        self.bg = pygame.transform.scale(bg, (250, 50))
        self.msg = "YOUR TURN"
        frame = pygame.image.load('media/GameHud/frame.png')
        self.frame = pygame.transform.scale(frame, (250, 50))
        self.font_name = pygame.font.SysFont('Agency FB', 30)
        self.text = self.font_name.render(self.msg, True, Color.GREEN2)
        self.rect = self.image.get_rect()
        self.rect.move_ip(500, 500)
        self._current_player = current_player
        self._current_sprite = current_sprite

        GameStateModel.instance().add_observer(self)

    def draw(self, screen: pygame.display):
        if self.enabled and self._current_sprite.turn:
            self.image.blit(self.bg, self.image.get_rect())
            self.image.blit(self.frame, self.image.get_rect())
            self.image.blit(self.text, self.image.get_rect().move(77, 7))
            screen.blit(self.image, self.image.get_rect().move(880, 600))

    def notify_player_index(self, player_index: int):

        self.enabled = GameStateModel.instance().players[player_index] == self._current_player
        if self.enabled:
            self._current_sprite.turn = True
            self.countdown_thread.start()

    def countdown(self, count):
        while count:
            mins, secs = divmod(count, 60)
            temp = '{:02d}:{:02d}'.format(mins, secs)
            self.time_str = f"TIME LEFT: {temp}"
            self._current_sprite.text_time_left = self.font_time.render(self.time_str, True, Color.GREEN2)
            time.sleep(1)
            count -= 1

        self._current_sprite.turn = False

    def notify_game_state(self, game_state: GameStateEnum):
        pass
