import threading
import pygame
import time
from threading import Thread
import src.constants.color as Color
from src.UIComponents.rect_button import RectButton
from src.action_events.turn_events.end_turn_event import EndTurnEvent
from src.core.networking import Networking
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.observers.game_state_observer import GameStateObserver
from src.UIComponents.text import Text


class NotifyPlayerTurn(pygame.sprite.Sprite, GameStateObserver):

    def __init__(self, current_player: PlayerModel, current_sprite:pygame.sprite.Sprite,sprite_group:pygame.sprite.Group):
        super().__init__()
        self.enabled = False
        self.running = True
        self.countdown_thread = None
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
        self._active_sprites = sprite_group

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
            self.btn = self._init_end_turn_button()
            self._active_sprites.add(self.btn)
            self._current_sprite.turn = True
            self.running = True

            self.countdown_thread = Thread(target=self.countdown, args=(10,))
            self.countdown_thread.start()


    def _init_end_turn_button(self):
        btn = RectButton(1130, 500, 150, 50, background=Color.ORANGE,
                         txt_obj=Text(pygame.font.SysFont('Arial', 23), "End Turn"))
        btn.on_click(self._end_turn)
        return btn

    def countdown(self, count):
        while count and self.running:
            mins,secs = divmod(count, 60)
            temp = '{:02d}:{:02d}'.format(mins, secs)
            self.time_str = f"TIME LEFT: {temp}"
            self._current_sprite.text_time_left = self.font_time.render(self.time_str, True, Color.GREEN2)
            time.sleep(1)
            count -= 1
        self.time_str = ""
        self.enabled = False
        self.running = False
        self._current_sprite.turn = False
        self._active_sprites.remove(self.btn)
        turn_event = EndTurnEvent()
        # send end turn, see ChatBox for example
        #Networking.get_instance().send_to_server(turn_event)
        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(turn_event)
        else:
            Networking.get_instance().client.send(turn_event)

    def _end_turn(self):
        self._current_sprite.turn = False
        self.enabled = False
        self.running = False

        if self.countdown_thread != threading.current_thread() and self.countdown_thread.is_alive():
            self.countdown_thread.join()

