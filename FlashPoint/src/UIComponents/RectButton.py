from typing import Tuple, Optional

import pygame

from src.UIComponents.Text import Text
from src.UIComponents.RectLabel import RectLabel
from src.UIComponents.Interactable import Interactable


class RectButton(RectLabel, Interactable):
    def __init__(self,
                 rect: pygame.Rect,
                 color: Tuple[int, int, int],
                 txtobj: Optional[Text] = None,
                 width: int=0):
        super(RectButton, self).__init__(rect, color, txtobj, width)
        self.click_event = None

    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = super(RectButton, self).rect

        if rect.x+rect.w > mouse[0] > rect.x and rect.y+rect.h > mouse[1] > rect.y:
            if click[0] and self.click_event:
                pygame.event.post(self.click_event)


    def on_click(self, click_event: pygame.event):
        self.click_event = click_event

    def off_click(self):
        self.click_event = None
