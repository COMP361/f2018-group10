import threading
import pygame
import time
from threading import Thread
import src.core.pause_event_switch as switch

import src.constants.color as Color
from src.action_events.stop_command_event import StopCommandEvent
from src.action_events.end_turn_advance_fire import EndTurnAdvanceFireEvent
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.rect_button import RectButton
from src.core.event_queue import EventQueue
from src.core.networking import Networking
from src.constants.state_enums import GameStateEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.observers.game_state_observer import GameStateObserver
from src.UIComponents.text import Text


class NotifyPlayerTurn(pygame.sprite.Sprite, GameStateObserver):

    def damage_changed(self, new_damage: int):
        pass

    def saved_victims(self, victims_saved: int):
        pass

    def dead_victims(self, victims_dead: int):
        pass

    def player_command(self, source: PlayerModel, target: PlayerModel):
        pass

    def __init__(self, current_player: PlayerModel, current_sprite: pygame.sprite.Sprite,
                 sprite_group: pygame.sprite.Group):
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
        self.rect.move_ip(880, 600)
        self.not_your_turn = self.init_not_your_turn()
        self._current_player = current_player
        self._current_sprite = current_sprite
        self._active_sprites = sprite_group
        self._should_advance_fire = False
        self.btn = None
        self.your_turn = None
        switch.ABORT = False

        GameStateModel.instance().add_observer(self)

    def update(self, event_queue:EventQueue):
        if self.enabled and self._current_sprite.turn:
            self.image.blit(self.bg, self.image.get_rect())
            self.image.blit(self.frame, self.image.get_rect())
            self.image.blit(self.text, self.image.get_rect().move(77, 7))

    def notify_player_index(self, player_index: int):
        self.enabled = (GameStateModel.instance().players[player_index] == self._current_player)

        if self.enabled:
            self.your_turn = self._init_your_turn()
            self.btn = self._init_end_turn_button()
            self._active_sprites.remove(self.not_your_turn)
            self._active_sprites.add(self.btn)
            self._active_sprites.add(self.your_turn)
            self._current_sprite.turn = True
            self.running = True

            self.countdown_thread = Thread(target=self.countdown, args=(120,), daemon=True)
            self.countdown_thread.start()
        else:
            self._current_sprite.turn = False
            if self.btn:
                self._active_sprites.remove(self.btn)
            if self.your_turn:
                self._active_sprites.remove(self.your_turn)
            self._active_sprites.add(self.not_your_turn)

    def _init_your_turn(self):
        rct = RectLabel(880, 600, 250, 50, background=Color.ORANGE,
                        txt_obj=Text(pygame.font.SysFont('Agency FB', 30), "YOUR TURN", Color.GREEN2))
        rct.change_bg_image('media/GameHud/wood2.png')
        rct.add_frame('media/GameHud/frame.png')
        return rct

    def init_not_your_turn(self):
        rct = RectLabel(880, 600, 250, 50, background=Color.ORANGE,
                        txt_obj=Text(pygame.font.SysFont('Agency FB', 30), "NOT YOUR TURN", Color.GREEN2))
        rct.change_bg_image('media/GameHud/wood2.png')
        rct.add_frame('media/GameHud/frame.png')
        return rct

    def _init_end_turn_button(self):
        btn = RectButton(1130, 500, 150, 50, background=Color.ORANGE,
                         txt_obj=Text(pygame.font.SysFont('Arial', 23), "END TURN",Color.GREEN2))
        btn.change_bg_image('media/GameHud/wood2.png')
        btn.add_frame('media/GameHud/frame.png')
        btn.on_click(self._end_turn)
        return btn

    def countdown(self, count):
        while count and self.running:
            if switch.ABORT:
                return
            mins,secs = divmod(count, 60)
            temp = '{:02d}:{:02d}'.format(mins, secs)
            self.time_str = f"TIME LEFT: {temp}"
            self._current_sprite.text_time_left = self.font_time.render(self.time_str, True, Color.GREEN2)
            time.sleep(1)
            count -= 1
        self.time_str = ""
        self.enabled = False
        self.running = False

        turn_event = EndTurnAdvanceFireEvent()
        # send end turn, see ChatBox for example
        try:
            if Networking.get_instance().is_host:
                Networking.get_instance().send_to_all_client(turn_event)
            else:
                Networking.get_instance().send_to_server(turn_event)
        except AttributeError as e:
            pass

        if not self._should_advance_fire:
            self._should_advance_fire = True
        
    def _end_turn(self):
        self._current_sprite.turn = False
        self.enabled = False
        self.running = False

        command = GameStateModel.instance().command
        if command[0]:
            StopCommandEvent(command[0]).execute()

        if self.countdown_thread != threading.current_thread() and self.countdown_thread.is_alive():
            self.countdown_thread.join()

    def notify_game_state(self, game_state: GameStateEnum):
        pass

    def player_added(self, player: PlayerModel):
        pass

    def player_removed(self, player: PlayerModel):
        pass
