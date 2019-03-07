import pygame
import time
from datetime import datetime
import src.constants.color as Color
from src.core.event_queue import EventQueue


class TimeBar(pygame.sprite.Sprite):

    # def __init__(self, x: int, y: int):
    #     super().__init__()
    #     self.image = pygame.Surface([1280, 30])
    #     self.rect = self.image.get_rect()
    #     self.rect.move_ip(x, y)
    #
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface([1280, 30])
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self._start_time = datetime.now()
        wood = pygame.image.load('media/GameHud/wood1.png')
        self.wood = pygame.transform.scale(wood, (1280, 30))
        menu = pygame.image.load('media/GameHud/menu.png')
        self.menu = pygame.transform.scale(menu, (30, 30))

    # def update(self,event_queue: EventQueue):
    #     self.image.fill(Color.GREEN)
    #     dt_obj = datetime.datetime.now()
    #     date_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    #     show_time = pygame.font.SysFont('Arial', 30)
    #     text = show_time.render(date_str, True, (0, 0, 0))
    #     text_rect = text.get_rect()
    #     text_rect.move_ip(500,0)
    #     self.image.blit(text,text_rect)
    #     #pygame.draw.rect(self.image, Color.RED, self.image.get_rect(), 2)

    def update(self,event_queue: EventQueue):

        self.image.blit(self.wood,self.rect)

        self.image.blit(self.menu,self.rect)

        # dt_obj = datetime.datetime.now()
        # date_str = dt_obj.strftime("%M:%S")
        # show_time = pygame.font.SysFont('Arial', 30)
        # text = show_time.render(date_str, True, (0, 0, 0))

        time_int = int(abs((datetime.now() - self._start_time).total_seconds()))
        time_str = "TOTAL TIME: "+f"{int(time_int/60):02d}:{(time_int % 60):02d}"
        show_time = pygame.font.SysFont('Agency FB', 28)
        text = show_time.render(time_str, True, Color.GREEN2)
        text_rect = text.get_rect()
        text_rect.move_ip(1135,-3)
        self.image.blit(text,text_rect)
