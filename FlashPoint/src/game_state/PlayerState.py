import pygame

import src.constants.Color as Color



class PlayerState(pygame.sprite.Sprite):

    def __init__(self,x: int, y: int, size: int=32):
        super().__init__()
        self.image = pygame.Surface([size, size*2])
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.is_hovered = False
        self._render()


    def _render(self):

        self.image.fill(Color.GREY, self.rect)  # eventually this will be an actual tile image.


    def check_mouse_over(self):
        mouse = pygame.mouse.get_pos()
        rect = self.rect
        x_max = rect.x + rect.w
        x_min = rect.x
        y_max = rect.y + rect.h
        y_min = rect.y
        return x_max > mouse[0] > x_min and y_max > mouse[1] > y_min



    def update(self):
        if self.check_mouse_over():
            if not self.is_hovered:
                self.is_hovered = True
                self.image.fill(Color.CYAN)
        else:
            self.image.fill(Color.BLUE)
            self.is_hovered = False
