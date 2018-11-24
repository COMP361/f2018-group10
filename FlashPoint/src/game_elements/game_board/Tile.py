import pygame

import src.constants.Color as Color


class Tile(pygame.sprite.Sprite):

    def __init__(self, x: int, y: int, size: int=64):
        """Create a tile, not sure what the sprite size should be..."""
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.is_hovered = False

        self._render()
        self._mouse_pos = (0, 0)     # For keeping track of previous location.
        self.is_scrolling = False

    def _render(self):
        """Eventually this might have some randomization logic? Dunno how we'll generate boards :( """
        self.image.fill(Color.GREY, self.rect)  # eventually this will be an actual tile image.

    def _check_mouse_over(self):
        mouse = pygame.mouse.get_pos()
        rect = self.rect
        x_max = rect.x + rect.w
        x_min = rect.x
        y_max = rect.y + rect.h
        y_min = rect.y
        return x_max > mouse[0] > x_min and y_max > mouse[1] > y_min

    def _highlight(self):
        if self._check_mouse_over():
            if not self.is_hovered:
                self.is_hovered = True
                self.image.fill(Color.YELLOW)
        else:
            self.image.fill(Color.GREY)
            self.is_hovered = False

    def _scroll(self):
        """Move this Sprite in the direction of the scroll."""
        current_mouse_pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[2]             # right click
        movement = (current_mouse_pos[0] - self._mouse_pos[0], current_mouse_pos[1] - self._mouse_pos[1])
        if pressed:
            print("Clicked")
            print(f"{self.groups()[0].rect.bottom}, {self.groups()[0].rect.top}")
            print(current_mouse_pos)
            if (self.groups()[0].rect.left < current_mouse_pos[0] < self.groups()[0].rect.right
                    and self.groups()[0].rect.top < current_mouse_pos[1] < self.groups()[0].rect.bottom):
                print("Scrolling")
                self.rect.move_ip(movement)
        self._mouse_pos = current_mouse_pos

    def update(self):
        self._scroll()
        self._highlight()
