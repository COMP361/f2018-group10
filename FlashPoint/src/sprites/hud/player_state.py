import pygame

import src.constants.color as Color
from src.UIComponents.interactable import Interactable
from src.constants.state_enums import PlayerStatusEnum
from src.core.event_queue import EventQueue
from src.models.game_units.player_model import PlayerModel
from src.observers.player_observer import PlayerObserver


class PlayerState(Interactable, PlayerObserver):

    def player_carry_changed(self, carry):
        pass

    def __init__(self, x: int, y: int, name: str, color: Color, current: PlayerModel):
        current.add_observer(self)
        self.image = pygame.Surface([64, 64])
        self.bg = pygame.image.load('media/GameHud/wood2-150x64.png')
        self.frame = pygame.image.load('media/GameHud/frame150x64.png')
        self.player_icon = self.color_picker(color)
        self.player_icon = pygame.transform.scale(self.player_icon, (70, 70))
        super().__init__(self.image.get_rect())
        self.font_name = pygame.font.SysFont('Agency FB', 30)
        self.font_other = pygame.font.SysFont('Agency FB', 13)
        self.x = x
        self.y = y
        self.name = name  # nickname restriction 20 symbols
        self.color = color
        self.ap = current.ap
        self.sap = current.special_ap
        self.AP = f'Action Points: {self.ap}'
        self.SAP = f'Special Action Points: {self.sap}'

        self.text = self.font_name.render(self.name, True, current.color)
        self.text_AP = self.font_other.render(self.AP, True, Color.GREEN2)
        self.text_SAP = self.font_other.render(self.SAP, True, Color.GREEN2)

        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.NAME_rect = self.text.get_rect()
        self.NAME_rect.move_ip(15, 2)
        self.AP_rect = self.text_AP.get_rect()
        self.AP_rect.move_ip(15, 32)
        self.SAP_rect = self.text_SAP.get_rect()
        self.SAP_rect.move_ip(15, 43)

        self.is_hovered = False

    def color_picker(self, color: Color):
        return {
            Color.WHITE: pygame.image.load('media/GameHud/PWHITE.png'),
            Color.BLUE: pygame.image.load('media/GameHud/Bleu.png'),
            Color.RED: pygame.image.load('media/GameHud/PRED.png'),
            Color.ORANGE: pygame.image.load('media/GameHud/PORANGE.png'),
            Color.YELLOW: pygame.image.load('media/GameHud/PYELLOW.png'),
            Color.GREEN: pygame.image.load('media/GameHud/PGREEN.png'),
        }[color]

    def enable(self):
        """
        Enables the event hook
        :return:
        """
        self._is_enabled = True

    def disable(self):
        """
        Disables the event hook
        :return:
        """
        self._is_enabled = False

    def update(self, event_queue: EventQueue):
        self.image = pygame.Surface([150, 64])
        # self.bg = pygame.transform.scale(self.bg, (150, 64))
        self.image.blit(self.bg, self.image.get_rect())

        # self.frame = pygame.transform.scale(self.frame,(150,64))

        # TODO Add switch statement for each player color!!!

        # player_icon = pygame.transform.scale(player_icon, (70, 70))
        player_icon_rect = self.player_icon.get_rect()
        player_icon_rect.move_ip(75, 0)

        self.image.blit(self.player_icon, player_icon_rect)
        self.image.blit(self.text, self.NAME_rect)
        self.image.blit(self.text_AP, self.AP_rect)
        # self.image.blit(self.text_SAP, self.SAP_rect)
        self.image.blit(self.frame, self.image.get_rect())

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
