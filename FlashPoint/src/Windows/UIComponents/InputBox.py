import pygame as pg

import src.constants.Color as Color
from src.core.EventQueue import EventQueue
from src.constants.Fonts import TEXT_BOX_FONT_SIZE


class InputBox(pg.sprite.Sprite):

    def __init__(self, *sprites, x=0, y=0, w=0, h=0, text=''):
        super().__init__(*sprites)
        self.COLOR_INACTIVE = Color.BLACK
        self.COLOR_ACTIVE = Color.WHITE
        self.FONT = pg.font.Font(None, TEXT_BOX_FONT_SIZE)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.image = pg.Surface((w, h))
        self.rect = self.image.get_rect()
        self.active = False
        self.message = ''
        self.rect = pg.draw.rect(self.image, self.color, self.rect, 2)
        self.rect.move_ip(x, y)
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
                    self.message = self.text
                    self.text = ''

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
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)
