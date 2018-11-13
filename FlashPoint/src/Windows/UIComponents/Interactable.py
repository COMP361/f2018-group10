from typing import Optional, Callable, Mapping

import pygame


class Interactable(pygame.sprite.Sprite):
    """
    Class for objects that can be clicked

    @TODO ---- NURI PLEASE READ THIS @
    To add a click action to the object, use this syntax:

        Object.on_click(function, {arg1, arg2,...})

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
        self._isHover = False
        self._clicked = False
        self._isEnabled = True
        self._rect = rect
        self._click_action = None
        self._click_args = {}
        self._hover_action = None
        self._hover_args = {}

    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = self._rect

        if rect.x+rect.w > mouse[0] > rect.x and rect.y+rect.h > mouse[1] > rect.y:
            # Only executes the hover function when the mouse is first moved into the button
            if not self._isHover:
                self.hover()
                self._isHover = True

            if click[0]:
                self.click()
        else:
            # Indicate that the mouse has moved out of bound so that the hover function can be run again next time
            self._isHover = False

    # I hope it works LOL
    def click(self):
        """
        Defines the click event
        :return:
        """
        if self._isEnabled and not self._clicked:
            self._clicked = True
            if isinstance(self._click_action, Callable):
                if len(self._click_args) > 0:
                    self._click_action(**self._click_args)
                else:
                    self._click_action()
            self._clicked = False

    def hover(self):
        """
        Defines the hover event
        :return:
        """
        if self._isEnabled and not self._isHover:
            if isinstance(self._hover_action, Callable):
                if len(self._hover_args) > 0:
                    self._hover_action(**self._hover_args)
                else:
                    self._hover_action()

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

    def on_click(self, click_action: Callable, click_args: Optional[Mapping]=None):
        """
        Assign a function to the click hook
        :param click_action: function to be executed when clicked
        :param click_args: arguments for the function
        :return:
        """
        self._click_action = click_action
        if isinstance(click_args, Mapping):
            self._click_args = click_args

    def on_hover(self, hover_action: Callable, hover_args: Optional[Mapping]=None):
        """
        Assign a function to the hover hook
        :param hover_action: function to be executed when hovered
        :param hover_args: arguments for the function
        :return:
        """
        self._hover_action = hover_action
        if isinstance(hover_args, Mapping):
            self._hover_args = hover_args

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
