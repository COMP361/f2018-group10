from typing import Tuple, Optional

import pygame

from src.Windows.UIComponents.Components import Components


class MenuWindow(object):

    SPACE_BETWEEN = 5

    """
    Popup Menu class
    """
    def __init__(self,
                 width: int,
                 height: Optional[int]=0,
                 def_position: Optional[Tuple[int, int]]=None,
                 color: Tuple[int, ...] = (175, 175, 175, 0.5),
                 padding: int=5):
        """
        Constructor
        :param width: Width of the object
        :param height: Height of the object
        :param def_position: Defined position for the object. Optional
        :param color: Background color of the object represented by an RGB tuple (Alpha optional)
        :param padding: Padding for the menu
        """
        self.grp = pygame.sprite.Group()
        self.window = pygame.sprite.Sprite()

        self.background = pygame.sprite.Sprite()
        self.background.image = pygame.display.get_surface().copy()
        self.background.image.fill(0, 0, 0)
        self.background.image.set_alpha(120)

        self.def_width = width
        self.def_height = None
        self.def_position = None
        self.color = color
        self.padding = padding
        self.children = Tuple[Components]
        self.is_open = False
        self.screen_copy = None

        self.window.x = 0
        self.window.y = 0
        if height:
            self.window.height = height
        if def_position:
            self.def_position = def_position

    def update(self):
        self.grp.draw(pygame.display.get_surface())
        self.grp.update()

    def toggle(self):
        """
        Toggles the popup menu
        :return: void
        """
        main_display = pygame.display.get_surface()

        if self.is_open:
            self.grp.remove(self.window, self.background)
            self.is_open = False
        else:
            # calculate the window's size
            self.window.width = self.def_width
            if self.def_height is None:
                self.window.height = self.padding * 2
                for child in self.children:
                    self.window.height += child.get_height() + self.SPACE_BETWEEN
            else:
                self.window.height = self.def_height

            if self.def_position is None:
                self.window.x = main_display.get_width()/2 - self.window.width/2
                self.window.y = main_display.get_height()/2 - self.window.height/2
            else:
                self.window.x = self.def_position[0]
                self.window.y = self.def_position[1]

            self.grp.add(self.background, self.window)

            # draw the menu on screen
            # menu_window = pygame.rect.Rect(self.x, self.y, width, height)
            # pygame.draw.rect(main_display, self.color, menu_window)
            self.is_open = True

    # TODO: Finish the class. Not sure if I need to call update here or not...

    def _render(self):
        x = self.window.x + self.padding
        y = self.window.y + self.padding
        for child in self.children:
            child.change_pos(x, y)
            y += child.get_height + self.SPACE_BETWEEN

    def add_child(self, child: Components, index: Optional[int]=None):
        """
        Adds component into the end of the menu, if index is defined, adds the child to the specified index.
        :param child:
        :param index:
        :return:
        """
        if index is None:
            self.children.append(child)
        else:
            self.children.insert(index, child)
