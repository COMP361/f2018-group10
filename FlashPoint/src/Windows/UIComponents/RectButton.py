from typing import Tuple, Optional, Union

import pygame

from src.Windows.UIComponents.Text import Text
from src.Windows.UIComponents.RectLabel import RectLabel
from src.Windows.UIComponents.Interactable import Interactable


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
                 outer_width: int=0,
                 txt_obj: Optional[Text] = None,
                 txt_pos: Text.Position = Text.Position.CENTER):
        __doc__ = RectLabel.__doc__

        RectLabel.__init__(self, x, y, width, height, background, outer_width, txt_obj, txt_pos)
        Interactable.__init__(self, self.rect, self.click(), self.hover())

    def hover(self):
        print("Holy Francis")

    def click(self):
        print("Holy Francis")
