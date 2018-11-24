import pygame

import src.constants.MainConstants as MainConst
from src.game_elements.game_board.Grid import Grid


class GameBoard(object):
    """Wrapper class for the Grid class. Contains methods specific for user interfacing."""
    def __init__(self,
                 width: int=MainConst.SCREEN_RESOLUTION[0]*2/3,
                 height: int=MainConst.SCREEN_RESOLUTION[1]*0.8):
        self.image = pygame.Surface((width, height))
        self.grid = Grid(screen=self.image)
        self.rect = self.image.get_rect().move(
            (MainConst.SCREEN_RESOLUTION[0] - width, MainConst.SCREEN_RESOLUTION[1] - height))

        self.is_scrolling = -1                              # Need 2 clicks to become 1 (True)
        self.mouse_pos = (0, 0)                             # Store the mouse pos to determine direction

    # def _scroll(self):
    #     current_mouse_pos = pygame.mouse.get_pos()
    #     pressed = pygame.mouse.get_pressed()[0]             # left click
    #     movement = (current_mouse_pos[0] - self.mouse_pos[0], current_mouse_pos[1] - self.mouse_pos[1])
    #
    #     if pressed:
    #         self.is_scrolling += 1
    #         if self.is_scrolling >= 1:
    #             # set motion direction
    #             print(f"scrolling: {movement[0]} {movement[1]}")
    #
    #             # Move all the sprites:
    #             for sprite in self.grid.sprites():
    #                 if (self.rect.left < self.grid.grid[0][0].rect.left < self.rect.right
    #                         and self.rect.bottom < self.grid.grid[0][0].rect.top < self.rect.top):
    #                     sprite.rect.move_ip(movement)
    #     else:
    #         self.is_scrolling = -1
    #
    #     self.mouse_pos = current_mouse_pos

    def draw(self, screen: pygame.display):
        screen.blit(self.image, self.rect)

    def update(self):
        # self._scroll()
        self.grid.update()
