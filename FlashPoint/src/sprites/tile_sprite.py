import pygame
from src.UIComponents.file_importer import FileImporter
from src.models.game_state_model import GameStateModel
from src.constants.state_enums import SpaceStatusEnum
from src.observers.observer import Observer
from src.UIComponents.interactable import Interactable
from src.core.event_queue import EventQueue


class TileSprite(Interactable, Observer):
    """Graphical representation of a Tile and controls."""

    def __init__(self, image: pygame.Surface, fire_image: pygame.Surface,
                 smoke_image: pygame.Surface, x, y, x_offset, y_offset, row, column):
        self.index = 0
        self.sprite_grp = pygame.sprite.Group()
        self.image = image

        self.row = row
        self.column = column

        self._fire_image = fire_image
        self._smoke_image = smoke_image
        self._non_highlight_image = image.copy()
        self._blank_image = image.copy()

        # Initialize if place is Fire, Smoke or Safe
        status = GameStateModel.instance().game_board.get_tile_at(row, column).space_status
        self.tile_status_changed(status)

        Interactable.__init__(self, self.image.get_rect())
        self.rect = self.image.get_rect().move(x_offset, y_offset)
        self.mouse_rect = pygame.Rect(self.rect).move(x, y)
        self._is_hovered = False
        self._mouse_pos = (0, 0)  # For keeping track of previous location.
        self.is_scrolling = False
        self._is_highlighted = False

    @property
    def highlighted(self) -> bool:
        return self._is_highlighted and self._is_enabled

    @highlighted.setter
    def highlighted(self, value: bool):
        self._is_highlighted = value

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

    def _apply_highlight(self):
        if self.hover() and self._is_enabled:
            if not self._is_hovered:
                self._is_hovered = True
                hover = pygame.Surface((self._non_highlight_image.get_width(), self._non_highlight_image.get_height()),
                                       pygame.SRCALPHA)
                hover.fill((255, 255, 0, 128))
                self.image.blit(hover, (0, 0))
        else:
            self.image.blit(self._non_highlight_image, (0, 0))
            self._is_hovered = False

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

    def draw(self, screen: pygame.Surface):
        self._apply_highlight()
        self.sprite_grp.draw(self.image)
        
        screen.blit(self.image, self.rect)

    def update(self, event_queue: EventQueue):
        self.sprite_grp.update(event_queue)
        self._scroll()

    def tile_status_changed(self, status: SpaceStatusEnum):
        new_surf = pygame.Surface([self._non_highlight_image.get_width(), self._non_highlight_image.get_height()])
        self._non_highlight_image = self._blank_image.copy()

        new_surf = pygame.Surface.convert_alpha(new_surf)
        new_surf.fill((0, 0, 0, 0), None, pygame.BLEND_RGBA_MULT)

        if status == SpaceStatusEnum.FIRE:
            image_file = FileImporter.import_image("media/All Markers/fire.png")
            new_surf.blit(image_file, (0, 0))
        elif status == SpaceStatusEnum.SMOKE:
            image_file = FileImporter.import_image("media/All Markers/smoke.png")
            new_surf.blit(image_file, (0, 0))

        self._non_highlight_image.blit(new_surf, (0, 0))
