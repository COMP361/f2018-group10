from typing import Tuple, Optional, Union

import pygame

from src.UIComponents.Text import Text
from src.UIComponents.EllipseLabel import EllipseLabel
from src.UIComponents.Interactable import Interactable


class EllipseButton(EllipseLabel, Interactable):
    """
    Creates a EllipseLabel and detects mouseclicks on the object
    """
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 background: Union[Tuple[int, int, int], str] = (0, 0, 0),
                 outer_width: int = 0,
                 txt_obj: Optional[Text] = None,
                 txt_pos: Optional[Text.Position] = Text.Position.CENTER):
        __doc__ = EllipseLabel.__doc__

        super(EllipseButton, self).__init__(x, y, width, height, background, outer_width, txt_obj, txt_pos)
        self.isHover = False
        self.isEnabled = True

    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = self.rect

        if rect.x+rect.w > mouse[0] > rect.x and rect.y+rect.h > mouse[1] > rect.y:
            # Only executes the hover function when the mouse is first moved into the button
            if not self.isHover:
                self.hover()
                self.isHover = True

            if click[0] and self.isEnabled:
                self.click()
        else:
            # Indicate that the mouse has moved out of bound so that the hover function can be run again next time
            self.isHover = False

    def hover(self):
        print("Holy Francis")

    def click(self):
        print("Holy Francis")

    def enable(self):
        self.isEnabled = True

    def disable(self):
        self.isEnabled = False
