from typing import Tuple, Optional

import pygame

from src.UIComponents.Components import Components


class MenuWindow(pygame.sprite.Sprite):
    """
    Popup Menu class
    """
    def __init__(self,
                 width: int,
                 height: Optional[int],
                 position: Optional[Tuple[int, int]],
                 padding: int=5):
        pygame.sprite.Sprite.__init__(self)
        self.def_width = width
        self.def_height = None
        self.position = None
        self.padding = padding
        self.children = Tuple[Components]
        self.isOpen = False
        if height:
            self.height = height
        if position:
            self.position = position

    def toggle(self):
        if self.isOpen:
            self.isOpen = False
        else:
            # dim the main display
            main_display = pygame.display.get_surface()
            pygame.draw.rect(main_display, (0, 0, 0, 0.5), main_display.get_rect())

            # calculate the window's size
            width = self.def_width
            if self.def_height is None:
                height = self.padding * 2
                for child in self.children:
                    height += child.get_height() + 5
            else:
                height = self.def_height

            menu_window = pygame.rect.Rect(0, 0, width, height)

            self.isOpen = True
