from typing import Callable, Union

import abc
import pygame


class Interactable(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def on_click(self, click_event: Union[pygame.event, Callable]):
        """
        Hook for click event
        :param click_event: Defines the action when the object is clicked
        :return:
        """
        pass

    @abc.abstractmethod
    def off_click(self):
        """
        Removes the click event hook
        :return:
        """
        pass
