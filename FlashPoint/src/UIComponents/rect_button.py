from typing import Tuple, Optional, Union

import pygame

from src.UIComponents.text import Text
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.interactable import Interactable


class RectButton(RectLabel, Interactable):
    """
    Creates a RectLabel and detects mouseclicks on the object
    """
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 background: Union[Tuple[int, int, int], str] = (0, 0, 0),
                 outer_width: int = 0,
                 txt_obj: Optional[Text] = None,
                 txt_pos: Text.Position = Text.Position.CENTER):
        __doc__ = RectLabel.__doc__

        RectLabel.__init__(self, x, y, width, height, background, outer_width, txt_obj, txt_pos)
        Interactable.__init__(self, self.rect)

    def change_rect(self, rect: pygame.Rect, outer_width: int = 0):
        self.rect = rect
        self.outer_width = outer_width
        self.resize_rect(self.rect)
        self._render()




