import pygame as pg

import src.constants.color as Color
from src.core.event_queue import EventQueue


class InputBox(pg.sprite.Sprite):

    def __init__(self, *sprites, x=0, y=0, w=0, h=0, fsize=25, text=''):
        super().__init__(*sprites)
        pg.key.set_repeat(300, 50)
        self.enter_enabled = True
        self.COLOR_INACTIVE = Color.BLACK
        self.COLOR_ACTIVE = Color.WHITE
        self.FONT = pg.font.SysFont("Agency FB", fsize)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.text_20 = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.image = pg.Surface((w, h))
        self.rect = self.image.get_rect()
        self.active = False
        self.message = ''
        self.bg = pg.Surface((w, h))
        self.bg.fill((64, 64, 64))
        self.rect2 = self.bg.get_rect()
        self.rect2.move_ip(x, y)
        self.rect = pg.draw.rect(self.image, self.color, self.rect, 2)
        self.rect.move_ip(x, y)
        self.image.blit(self.txt_surface, (self.rect.x + 5, self.rect.y))

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
                    if self.enter_enabled:
                        self.message = self.text
                        self.text = ''
                    else:
                        return
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    self.text += event.unicode

                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self, event_queue: EventQueue):
        for event in event_queue:
            self.handle_event(event)

        width = max(400, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen: pg.Surface):
        screen.blit(self.bg, self.rect2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y))
        pg.draw.rect(screen, self.color, self.rect, 2)

    def enable_enter(self):
        self.enter_enabled = True

    def disable_enter(self):
        self.enter_enabled = False
