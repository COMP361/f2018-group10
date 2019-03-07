from threading import Thread
from datetime import datetime
import time

import pygame

import src.constants.color as Color
from src.core.event_queue import EventQueue

import time

from src.models.game_state_model import GameStateModel
from src.observers.game_state_observer import GameStateObserver


class CurrentPlayerState(pygame.sprite.Sprite,GameStateObserver):

    def __init__(self, x: int, y: int, name: str, color: Color):
        super().__init__()
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
        self.AP = f'AP: {4}'
        self.SAP = f'Special AP:{4}'


        self.text = self.font_name.render(self.name, True, Color.GREEN2)
        self.text_AP = self.font_other.render(self.AP, True, Color.GREEN2)
        self.text_SAP = self.font_other.render(self.SAP, True, Color.GREEN2)
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


    # def countdown(self, count):
    #     while count:
    #         mins,secs = divmod(count, 60)
    #         temp = '{:02d}:{:02d}'.format(mins, secs)
    #         self.time_str = f"TIME LEFT: {temp}"
    #         self.text_time_left = self.font_time.render(self.time_str, True, Color.WHITE)
    #         time.sleep(1)
    #         count -= 1
    #
    #     self.turn = False

    def notify_player_index(self, player_index: int):
        pass

