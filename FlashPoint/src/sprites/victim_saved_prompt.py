import pygame
import src.constants.color as Color
from src.core.event_queue import EventQueue


class VictimSavedPrompt(object):

    def __init__(self):

        self.image = pygame.Surface([400, 100])
        self.rect = self.image.get_rect()
        self.rect.move_ip(480, 30)
        self.bg = pygame.image.load('src/media/GameHud/wood2.png')

        self.frame = pygame.image.load('src/media/GameHud/frame.png')
        self.frame = pygame.transform.scale(self.frame,(400,100))
        self.message = f"A victim has been saved"
        self.font = pygame.font.SysFont('Agency FB', 30)
        self.text = self.font.render(self.message, True, Color.GREEN2)
        self.text_rect = self.text.get_rect()
        self.text_rect.move_ip(480, 0)

        self.enabled = False


    def update(self,event_queue:EventQueue):
        self.image.update(event_queue)


    def draw(self,screen):
        if self.enabled:
            self.image.blit(self.bg, self.image.get_rect())
            self.image.blit(self.text, self.text.get_rect().move((75,28)))
            self.image.blit(self.frame, self.image.get_rect())

            screen.blit(self.image,self.rect)
