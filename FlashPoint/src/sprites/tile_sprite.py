from typing import Tuple, List

import pygame

import src.constants.color as Color
from src.UIComponents.file_importer import FileImporter
from src.UIComponents.interactable import Interactable
from src.UIComponents.rect_button import RectButton
from src.UIComponents.text import Text
from src.constants.media_constants import WATER, EXPLOSION
from src.constants.state_enums import SpaceStatusEnum
from src.core.event_queue import EventQueue
from src.models.game_state_model import GameStateModel
from src.models.model import Model
from src.observers.tile_observer import TileObserver


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

        self.counter = 80

        self.explosion = False
        self.explosion_image = image.copy()
        self.explosion_image.blit(pygame.image.load(EXPLOSION), (0, 0, 128, 128))
        self.explosion_image.get_rect().move_ip(x_offset,y_offset)

        self.fire_deck_gun = False
        self.fire_deck_gun_image = image.copy()
        self.fire_deck_gun_image.blit(pygame.transform.scale(pygame.image.load(WATER),(128,128)), (0, 0, 128, 128))
        self.fire_deck_gun_image.get_rect().move_ip(x_offset, y_offset)

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
        self.identify_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                          Text(pygame.font.SysFont('Agency FB', 15), "Identify", Color.GREEN2))
        pygame.draw.rect(self.identify_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

        self.move_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                      Text(pygame.font.SysFont('Agency FB', 15), "Move Here", Color.GREEN2))
        pygame.draw.rect(self.move_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

        self.extinguish_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                            Text(pygame.font.SysFont('Agency FB', 15), "Extinguish", Color.GREEN2))
        pygame.draw.rect(self.extinguish_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

        self.pickup_victim_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                               Text(pygame.font.SysFont('Agency FB', 15), "Carry Victim", Color.GREEN2))
        pygame.draw.rect(self.pickup_victim_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

        self.drop_victim_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                             Text(pygame.font.SysFont('Agency FB', 15), "Leave Victim", Color.GREEN2))
        pygame.draw.rect(self.drop_victim_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

        self.lead_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                               Text(pygame.font.SysFont('Agency FB', 15), "Lead Victim", Color.GREEN2))

        pygame.draw.rect(self.lead_button.image,Color.YELLOW,[0, 0, 100, 25],3)

        self.change_crew_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                             Text(pygame.font.SysFont('Agency FB', 15), "Change Crew", Color.GREEN2))
        pygame.draw.rect(self.change_crew_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

        self.stop_lead_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                             Text(pygame.font.SysFont('Agency FB', 15), "Leave Victim", Color.GREEN2))

        pygame.draw.rect(self.stop_lead_button.image,Color.YELLOW,[0, 0, 100, 25],3)

        self.drive_ambulance_here_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                                      Text(pygame.font.SysFont('Agency FB', 15), "Drive Ambulance Here",
                                                           Color.GREEN2))

        pygame.draw.rect(self.drive_ambulance_here_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

        self.drive_engine_here_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                                   Text(pygame.font.SysFont('Agency FB', 15), "Drive Engine Here",
                                                        Color.GREEN2))

        pygame.draw.rect(self.drive_engine_here_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

        self.ride_vehicle_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                              Text(pygame.font.SysFont('Agency FB', 15), "Ride Vehicle", Color.GREEN2))

        pygame.draw.rect(self.ride_vehicle_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

        self.remove_hazmat_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                        Text(pygame.font.SysFont('Agency FB', 15), "Remove Hazmat", Color.GREEN2))

        pygame.draw.rect(self.remove_hazmat_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

        self.dismount_vehicle_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                                  Text(pygame.font.SysFont('Agency FB', 15), "Dismount Vehicle",
                                                       Color.GREEN2))

        pygame.draw.rect(self.dismount_vehicle_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

        self.fire_deck_gun_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                               Text(pygame.font.SysFont('Agency FB', 15), "Fire Deck Gun", Color.GREEN2))

        pygame.draw.rect(self.fire_deck_gun_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

        self.resuscitate_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                              Text(pygame.font.SysFont('Agency FB', 15), "Resuscitate", Color.GREEN2))

        pygame.draw.rect(self.resuscitate_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

        self.command_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                         Text(pygame.font.SysFont('Agency FB', 15), "Command", Color.GREEN2))

        pygame.draw.rect(self.command_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

        self.pickup_hazmat_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                               Text(pygame.font.SysFont('Agency FB', 15), "Pickup Hazmat", Color.GREEN2))

        pygame.draw.rect(self.pickup_hazmat_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

        self.drop_hazmat_button = RectButton(self.rect.x, self.rect.y, 100, 25, Color.WOOD, 0,
                                               Text(pygame.font.SysFont('Agency FB', 15), "Drop Hazmat", Color.GREEN2))

        pygame.draw.rect(self.drop_hazmat_button.image, Color.YELLOW, [0, 0, 100, 25], 3)

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
        self.resuscitate_button.disable()
        self.lead_button.disable()
        self.stop_lead_button.disable()
        self.fire_deck_gun_button.disable()
        self.change_crew_button.disable()

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
        self.resuscitate_button.on_click(None)
        self.lead_button.on_click(None)
        self.stop_lead_button.on_click(None)
        self.fire_deck_gun_button.on_click(None)
        self.change_crew_button.on_click(None)

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

        if self.explosion:
            screen.blit(self.explosion_image, self.rect)
            self.counter -= 1
            if self.counter == 0:
                self.explosion = False
                self.counter = 80
                screen.blit(self.image, self.rect)
        elif self.fire_deck_gun:
            screen.blit(self.fire_deck_gun_image,self.rect)
            self.counter -= 1
            if self.counter == 0:
                self.fire_deck_gun = False
                self.counter = 80
                screen.blit(self.image, self.rect)

        else:
            self._draw_hightlight()
            screen.blit(self.image, self.rect)

    def draw_menu(self, screen: pygame.Surface):
        offset = 0
        inc = 30
        if self.move_button.enabled:
            self.draw_btn(self.move_button, offset, screen)
            offset += inc

        if self.extinguish_button.enabled:
            self.draw_btn(self.extinguish_button, offset, screen)
            offset += inc

        if self.pickup_victim_button.enabled:
            self.draw_btn(self.pickup_victim_button, offset, screen)
            offset += inc
        elif self.drop_victim_button.enabled:
            self.draw_btn(self.drop_victim_button, offset, screen)
            offset += inc

        if self.drive_ambulance_here_button.enabled:
            self.draw_btn(self.drive_ambulance_here_button, offset, screen)
            offset += inc

        if self.drive_engine_here_button.enabled:
            self.draw_btn(self.drive_engine_here_button, offset, screen)
            offset += inc

        if self.identify_button.enabled:
            self.draw_btn(self.identify_button, offset, screen)
            offset += inc

        if self.ride_vehicle_button.enabled:
            self.draw_btn(self.ride_vehicle_button, offset, screen)
            offset += inc

        if self.dismount_vehicle_button.enabled:
            self.draw_btn(self.dismount_vehicle_button, offset, screen)
            offset += inc

        if self.remove_hazmat_button.enabled:
            self.draw_btn(self.remove_hazmat_button, offset, screen)
            offset += inc

        if self.pickup_hazmat_button.enabled:
            self.draw_btn(self.pickup_hazmat_button, offset, screen)
            offset += inc

        elif self.drop_hazmat_button.enabled:
            self.draw_btn(self.drop_hazmat_button, offset, screen)
            offset += inc

        if self.resuscitate_button.enabled:
            self.draw_btn(self.resuscitate_button, offset, screen)
            offset += inc

        if self.fire_deck_gun_button.enabled:
            screen.blit(self.fire_deck_gun_button.image, self.fire_deck_gun_button.rect)
            self.fire_deck_gun_button.rect.x = self.rect.x
            self.fire_deck_gun_button.rect.y = self.rect.y + offset
            offset += inc

        if self.change_crew_button.enabled:
            screen.blit(self.change_crew_button.image, self.change_crew_button.rect)
            self.change_crew_button.rect.x = self.rect.x
            self.change_crew_button.rect.y = self.rect.y + offset
            offset += inc

        if self.command_button.enabled:
            self.draw_btn(self.command_button, offset, screen)
            offset += inc

        if self.lead_button.enabled:
            self.draw_btn(self.lead_button, offset, screen)
            offset += inc

        if self.stop_lead_button.enabled:
            self.draw_btn(self.stop_lead_button, offset, screen)
            offset += inc

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
        self.resuscitate_button.update(event_queue)
        self.fire_deck_gun_button.update(event_queue)
        self.lead_button.update(event_queue)
        self.stop_lead_button.update(event_queue)
        self.change_crew_button.update(event_queue)

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
