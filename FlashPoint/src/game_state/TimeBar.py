import pygame
import datetime
import time
import src.constants.Color as Color

class TimeBar(pygame.sprite.Sprite):

    def __init__(self, x: int, y: int) :
        super().__init__()
        self.image = pygame.Surface([1280, 50])
        #self.gen_time = time.localtime(time.time())
        #self.dt_obj = datetime(2018,11,26,15,55,47)
        #self.dt_obj = datetime.datetime.now()
        #self.date_str = self.dt_obj.strftime("%Y-%m-%d %H:%M:%S")
        #self.show_time = pygame.font.SysFont('Arial', 30)
        #self.text = self.show_time.render(self.date_str, True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)






    def update(self):
        self.image.fill(Color.GREEN)
        dt_obj = datetime.datetime.now()
        date_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
        show_time = pygame.font.SysFont('Arial', 30)
        text = show_time.render(date_str, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.move_ip(500,0)
        self.image.blit(text,text_rect)
        #pygame.draw.rect(self.image, Color.RED, self.image.get_rect(), 2)


