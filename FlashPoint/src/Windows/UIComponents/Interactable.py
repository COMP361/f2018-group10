from typing import Optional, Callable
from functools import partial

import abc

import pygame


class Interactable(metaclass=abc.ABCMeta):
    """
    Abstract class for objects that can be clicked
    """
    def __init__(self, rect: pygame.rect.Rect, click_action: Optional[Callable], hover_action: Optional[Callable]):
        """
        Initialize the interactive component
        :param rect: Rect area of the component
        :param click_action: Function to be called when clicked
        :param hover_action: Function to be called when hovered over
        """
        self._isHover = False
        self._clicked = False
        self._isEnabled = True
        self._rect = rect
        self._click_action = None
        self._hover_action = None
        # assign click and hover action
        if click_action:
            self._click_action = click_action
        if hover_action:
            self._hover_action = hover_action

    # WTF am I doing
    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = self._rect

        if rect.x+rect.w > mouse[0] > rect.x and rect.y+rect.h > mouse[1] > rect.y:
            # Only executes the hover function when the mouse is first moved into the button
            if not self._isHover:
                self.on_hover()
                self._isHover = True

            if click[0]:
                self.on_click()
        else:
            # Indicate that the mouse has moved out of bound so that the hover function can be run again next time
            self._isHover = False

    # I hope it works LOL
    async def on_click(self):
        """
        Defines the click event
        :return:
        """
        if self._isEnabled and not self._clicked:
            self._clicked = True
            await self.click_action()
            self._clicked = False

    def on_hover(self):
        """
        Defines the hover event
        :return:
        """
        if self._isEnabled and not self._isHover:
            self.hover_action()

    def enable(self):
        """
        Enables the event hook
        :return:
        """
        self._isEnabled = True

    def disable(self):
        """
        Disables the event hook
        :return:
        """
        self._isEnabled = False

    # why is this so hard
    @property
    def click_action(self):
        return self._click_action

    @click_action.setter
    def click_action(self, action: Callable):
        self._click_action = action

    @property
    def hover_action(self):
        return self._hover_action

    @hover_action.setter
    def hover_action(self, action: Callable):
        self._hover_action = action

    # SAVE ME FROM THIS MISERY
