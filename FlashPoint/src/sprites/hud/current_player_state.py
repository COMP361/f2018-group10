from datetime import datetime

import pygame

import src.constants.color as Color
from src.constants.state_enums import PlayerStatusEnum, GameKindEnum
from src.core.event_queue import EventQueue
from src.models.game_units.player_model import PlayerModel
from src.observers.player_observer import PlayerObserver
import src.constants.media_constants as MEDIA_CONSTS


class CurrentPlayerState(pygame.sprite.Sprite, PlayerObserver):

    def player_carry_changed(self, carry):
        pass


    def player_leading_victim_changed(self, leading_victim):
        pass

    def __init__(self, x: int, y: int, name: str, color: Color, current: PlayerModel, rules: GameKindEnum):
        super().__init__()
        current.add_observer(self)
        bg = pygame.image.load(MEDIA_CONSTS.WOOD)
        self.bg = pygame.transform.scale(bg, (150, 150))
        frame = pygame.image.load(MEDIA_CONSTS.FRAME)
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
        self.rules = rules
        self.ap = current.ap
        self.AP = f'AP: {self.ap}'
        self.sap = current.special_ap
        self.SAP = f'Special AP: {self.sap}'

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
        self.SAP_rect.move_ip(15, 72)

    def color_picker(self, color: Color):
        return {
            Color.WHITE: pygame.image.load(MEDIA_CONSTS.P_WHITE),
            Color.BLUE: pygame.image.load(MEDIA_CONSTS.P_BLUE),
            Color.RED: pygame.image.load(MEDIA_CONSTS.P_RED),
            Color.ORANGE: pygame.image.load(MEDIA_CONSTS.P_ORANGE),
            Color.YELLOW: pygame.image.load(MEDIA_CONSTS.P_YELLOW),
            Color.GREEN: pygame.image.load(MEDIA_CONSTS.P_GREEN),
        }[color]

    def update(self, event_queue: EventQueue):
        self.image.blit(self.bg, self.image.get_rect())
        self.image.blit(self.player_im, self.image.get_rect().move(50, 0))
        self.image.blit(self.surface_for_text, self.image.get_rect())
        self.image.blit(self.frame, self.image.get_rect())
        self.image.blit(self.text, self.P_rect)
        self.image.blit(self.text_AP, self.AP_rect)

        if self.rules is GameKindEnum.EXPERIENCED:
            self.image.blit(self.text_SAP, self.SAP_rect)

        if self.turn:
            self.time_left_rect = self.text_time_left.get_rect()
            self.time_left_rect.move_ip(15, 100)
            self.image.blit(self.text_time_left, self.time_left_rect)

    def player_status_changed(self, status: PlayerStatusEnum):
        pass

    def player_ap_changed(self, updated_ap: int):
        self.AP = f'AP: {updated_ap}'
        self.text_AP = self.font_other.render(self.AP, True, Color.GREEN2)

    def player_special_ap_changed(self, updated_sap: int):
        self.SAP = f'Special AP: {updated_sap}'
        self.text_SAP = self.font_other.render(self.SAP, True, Color.GREEN2)

    def player_position_changed(self, x_pos: int, y_pos: int):
        pass

    def player_wins_changed(self, wins: int):
        pass

    def player_losses_changed(self, losses: int):
        pass

    def player_role_changed(self, role):
        pass