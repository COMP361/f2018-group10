from typing import Tuple, List

import pygame
from src.UIComponents.file_importer import FileImporter
from src.UIComponents.rect_button import RectButton
from src.models.game_state_model import GameStateModel
from src.constants.state_enums import SpaceStatusEnum
from src.UIComponents.interactable import Interactable
from src.core.event_queue import EventQueue
from src.models.model import Model
from src.observers.tile_observer import TileObserver
import src.constants.color as Color
from src.UIComponents.text import Text


class TileSprite(Interactable, TileObserver):
    """Graphical representation of a Tile and controls."""

    def __init__(self, image: pygame.Surface, fire_image: pygame.Surface,
                 smoke_image: pygame.Surface, x, y, x_offset, y_offset, row, column):
        self.index = 0
        self.sprite_grp = pygame.sprite.Group()
        self.image = image
        self._highlight_color = None
        self.row = row
        self.column = column

        self._fire_image = fire_image
        self._smoke_image = smoke_image
        self._non_highlight_image = image.copy()
        self._blank_image = image.copy()

        # Initialize if place is Fire, Smoke or Safe
        tile = GameStateModel.instance().game_board.get_tile_at(row, column)
        status = tile.space_status
        is_hotspot = tile.is_hotspot
        self.tile_status_changed(status, is_hotspot)

        Interactable.__init__(self, self.image.get_rect())
        self.rect = self.image.get_rect().move(x_offset, y_offset)
        self.mouse_rect = pygame.Rect(self.rect).move(x, y)
        self._is_hovered = False
        self._mouse_pos = (0, 0)  # For keeping track of previous location.
        self.is_scrolling = False

        # ------- POP-UP MENU -------- #
        self.identify_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.BLACK, 0,
                                       Text(pygame.font.SysFont('Arial', 20), "Identify", Color.ORANGE))

        self.move_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.BLACK, 0,
                                      Text(pygame.font.SysFont('Arial', 15), "Move Here", Color.ORANGE))
        self.extinguish_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.BLACK, 0,
                                            Text(pygame.font.SysFont('Arial', 15), "Extinguish", Color.ORANGE))
        self.pickup_victim_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.BLACK, 0,
                                               Text(pygame.font.SysFont('Arial', 15), "Pickup Victim", Color.ORANGE))
        self.drop_victim_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.BLACK, 0,
                                             Text(pygame.font.SysFont('Arial', 15), "Drop Victim", Color.ORANGE))

        self.drive_ambulance_here_button = RectButton(self.rect.x, self.rect.y, 120, 25, Color.BLACK, 0,
                                             Text(pygame.font.SysFont('Arial', 15), "Drive Ambulance Here", Color.ORANGE))

        self.drive_engine_here_button = RectButton(self.rect.x, self.rect.y, 120, 25, Color.BLACK, 0,
                                                      Text(pygame.font.SysFont('Arial', 15), "Drive Engine Here",
                                                           Color.ORANGE))
        self.ride_vehicle_button = RectButton(self.rect.x, self.rect.y, 120, 25, Color.BLACK, 0,
                                              Text(pygame.font.SysFont('Arial', 15), "Ride Vehicle", Color.ORANGE))
        self.remove_hazmat_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.BLACK, 0,
                                               Text(pygame.font.SysFont('Arial', 20), "Remove Hazmat", Color.ORANGE))

        self.pickup_hazmat_button = RectButton(self.rect.x, self.rect.y, 100,25,Color.BLACK, 0,
                                               Text(pygame.font.SysFont('Arial', 20), "Pickup Hazmat", Color.ORANGE))

        self.drop_hazmat_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.BLACK, 0,
                                               Text(pygame.font.SysFont('Arial', 20), "Drop Hazmat", Color.ORANGE))

        self.dismount_vehicle_button = RectButton(self.rect.x, self.rect.y, 120, 25, Color.BLACK, 0,
                                              Text(pygame.font.SysFont('Arial', 15), "Dismount Vehicle", Color.ORANGE))

        self.command_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.BLACK, 0,
                                         Text(pygame.font.SysFont('Arial', 20), "Command", Color.ORANGE))

        self.disable_all()

    def __str__(self):
        return f"TileSprite at: {self.row},{self.column}"

    def _draw_hightlight(self):
        self.image.blit(self._non_highlight_image, (0, 0))
        hover = pygame.Surface(
            (self._non_highlight_image.get_width(), self._non_highlight_image.get_height())).convert_alpha()
        if self._highlight_color:
            hover.fill(self._highlight_color)
            hover.set_alpha(10)
            self.image.blit(hover, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    @property
    def highlight_color(self):
        return self._highlight_color

    @highlight_color.setter
    def highlight_color(self, color: Tuple[int, int, int]):
        self._highlight_color = color

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

    def disable_all(self):
        # Disable all buttons
        self.identify_button.disable()
        self.move_button.disable()
        self.extinguish_button.disable()
        self.pickup_victim_button.disable()
        self.drop_victim_button.disable()
        self.drive_ambulance_here_button.disable()
        self.drive_engine_here_button.disable()
        self.ride_vehicle_button.disable()
        self.dismount_vehicle_button.disable()
        self.command_button.disable()
        self.remove_hazmat_button.disable()
        self.pickup_hazmat_button.disable()
        self.drop_hazmat_button.disable()

        # Important! Reset the on_clicks
        self.identify_button.on_click(None)
        self.move_button.on_click(None)
        self.extinguish_button.on_click(None)
        self.pickup_victim_button.on_click(None)
        self.drop_victim_button.on_click(None)
        self.drive_ambulance_here_button.on_click(None)
        self.drive_engine_here_button.on_click(None)
        self.ride_vehicle_button.on_click(None)
        self.dismount_vehicle_button.on_click(None)
        self.command_button.on_click(None)
        self.remove_hazmat_button.on_click(None)
        self.pickup_hazmat_button.on_click(None)
        self.drop_hazmat_button.on_click(None)

    def is_clicked(self):
        if not self.hover():
            return False

        for event in EventQueue.get_instance():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                return True
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
        self._draw_hightlight()
        screen.blit(self.image, self.rect)

    def draw_menu(self, screen: pygame.Surface):
        offset = 0

        if self.move_button.enabled:
            self.draw_btn(self.move_button, offset, screen)
            offset += 20

        if self.extinguish_button.enabled:
            self.draw_btn(self.extinguish_button, offset, screen)
            offset += 20

        if self.pickup_victim_button.enabled:
            self.draw_btn(self.pickup_victim_button, offset, screen)
            offset += 20
        elif self.drop_victim_button.enabled:
            self.draw_btn(self.drop_victim_button, offset, screen)
            offset += 20

        if self.drive_ambulance_here_button.enabled:
            self.draw_btn(self.drive_ambulance_here_button, offset, screen)
            offset += 20

        if self.drive_engine_here_button.enabled:
            self.draw_btn(self.drive_engine_here_button, offset, screen)
            offset += 20

        if self.identify_button.enabled:
            self.draw_btn(self.identify_button, offset, screen)
            offset += 20

        if self.ride_vehicle_button.enabled:
            self.draw_btn(self.ride_vehicle_button, offset, screen)
            offset += 20

        if self.dismount_vehicle_button.enabled:
            self.draw_btn(self.dismount_vehicle_button, offset, screen)
            offset += 20

        if self.remove_hazmat_button.enabled:
            self.draw_btn(self.remove_hazmat_button, offset, screen)
            offset += 20

        if self.pickup_hazmat_button.enabled:
            self.draw_btn(self.pickup_hazmat_button, offset, screen)
            offset += 20

        elif self.drop_hazmat_button.enabled:
            self.draw_btn(self.drop_hazmat_button, offset, screen)
            offset += 20

        if self.command_button.enabled:
            self.draw_btn(self.command_button, offset, screen)
            offset += 20

    def draw_btn(self, button: RectButton, offset: int, screen: pygame.Surface):
        screen.blit(button.image, button.rect)
        button.rect.x = self.rect.x
        button.rect.y = self.rect.y + offset

    def update(self, event_queue: EventQueue):
        self.sprite_grp.update(event_queue)

        self.drive_ambulance_here_button.update(event_queue)
        self.drop_victim_button.update(event_queue)
        self.extinguish_button.update(event_queue)
        self.pickup_victim_button.update(event_queue)
        self.move_button.update(event_queue)
        self.identify_button.update(event_queue)
        self.ride_vehicle_button.update(event_queue)
        self.dismount_vehicle_button.update(event_queue)
        self.drive_engine_here_button.update(event_queue)
        self.command_button.update(event_queue)
        self.remove_hazmat_button.update(event_queue)
        self.drop_hazmat_button.update(event_queue)
        self.pickup_hazmat_button.update(event_queue)

        self._scroll()
        if self.is_clicked():
            self.click()

    def tile_status_changed(self, status: SpaceStatusEnum, is_hotspot: bool):
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

        if is_hotspot:
            hs_img = FileImporter.import_image("media/all_markers/hot_spot.png")
            new_surf.blit(hs_img, (0, 0))

        self._non_highlight_image.blit(new_surf, (0, 0))

    def tile_assoc_models_changed(self, assoc_models: List[Model]):
        pass
