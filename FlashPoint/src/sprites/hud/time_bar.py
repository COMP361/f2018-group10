import pygame
from datetime import datetime
import src.constants.color as Color
from src.core.event_queue import EventQueue


class TimeBar(pygame.sprite.Sprite):

    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface([1280, 30])
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self._start_time = datetime.now()
        wood = pygame.image.load('src/media/GameHud/wood1.png')
        self.wood = pygame.transform.scale(wood, (1280, 30))
        menu = pygame.image.load('src/media/GameHud/menu.png')
        self.menu = pygame.transform.scale(menu, (30, 30))

    def update(self, event_queue: EventQueue):
        self.image.blit(self.wood, self.rect)

        self.image.blit(self.menu, self.rect)

        time_int = int(abs((datetime.now() - self._start_time).total_seconds()))
        time_str = "TOTAL TIME: " + f"{int(time_int / 60):02d}:{(time_int % 60):02d}"
        show_time = pygame.font.SysFont('Agency FB', 28)
        text = show_time.render(time_str, True, Color.GREEN2)
        text_rect = text.get_rect()
        text_rect.move_ip(1135, -3)
        self.image.blit(text, text_rect)
