from typing import Any, Union

import pygame
from pygame.surface import SurfaceType

import src.constants.Color as Color
from src.Windows.UIComponents.Text import Text


class PlayerState(pygame.sprite.Sprite):

    def __init__(self,x: int, y: int, name: str,color: Color):
        super().__init__()
        self.image = pygame.Surface([64*2, 64])
        self.font_name = pygame.font.SysFont('Arial', 30)
        self.font_other = pygame.font.SysFont('Arial', 13)
        self.name = name
        self.color = color
        self.AP = "Action Points:"
        self.SAP = "Special Action Points:"
        self.text = self.font_name.render(self.name, True, (0, 0, 0))
        self.text_AP = self.font_other.render(self.AP, True, (0, 0, 0))
        self.text_SAP = self.font_other.render(self.SAP, True, (0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.P_rect = self.text.get_rect()
        self.P_rect.move_ip(15,13)
        self.AP_rect = self.text_AP.get_rect()
        self.AP_rect.move_ip(0,15)
        self.SAP_rect = self.text_SAP.get_rect()
        self.SAP_rect.move_ip(0,30)

        self.is_hovered = False
        #self._render()

    #def _render(self):
    #   self.image.fill(Color.GREY, self.rect)


    def check_mouse_over(self):
        mouse = pygame.mouse.get_pos()
        rect = self.rect
        x_max = rect.x + rect.w
        x_min = rect.x
        y_max = rect.y + rect.h
        y_min = rect.y
        return x_max > mouse[0] > x_min and y_max > mouse[1] > y_min



    def update(self):
        if self.check_mouse_over():
            if not self.is_hovered:
                self.is_hovered = True
                self.image.fill(Color.RED)
                #self.image.blit(self.text, self.text.get_rect())
                self.image.blit(self.text_AP, self.AP_rect)
                self.image.blit(self.text_SAP, self.SAP_rect)
                pygame.draw.rect(self.image, Color.RED, self.image.get_rect(), 2)


        else:
            self.image.fill(self.color)
            self.image.blit(self.text, self.P_rect)
            #self.image.blit(self.text_AP, self.AP_rect)
            self.is_hovered = False
