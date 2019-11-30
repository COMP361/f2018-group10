import pygame
import time
from src.core.event_queue import EventQueue
from src.constants.media_constants import TIMEBAR_WOOD


class TimeBar(pygame.sprite.Sprite):

    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface([1280, 30])
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

    def update(self, event_queue: EventQueue):
        wood = pygame.image.load(TIMEBAR_WOOD)
        wood = pygame.transform.scale(wood, (1280, 30))
        self.image.blit(wood, self.rect)

        time_obj = time.time()
        time_str = str(time_obj)
        show_time = pygame.font.SysFont('Arial', 30)
        text = show_time.render(time_str, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.move_ip(500, 0)
        self.image.blit(text, text_rect)
