import pygame
import src.constants.color as Color
from src.core.event_queue import EventQueue


class VictimDead(pygame.sprite.Sprite):

    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface([227, 88])
        self.font_name = pygame.font.SysFont('Arial', 23)
        self.font_other = pygame.font.SysFont('Arial', 25)
        self.name = "Victims Lost: "
        self.current = str(2)
        self.max = str(4)
        self.slash = "/"
        self.text_name = self.font_name.render(self.name, True, (0, 0, 0))
        self.text_current = self.font_other.render(self.current, True, (0, 0, 0))
        self.text_slash = self.font_other.render(self.slash, True, (0, 0, 0))
        self.text_max = self.font_other.render(self.max, True, (0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.name_rect = self.text_name.get_rect()
        self.name_rect.move_ip(80, 10)
        self.current_rect = self.text_name.get_rect()
        self.current_rect.move_ip(80, 40)
        self.slash_rect = self.text_slash.get_rect()
        self.slash_rect.move_ip(90,40)
        self.max_rect = self.text_max.get_rect()
        self.max_rect.move_ip(100, 40)

    def update(self,event_queue: EventQueue):

        self.image.fill(Color.GREEN)
        self.image.blit(self.text_name, self.name_rect)
        self.image.blit(self.text_current, self.current_rect)
        self.image.blit(self.text_slash, self.slash_rect)
        self.image.blit(self.text_max, self.max_rect)

        pygame.draw.rect(self.image, Color.RED, self.image.get_rect(), 2)
