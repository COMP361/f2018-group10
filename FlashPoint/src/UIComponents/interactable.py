from typing import Callable

import pygame
from src.constants.change_scene_enum import ChangeSceneEnum

from src.core.event_queue import EventQueue


class Interactable(pygame.sprite.Sprite):
    """
    Class for objects that can be clicked

    @TODO ---- NURI PLEASE READ THIS @
    To add a click action to the object, use this syntax:

        Object.on_click(function, arg1, arg2,...)

        - Assume "Object" inherits Interactable
        - function must be only the name (i.e. without brackets)

    Same idea goes for hover action (see my main.py for example)
    @TODO implement an asynchronous event loop for clickable actions
    """
    def __init__(self, rect: pygame.rect.Rect):
        """
        Initialize the interactive component
        :param rect: Rect area of the component
        """
        pygame.sprite.Sprite.__init__(self)
        self._is_hover = False
        self._clicked = False
        self._is_enabled = True
        self._rect = rect
        self._click_action = None
        self._click_args = None
        self._click_kwargs = None
        self._hover_action = None
        self._hover_args = None
        self._hover_kwargs = None
        self._off_hover_action = None
        self._off_hover_args = None
        self._off_hover_kwargs = None

    def update(self, event_queue: EventQueue):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = self._rect

        if rect.x+rect.w > mouse[0] > rect.x and rect.y+rect.h > mouse[1] > rect.y:
            # Only executes the hover function when the mouse is first moved into the button
            if not self._is_hover:
                self.hover()

            for event in event_queue:
                if not isinstance(event, ChangeSceneEnum):
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not self._clicked:
                        self._clicked = True
                        self.click()

            if not click[0]:
                self._clicked = False
        else:
            # Indicate that the mouse has moved out of bound so that the hover function can be run again next time
            self.exit_hover()

    def on_click(self, click_action: Callable, *args, **kwargs):
        """
        Assign a function to the click hook
        :param click_action: function to be executed when clicked
        :param args: Non key-worded arguments for the function
        :param kwargs: Key-worded parameters for the function
        :return:
        """
        self._click_action = click_action
        if args is not None:
            self._click_args = args
        if kwargs is not None:
            self._click_kwargs = kwargs

    def on_hover(self, hover_action: Callable, *args, **kwargs):
        """
        Assign a function to the ON hover hook
        :param hover_action: function to be executed when hovered
        :param args: Non key-worded arguments for the function
        :param kwargs: Key-worded arguments for the function
        :return:
        """
        self._hover_action = hover_action
        if args is not None:
            self._hover_args = args
        if kwargs is not None:
            self._hover_kwargs = kwargs

    def off_hover(self, off_hover_action: Callable, *args, **kwargs):
        """
        Assign a function to the OFF hover hook
        :param off_hover_action: function to be executed when exiting hovered state
        :param args: Non key-worded arguments for the function
        :param kwargs: Key-worded arguments for the function
        :return:
        """
        self._off_hover_action = off_hover_action
        if args is not None:
            self._off_hover_args = args
        if kwargs is not None:
            self._off_hover_kwargs = kwargs

    # I hope it works LOL
    def click(self):
        """
        Defines the click event
        :return:
        """
        if self._is_enabled:
            if isinstance(self._click_action, Callable):
                return self._click_action(*self._click_args, **self._click_kwargs)

    def hover(self):
        """
        Defines the hover event
        :return:
        """
        if self._is_enabled and not self._is_hover:
            if isinstance(self._hover_action, Callable):
                self._hover_action(*self._hover_args, **self._hover_kwargs)
                self._is_hover = True

    def exit_hover(self):
        """
        Defines the off hover event
        :return:
        """
        if self._is_enabled and self._is_hover:
            if isinstance(self._off_hover_action, Callable):
                self._off_hover_action(*self._off_hover_args, **self._off_hover_kwargs)
                self._is_hover = False

    def enable(self):
        """
        Enables the event hook
        :return:
        """
        # print(f"Enabling: {self}")
        self._is_enabled = True

    def disable(self):
        """
        Disables the event hook
        :return:
        """
        self._is_enabled = False

    def resize_rect(self, rect: pygame.rect.Rect):
        self._rect = rect

    @property
    def enabled(self):
        return self._is_enabled

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

    @property
    def off_hover_action(self):
        return self._off_hover_action

    @off_hover_action.setter
    def off_hover_action(self, action: Callable):
        self._off_hover_action = action

    # SAVE ME FROM THIS MISERY
