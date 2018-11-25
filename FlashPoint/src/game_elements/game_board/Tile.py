import pygame

import src.constants.Color as Color


class Tile(pygame.sprite.Sprite):

    def __init__(self, x: int, y: int, x_offset: int, y_offset: int, size: int=128):
        """Create a tile, not sure what the sprite size should be..."""
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.rect = self.image.get_rect().move(x_offset, y_offset)
        self.mouse_rect = pygame.Rect(self.rect).move(x, y)
        self.is_hovered = False

        self._render()
        self._mouse_pos = (0, 0)     # For keeping track of previous location.
        self.is_scrolling = False

    def _render(self):
        """Eventually this might have some randomization logic? Dunno how we'll generate boards :( """
        self.image.fill(Color.GREY, self.rect)  # eventually this will be an actual tile image.

    def _check_mouse_over(self):
        mouse = pygame.mouse.get_pos()
        rect = self.mouse_rect
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
            grid = self.groups()[0]
            if (grid.rect.left < current_mouse_pos[0] < grid.rect.right
                    and grid.rect.top < current_mouse_pos[1] < grid.rect.bottom):

                self.rect.move_ip(movement)
                self.mouse_rect.move_ip(movement)
        self._mouse_pos = current_mouse_pos

    def update(self):
        self._scroll()
        self._highlight()
