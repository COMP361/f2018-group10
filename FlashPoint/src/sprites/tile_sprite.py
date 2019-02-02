import pygame

<<<<<<< HEAD:FlashPoint/src/sprites/TileSprite.py
from src.UIComponents.Interactable import Interactable
from src.constants import color
from src.core.event_queue import EventQueue
from src.models.game_board import TileModel
=======
from src.UIComponents.interactable import Interactable
from src.constants import Color
from src.core.EventQueue import EventQueue
from src.models.game_board import tile_model
>>>>>>> GSD-Alek:FlashPoint/src/sprites/tile_sprite.py


class TileSprite(Interactable):
    """Graphical representation of a Tile and controls."""
    def __init__(self, grid_x_pos: int, grid_y_pos: int, x_offset, y_offset, tile_model: tile_model, size: int = 128):
        self.tile_model = tile_model

        self.image = pygame.Surface([size, size])
        super().__init__(self.image.get_rect())
        self.rect = self.image.get_rect().move(x_offset, y_offset)
        self.mouse_rect = pygame.Rect(self.rect).move(grid_x_pos, grid_y_pos)

        self._mouse_pos = (0, 0)  # For keeping track of previous location.
        self.is_hovered = False
        self.is_scrolling = False

        self._render()

    def _render(self):
        """Eventually this might have some randomization logic? Dunno how we'll generate boards :( """
        self.image.fill(color.GREY, self.rect)  # eventually this will be an actual tile image.

    def _highlight(self):
        if self.hover() and self._is_enabled:
            if not self.is_hovered:
                self.is_hovered = True
                self.image.fill(color.YELLOW)
        else:
            self.image.fill(color.GREY)
            self.is_hovered = False

    def _scroll(self):
        """Move this Sprite in the direction of the scroll."""
        current_mouse_pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[2]  # right click
        movement = (current_mouse_pos[0] - self._mouse_pos[0], current_mouse_pos[1] - self._mouse_pos[1])
        if pressed:
            grid = self.groups()[0]
            if (grid.rect.left < current_mouse_pos[0] < grid.rect.right
                    and grid.rect.top < current_mouse_pos[1] < grid.rect.bottom):
                self.rect.move_ip(movement)
                self.mouse_rect.move_ip(movement)
        self._mouse_pos = current_mouse_pos

    # TODO Alek please make this functionality a permanent solution
    # def remove_sprite_character(self, some_character):
    #     for sprite in self.tile_model.game_unit_sprites:
    #         if isinstance(sprite, CharacterSprite) and sprite == some_character:
    #             # Takes care of not taking out other characters as well
    #             self.tile_model.game_unit_sprites.remove(some_character)
    #
    # def find_character(self):
    #     for sprite in self.tile_model.game_unit_sprites:
    #         if isinstance(sprite, CharacterSprite):
    #             return sprite

    def hover(self):
        if self._is_enabled:
            mouse = pygame.mouse.get_pos()
            rect = self.rect
            x_max = rect.x + rect.w
            x_min = rect.x
            y_max = rect.y + rect.h
            y_min = rect.y
            return x_max > mouse[0] > x_min and y_max > mouse[1] > y_min
        else:
            return False

    def draw(self, screen: pygame.Surface):
        self._highlight()
        # self.sprite_grp.draw(self.image)
        screen.blit(self.image, self.rect)

    def update(self, event_queue: EventQueue):
        # self.sprite_grp.update(event_queue)
        self._scroll()
