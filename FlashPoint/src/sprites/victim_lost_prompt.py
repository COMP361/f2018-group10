import pygame
import src.constants.color as Color
from src.core.event_queue import EventQueue
from src.constants.media_constants import WOOD, FRAME


class VictimLostPrompt(object):


    def __init__(self):

        self.image = pygame.Surface([400, 100])
        self.rect = self.image.get_rect()
        self.rect.move_ip(480, 0)
        self.bg = pygame.image.load(WOOD)

        self.frame = pygame.image.load(FRAME)
        self.frame = pygame.transform.scale(self.frame,(400,100))
        self.message = f"A victim has been lost"
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
            self.image.blit(self.text, self.text.get_rect().move((72,28)))
            self.image.blit(self.frame, self.image.get_rect())
            screen.blit(self.image,self.rect)
