from threading import Thread
from datetime import datetime
import time

import pygame

import src.constants.color as Color
from src.constants.state_enums import PlayerStatusEnum
from src.core.event_queue import EventQueue

import time

from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.observers.game_state_observer import GameStateObserver
from src.observers.player_observer import PlayerObserver


class CurrentPlayerState(pygame.sprite.Sprite,PlayerObserver):

    def __init__(self, x: int, y: int, name: str, color: Color,current:PlayerModel):
        super().__init__()
        current.add_observer(self)
        #self.countdown_thread = Thread(target=self.countdown,args= (10,))
        bg = pygame.image.load('media/GameHud/wood2.png')
        self.bg = pygame.transform.scale(bg, (150, 150))
        frame = pygame.image.load('media/GameHud/frame.png')
        self.frame = pygame.transform.scale(frame, (150, 150))
        self.image = pygame.Surface([150, 150])
        self.surface_for_text = pygame.Surface([150, 150])
        self.surface_for_text.fill(Color.GREY)
        self.surface_for_text.set_alpha(130)
        self.player_im = self.color_picker(color)
        self.player_im = pygame.transform.scale(self.player_im, (150, 150))
        self.font_name = pygame.font.SysFont('Agency FB', 30)
        self.font_other = pygame.font.SysFont('Agency FB', 23)
        self.font_time = pygame.font.SysFont('Agency FB', 25)
        self.name = name
        self.ap = current.ap
        self.AP = f'AP: {self.ap}'
        self.sap = 0
        self.SAP = f'Special AP:{self.sap}'


        self.text = self.font_name.render(self.name, True, Color.GREEN2)
        self.text_AP = self.font_other.render(self.AP, True, Color.WHITE)
        self.text_SAP = self.font_other.render(self.SAP, True, Color.WHITE)
        self.turn = False
        self.start = datetime.now()
        self.time_str = f"TOTAL TIME:"
        self.text_time_left = self.font_time.render(self.time_str, True, Color.GREEN2)
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.P_rect = self.text.get_rect()
        self.P_rect.move_ip(15, 10)
        self.AP_rect = self.text_AP.get_rect()
        self.AP_rect.move_ip(15, 50)
        self.SAP_rect = self.text_SAP.get_rect()
        self.SAP_rect.move_ip(15, 70)

        # self.is_hovered = False

    # IN CASE WE WILL NEED THIS

    # def check_mouse_over(self):
    #     mouse = pygame.mouse.get_pos()
    #     rect = self.rect
    #     x_max = rect.x + rect.w
    #     x_min = rect.x
    #     y_max = rect.y + rect.h
    #     y_min = rect.y
    #     return x_max > mouse[0] > x_min and y_max > mouse[1] > y_min

    def color_picker(self, color: Color):
        return {
            Color.WHITE: pygame.image.load('media/GameHud/PWHITE.png'),
            Color.BLUE: pygame.image.load('media/GameHud/Bleu.png'),
            Color.RED: pygame.image.load('media/GameHud/PRED.png'),
            Color.ORANGE: pygame.image.load('media/GameHud/PORANGE.png'),
            Color.YELLOW: pygame.image.load('media/GameHud/PYELLOW.png'),
            Color.GREEN: pygame.image.load('media/GameHud/PGREEN.png'),
        }[color]

    def update(self, event_queue: EventQueue):

        self.image.blit(self.bg, self.image.get_rect())
        self.image.blit(self.player_im, self.image.get_rect().move(50, 0))
        self.image.blit(self.surface_for_text, self.image.get_rect())
        self.image.blit(self.frame, self.image.get_rect())
        self.image.blit(self.text, self.P_rect)
        self.image.blit(self.text_AP, self.AP_rect)
        #if gamemode is expirienced
        #self.image.blit(self.text_SAP, self.SAP_rect)

        if self.turn:
            self.time_left_rect = self.text_time_left.get_rect()
            self.time_left_rect.move_ip(15, 100)
            self.image.blit(self.text_time_left, self.time_left_rect)


    def player_status_changed(self, status: PlayerStatusEnum):
        pass


    def player_ap_changed(self, updated_ap: int):
        self.ap = updated_ap
        self.AP = f'AP: {self.ap}'
        self.text_AP = self.font_other.render(self.AP, True, Color.GREEN2)

    def player_special_ap_changed(self, updated_ap: int):
        pass


    def player_position_changed(self, x_pos: int, y_pos: int):
        pass


    def player_wins_changed(self, wins: int):
        pass


    def player_losses_changed(self, losses: int):
        pass


