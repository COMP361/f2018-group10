from typing import Tuple, Optional, Union

from src.Windows.UIComponents.Text import Text
from src.Windows.UIComponents.EllipseLabel import EllipseLabel
from src.Windows.UIComponents.Interactable import Interactable


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
