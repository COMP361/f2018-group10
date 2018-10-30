from typing import Callable, Union, Optional

import abc
import pygame


class Interactable(metaclass=abc.ABCMeta):
    """
    Interface class for objects that can be clicked
    """
    @abc.abstractmethod
    def click(self):
        """
        Defines the click event
        :return:
        """
        pass

    @abc.abstractmethod
    def hover(self):
        """
        Defines the hover event
        :return:
        """
        pass

    @abc.abstractmethod
    def enable(self):
        """
        Enables the click event hook
        :return:
        """
        pass

    @abc.abstractmethod
    def disable(self):
        """
        Disables the click event hook
        :return:
        """
        pass
