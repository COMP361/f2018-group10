import pygame

import src.constants.color as Color
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.scene import Scene


class LoseScene(Scene):
    def __init__(self, screen: pygame.Surface):
        Scene.__init__(self, screen)
        self._init_background()
        self._init_title_text()

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/Win_Loose/fire3.jpg")
        self.sprite_grp.add(background_box)

    def _init_log_box(self):
        box_size = (self.resolution[0] / 2, self.resolution[1] / 2)
        x_pos = self.resolution[0] / 2 - box_size[0] / 2
        y_pos = self.resolution[1] / 2 - box_size[1] / 2
        log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.GREEN)
        self.sprite_grp.add(log_box)

    def _init_title_text(self):
            box_size = (400, 40)
            self.text_title = RectButton(440, 350, box_size[0], box_size[1], "media/Win_Loose/LOST.png"
                                         )

            self.sprite_grp.add(self.text_title)
