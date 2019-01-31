import pygame

import src.constants.Color as Color
from src.core.EventQueue import EventQueue


class CurrentPlayerState(pygame.sprite.Sprite):

    def __init__(self, x: int, y: int, name: str):
        super().__init__()
        self.image = pygame.Surface([150, 1500])
        self.font_name = pygame.font.SysFont('Agency FB', 30)
        self.font_other = pygame.font.SysFont('Agency FB', 20)
        self.name = name
        self.AP = "AP:"
        self.SAP = "Special AP:"
        self.text = self.font_name.render(self.name, True, Color.WHITE)
        self.text_AP = self.font_other.render(self.AP, True, Color.WHITE)
        self.text_SAP = self.font_other.render(self.SAP, True, Color.WHITE)

        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.P_rect = self.text.get_rect()
        self.P_rect.move_ip(15, 10)
        self.AP_rect = self.text_AP.get_rect()
        self.AP_rect.move_ip(15, 50)
        self.SAP_rect = self.text_SAP.get_rect()
        self.SAP_rect.move_ip(15, 70)
        # self.is_hovered = False


    #IN CASE WE WILL NEED THIS

    # def check_mouse_over(self):
    #     mouse = pygame.mouse.get_pos()
    #     rect = self.rect
    #     x_max = rect.x + rect.w
    #     x_min = rect.x
    #     y_max = rect.y + rect.h
    #     y_min = rect.y
    #     return x_max > mouse[0] > x_min and y_max > mouse[1] > y_min

    def update(self, event_queue: EventQueue):
        bg = pygame.image.load('media/wood2.png')
        bg = pygame.transform.scale(bg, (150, 150))
        self.image.blit(bg, self.image.get_rect())
        frame = pygame.image.load('media/frame.png')
        frame = pygame.transform.scale(frame,(150,150))
        self.image.blit(frame,self.image.get_rect())
        self.image.blit(self.text, self.P_rect)
        self.image.blit(self.text_AP, self.AP_rect)
        self.image.blit(self.text_SAP, self.SAP_rect)


