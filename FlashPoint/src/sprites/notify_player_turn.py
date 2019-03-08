import threading
import pygame
import time
from threading import Thread
import src.constants.color as Color
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.action_events.turn_events.end_turn_event import EndTurnEvent
from src.core.event_queue import EventQueue
from src.core.networking import Networking
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.observers.game_state_observer import GameStateObserver
from src.UIComponents.text import Text


class NotifyPlayerTurn(pygame.sprite.Sprite, GameStateObserver):

    def __init__(self, current_player: PlayerModel, current_sprite:pygame.sprite.Sprite,sprite_group:pygame.sprite.Group):
        super().__init__()
        self.image = pygame.Surface([0,0])
        self.rect = self.image.get_rect()
        self.enabled = False
        self.running = True
        self.countdown_thread = None
        self.font_time = pygame.font.SysFont('Agency FB', 25)

        self.not_your_turn = self._init_not_your_turn()



        self._current_player = current_player
        self._current_sprite = current_sprite
        self._active_sprites = sprite_group

        GameStateModel.instance().add_observer(self)

    def notify_player_index(self, player_index: int):

        self.enabled = GameStateModel.instance().players[player_index] == self._current_player
        if self.enabled:
            self.your_turn = self._init_your_turn()
            self.btn = self._init_end_turn_button()
            self._active_sprites.remove(self.not_your_turn)
            self._active_sprites.add(self.btn)
            self._active_sprites.add(self.your_turn)
            self._current_sprite.turn = True
            self.running = True

            self.countdown_thread = Thread(target=self.countdown, args=(10,))
            self.countdown_thread.start()


    def _init_end_turn_button(self):
        btn = RectButton(1130, 500, 150, 50, background=Color.ORANGE,
                         txt_obj=Text(pygame.font.SysFont('Agency FB', 23), "END TURN",Color.GREEN2))
        btn.change_bg_image('media/GameHud/wood2.png')
        btn.add_frame('media/GameHud/frame.png')
        btn.on_click(self._end_turn)
        return btn

    def _init_your_turn(self):

        rct = RectLabel(880,600,250,50,background=Color.ORANGE,
                        txt_obj=Text(pygame.font.SysFont('Agency FB', 30),"YOUR TURN",Color.GREEN2))
        rct.change_bg_image('media/GameHud/wood2.png')
        rct.add_frame('media/GameHud/frame.png')
        return rct

    def _init_not_your_turn(self):

        rct = RectLabel(880,600,250,50,background=Color.ORANGE,
                        txt_obj=Text(pygame.font.SysFont('Agency FB', 30),"NOT YOUR TURN",Color.GREEN2))
        rct.change_bg_image('media/GameHud/wood2.png')
        rct.add_frame('media/GameHud/frame.png')
        return rct

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
        self._active_sprites.remove(self.your_turn)
        self._active_sprites.add(self.not_your_turn)
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


    def damage_changed(self, new_damage: int):
        pass

    def saved_victims(self, victims_saved: int):
        pass

    def dead_victims(self, victims_dead: int):
        pass
