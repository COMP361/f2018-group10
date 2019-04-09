import pygame

import src.constants.color as Color
from src.UIComponents.interactable import Interactable
from src.constants.state_enums import PlayerStatusEnum, GameKindEnum, PlayerRoleEnum
from src.core.event_queue import EventQueue
from src.models.game_units.player_model import PlayerModel
from src.observers.player_observer import PlayerObserver


class PlayerState(Interactable, PlayerObserver):


    def player_carry_changed(self, carry):
        pass

    def player_leading_victim_changed(self, leading_victim):
        pass

    def __init__(self, x: int, y: int, name: str, color: Color, current: PlayerModel,rules):
        current.add_observer(self)

        self.image = pygame.Surface([150, 64])
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
        self.rules = rules
        self.role = current.role
        #self.ability = self.ability_description(self.role)
        #self.ability = "Pizda"
        self.AP = f'Action Points: {current.ap}'
        self.SAP = f'Special Action Points: {current.special_ap}'


        #self.text_description = self.font_other.render(self.ability,True,Color.WHITE)
        self.text = self.font_name.render(self.name, True, current.color)
        self.text_AP = self.font_other.render(self.AP, True, Color.GREEN2)
        self.text_SAP = self.font_other.render(self.SAP, True, Color.GREEN2)

        self.rect = self.image.get_rect()
        self.rect.move_ip(self.x, self.y)
        self.NAME_rect = self.text.get_rect()
        self.NAME_rect.move_ip(15, 2)
        self.AP_rect = self.text_AP.get_rect()
        self.AP_rect.move_ip(15, 32)
        self.SAP_rect = self.text_SAP.get_rect()
        self.SAP_rect.move_ip(15, 43)
        #self.text_description_rect = self.text_description.get_rect()
        #self.text_description_rect.move_ip(15,2)

        self.surface_for_text = pygame.Surface([150, 150])
        self.surface_for_text.fill(Color.GREY)
        self.surface_for_text.set_alpha(130)

        self.surface_for_text_hover = pygame.Surface([150, 150])
        self.surface_for_text_hover.fill(Color.GREY)
        self.surface_for_text_hover.set_alpha(130)




    def color_picker(self, color: Color):
        return {
            Color.WHITE: pygame.image.load('media/GameHud/PWHITE.png'),
            Color.BLUE: pygame.image.load('media/GameHud/Bleu.png'),
            Color.RED: pygame.image.load('media/GameHud/PRED.png'),
            Color.ORANGE: pygame.image.load('media/GameHud/PORANGE.png'),
            Color.YELLOW: pygame.image.load('media/GameHud/PYELLOW.png'),
            Color.GREEN: pygame.image.load('media/GameHud/PGREEN.png'),
        }[color]

    # def ability_description(self,role:PlayerRoleEnum):
    #     return {
    #         PlayerRoleEnum.GENERALIST: "No special abilities or actions",
    #         PlayerRoleEnum.PARAMEDIC: "Treat: Resuscitate a victim: 1\n"
    #                                   "Place a Heal marker under the\n"
    #                                   "treated victim to denote this\n"
    #                                   "change in status",
    #
    #     }[role]


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

        mouse = pygame.mouse.get_pos()

        if self.x + 150 > mouse[0] > self.x and self.y + 64 > mouse[1] > self.y:

            self.image.blit(self.bg,self.image.get_rect())
            self.image.blit(self.surface_for_text,self.image.get_rect())

            if self.role == PlayerRoleEnum.GENERALIST:
                self.line_1 = "No special abilities or actions"
                self.text_line1 = self.font_other.render(self.line_1, True, Color.GREEN2)
                self.text_line1_rect = self.text_line1.get_rect()
                self.text_line1_rect.move_ip(15,24)
                self.image.blit(self.text_line1,self.text_line1_rect)
            elif self.role == PlayerRoleEnum.PARAMEDIC:
                self.line_1 = "Resuscitate a victim (1 AP):"
                self.line_2 = "Place a Heal marker under the"
                self.line_3 = "treated victim to denote this"
                self.line_4 = "change in status"
                self.text_line1 = self.font_other.render(self.line_1, True, Color.GREEN2)
                self.text_line2 = self.font_other.render(self.line_2, True, Color.GREEN2)
                self.text_line3 = self.font_other.render(self.line_3, True, Color.GREEN2)
                self.text_line4 = self.font_other.render(self.line_4, True, Color.GREEN2)
                self.text_line1_rect = self.text_line1.get_rect()
                self.text_line2_rect = self.text_line1.get_rect()
                self.text_line3_rect = self.text_line1.get_rect()
                self.text_line4_rect = self.text_line4.get_rect()
                self.text_line1_rect.move_ip(15, 4)
                self.text_line2_rect.move_ip(15, 15)
                self.text_line3_rect.move_ip(15, 26)
                self.text_line4_rect.move_ip(15, 37)
                self.image.blit(self.text_line1, self.text_line1_rect)
                self.image.blit(self.text_line2, self.text_line2_rect)
                self.image.blit(self.text_line3, self.text_line3_rect)
                self.image.blit(self.text_line4, self.text_line4_rect)
            elif self.role == PlayerRoleEnum.CAFS:
                self.line_1 = "3 free extinguish AP per turn"
                self.text_line1 = self.font_other.render(self.line_1, True, Color.GREEN2)
                self.text_line1_rect = self.text_line1.get_rect()
                self.text_line1_rect.move_ip(15, 24)
                self.image.blit(self.text_line1, self.text_line1_rect)
            elif self.role == PlayerRoleEnum.HAZMAT:
                self.line_1 = "Dispose (2 AP):"
                self.line_2 = "Remove a hazmat from the fire-"
                self.line_3 = "fighter space "
                self.text_line1 = self.font_other.render(self.line_1, True, Color.GREEN2)
                self.text_line2 = self.font_other.render(self.line_2, True, Color.GREEN2)
                self.text_line3 = self.font_other.render(self.line_3, True, Color.GREEN2)
                self.text_line1_rect = self.text_line1.get_rect()
                self.text_line2_rect = self.text_line1.get_rect()
                self.text_line3_rect = self.text_line1.get_rect()
                self.text_line1_rect.move_ip(15, 4)
                self.text_line2_rect.move_ip(15, 15)
                self.text_line3_rect.move_ip(15, 26)
                self.image.blit(self.text_line1, self.text_line1_rect)
                self.image.blit(self.text_line2, self.text_line2_rect)
                self.image.blit(self.text_line3, self.text_line3_rect)
            elif self.role == PlayerRoleEnum.RESCUE:
                self.line_1 = "SAPs are only for movement"
                self.line_2 = "Chop (1 AP):"
                self.line_3 = "The rescue specialist pays double"
                self.line_4 = "AP to extinguish fire/smoke"
                self.text_line1 = self.font_other.render(self.line_1, True, Color.GREEN2)
                self.text_line2 = self.font_other.render(self.line_2, True, Color.GREEN2)
                self.text_line3 = self.font_other.render(self.line_3, True, Color.GREEN2)
                self.text_line4 = self.font_other.render(self.line_4, True, Color.GREEN2)
                self.text_line1_rect = self.text_line1.get_rect()
                self.text_line2_rect = self.text_line1.get_rect()
                self.text_line3_rect = self.text_line1.get_rect()
                self.text_line4_rect = self.text_line4.get_rect()
                self.text_line1_rect.move_ip(15, 4)
                self.text_line2_rect.move_ip(15, 15)
                self.text_line3_rect.move_ip(15, 26)
                self.text_line4_rect.move_ip(15, 37)
                self.image.blit(self.text_line1, self.text_line1_rect)
                self.image.blit(self.text_line2, self.text_line2_rect)
                self.image.blit(self.text_line3, self.text_line3_rect)
                self.image.blit(self.text_line4, self.text_line4_rect)
            elif self.role == PlayerRoleEnum.DRIVER:
                self.line_1 = "Fire The Deck Gun (2 AP):"
                self.line_2 = "ASK FRANCIS HOW IT WORKS"
                self.text_line1 = self.font_other.render(self.line_1, True, Color.GREEN2)
                self.text_line2 = self.font_other.render(self.line_2, True, Color.GREEN2)
                self.text_line1_rect = self.text_line1.get_rect()
                self.text_line2_rect = self.text_line1.get_rect()
                self.text_line1_rect.move_ip(15, 4)
                self.text_line2_rect.move_ip(15, 15)
                self.image.blit(self.text_line1, self.text_line1_rect)
                self.image.blit(self.text_line2, self.text_line2_rect)
            elif self.role == PlayerRoleEnum.IMAGING:
                self.line_1 = "Identify (1 AP):"
                self.line_2 = "Flip a POI marker anywhere"
                self.line_3 = "in the board"
                self.text_line1 = self.font_other.render(self.line_1, True, Color.GREEN2)
                self.text_line2 = self.font_other.render(self.line_2, True, Color.GREEN2)
                self.text_line3 = self.font_other.render(self.line_3, True, Color.GREEN2)
                self.text_line1_rect = self.text_line1.get_rect()
                self.text_line2_rect = self.text_line1.get_rect()
                self.text_line3_rect = self.text_line1.get_rect()
                self.text_line1_rect.move_ip(15, 4)
                self.text_line2_rect.move_ip(15, 15)
                self.text_line3_rect.move_ip(15, 26)
                self.image.blit(self.text_line1, self.text_line1_rect)
                self.image.blit(self.text_line2, self.text_line2_rect)
                self.image.blit(self.text_line3, self.text_line3_rect)
            elif self.role == PlayerRoleEnum.DOGE:
                self.line_1 = "DRAG(4 AP): carry a victim into"
                self.line_2 = "an Adjacent space"
                self.line_3 = "SQUEZZE(2 AP): move throug a"
                self.line_4 = "damaged wall"
                self.text_line1 = self.font_other.render(self.line_1, True, Color.GREEN2)
                self.text_line2 = self.font_other.render(self.line_2, True, Color.GREEN2)
                self.text_line3 = self.font_other.render(self.line_3, True, Color.GREEN2)
                self.text_line4 = self.font_other.render(self.line_4, True, Color.GREEN2)
                self.text_line1_rect = self.text_line1.get_rect()
                self.text_line2_rect = self.text_line1.get_rect()
                self.text_line3_rect = self.text_line1.get_rect()
                self.text_line4_rect = self.text_line4.get_rect()
                self.text_line1_rect.move_ip(15, 4)
                self.text_line2_rect.move_ip(15, 15)
                self.text_line3_rect.move_ip(15, 26)
                self.text_line4_rect.move_ip(15, 37)
                self.image.blit(self.text_line1, self.text_line1_rect)
                self.image.blit(self.text_line2, self.text_line2_rect)
                self.image.blit(self.text_line3, self.text_line3_rect)
                self.image.blit(self.text_line4, self.text_line4_rect)

            self.image.blit(self.frame,self.image.get_rect())

        else:

            self.image = pygame.Surface([150, 64])
            self.image.blit(self.bg, self.image.get_rect())

            player_icon_rect = self.player_icon.get_rect()
            player_icon_rect.move_ip(75, 0)

            self.image.blit(self.player_icon, player_icon_rect)
            self.image.blit(self.text, self.NAME_rect)
            self.image.blit(self.text_AP, self.AP_rect)

            if self.rules is GameKindEnum.EXPERIENCED:
                self.image.blit(self.text_SAP, self.SAP_rect)
            self.image.blit(self.frame, self.image.get_rect())


    def player_status_changed(self, status: PlayerStatusEnum):
        pass

    def player_ap_changed(self, updated_ap: int):
        self.AP = f'Action Points: {updated_ap}'
        self.text_AP = self.font_other.render(self.AP, True, Color.GREEN2)

    def player_special_ap_changed(self, updated_sap: int):
        self.SAP = f'Special Action Points: {updated_sap}'
        self.text_SAP = self.font_other.render(self.SAP, True, Color.GREEN2)

    def player_position_changed(self, x_pos: int, y_pos: int):
        pass

    def player_wins_changed(self, wins: int):
        pass

    def player_losses_changed(self, losses: int):
        pass

    def player_role_changed(self, role):
        pass