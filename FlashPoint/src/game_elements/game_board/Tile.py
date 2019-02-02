import pygame

import src.constants.Color as Color
from src.game_elements.game_board.CharacterSprite import CharacterSprite
from src.UIComponents.Interactable import Interactable
from src.core.EventQueue import EventQueue


class Tile(Interactable):

    def __init__(self, image: pygame.Surface, x: int, y: int, x_offset: int, y_offset: int):
        """Create a tile, not sure what the sprite size should be..."""
        self.index = 0
        self.sprite_grp = pygame.sprite.Group()
        self.image = image
        self._backup_image = image.copy()
        super().__init__(self.image.get_rect())
        self.rect = self.image.get_rect().move(x_offset, y_offset)
        self.mouse_rect = pygame.Rect(self.rect).move(x, y)
        self.is_hovered = False
        self._mouse_pos = (0, 0)  # For keeping track of previous location.
        self.is_scrolling = False

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

    def enable(self):
        """
        Enables the event hook
        :return:
        """
        self._is_enabled = True

    def disable(self):
        """
        Disables the event hook
        :return:
        """
        self._is_enabled = False

    def _highlight(self):
        if self.hover() and self._is_enabled:
            if not self.is_hovered:
                self.is_hovered = True
                self.image = self._backup_image.copy()
                self.image.fill(Color.YELLOW)
        else:
            self.image = self._backup_image
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

    def remove_sprite_character(self, some_character):
        for sprite in self.sprite_grp:
            if isinstance(sprite, CharacterSprite) and sprite == some_character:
                # Takes care of not taking out other characters as well
                self.sprite_grp.remove(some_character)

    def find_character(self):
        for sprite in self.sprite_grp:
            if isinstance(sprite, CharacterSprite):
                return sprite

    def draw(self, screen: pygame.Surface):
        self._highlight()
        self.sprite_grp.draw(self.image)
        screen.blit(self.image, self.rect)

    def update(self, event_queue: EventQueue):
        self.sprite_grp.update(event_queue)
        self._scroll()


