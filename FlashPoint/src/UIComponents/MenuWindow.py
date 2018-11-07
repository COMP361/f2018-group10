from typing import Tuple, Optional

import pygame

from src.UIComponents.Components import Components
from src.UIComponents.RectButton import RectButton


class MenuWindow(pygame.sprite.Sprite):

    SPACE_BETWEEN = 5

    """
    Popup Menu class
    """
    def __init__(self,
                 width: int,
                 height: Optional[int],
                 def_position: Optional[Tuple[int, int]],
                 color: Tuple[int, int, int, int] = (175, 175, 175, 0.5),
                 padding: int=5):
        pygame.sprite.Sprite.__init__(self)
        self.def_width = width
        self.def_height = None
        self.def_position = None
        self.color = color
        self.padding = padding
        self.children = Tuple[Components]
        self.is_open = False
        self.screen_copy = None

        self.x = 0
        self.y = 0
        if height:
            self.height = height
        if def_position:
            self.def_position = def_position

    def toggle(self):
        main_display = pygame.display.get_surface()

        if self.is_open:
            main_display.fill((0, 0, 0, 0))
            main_display.blit(self.screen_copy)
            self.is_open = False
        else:
            # copy the display and store in memory (so that we can redraw it)
            self.screen_copy = main_display.copy()
            # dim the main display
            pygame.draw.rect(main_display, (0, 0, 0, 0.5), main_display.get_rect())

            # calculate the window's size
            width = self.def_width
            if self.def_height is None:
                height = self.padding * 2
                for child in self.children:
                    height += child.get_height() + self.SPACE_BETWEEN
            else:
                height = self.def_height

            if self.def_position is None:
                self.x = main_display.get_width()/2 - width/2
                self.y = main_display.get_height()/2 - height/2
            else:
                self.x = self.def_position[0]
                self.y = self.def_position[1]

            # draw the menu on screen
            menu_window = pygame.rect.Rect(x, y, width, height)
            pygame.draw.rect(main_display, self.color, menu_window)

            self.is_open = True

    # TODO: Finish the class. Not sure if I need to call update here or not...

    def _render(self):
        x = self.x + self.padding
        y = self.y + self.padding
        for child in self.children:
            child.change_pos(x, y)
            y += child.get_height + self.SPACE_BETWEEN

    def add_child(self):
        new_btn = RectButton()
