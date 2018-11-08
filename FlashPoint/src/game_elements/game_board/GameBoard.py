import pygame

from src.game_elements.game_board.Grid import Grid


class GameBoard(pygame.sprite.Group):
    """Wrapper class for the Grid class. Contains methods specific for user interfacing."""
    def __init__(self, *sprites: pygame.sprite.Sprite, screen=None):
        super().__init__(*sprites)
        self._grid = Grid(screen=screen)
        self.add(self._grid)

    def _zoom(self):
        pass

    def _scroll(self):
        pass

    def draw(self, screen: pygame.Surface):
        self._grid.draw(screen)

    def update(self):
        # middle mouse pressed
        if pygame.mouse.get_pressed()[1]:
            self._scroll()

        self._zoom()
        self._scroll()

