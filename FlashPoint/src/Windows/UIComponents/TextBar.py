import pygame as pg
from src.core.EventQueue import EventQueue


class InputBox(pg.sprite.Sprite):

    def __init__(self, *group, x=0, y=0, w=0, h=0, text=''):
        super().__init__(*group)
        self.COLOR_INACTIVE = pg.Color('lightskyblue3')
        self.COLOR_ACTIVE = pg.Color('dodgerblue2')
        self.FONT = pg.font.Font(None, 32)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.image = pg.Surface((w, h))
        self.rect = self.image.get_rect()
        self.active = False
        self.rect = pg.draw.rect(self.image, self.color, self.rect, 2)
        self.rect.move_ip(x,y)
        self.image.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.image = self.FONT.render(self.text, True, self.color)

    def update(self, event_queue: EventQueue):
        for event in event_queue:
            self.handle_event(event)
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width
