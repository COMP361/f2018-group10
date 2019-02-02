import pygame

<<<<<<< HEAD:FlashPoint/src/scenes/HostMenuScene.py
import src.constants.color as Color
from src.UIComponents.RectButton import RectButton
from src.UIComponents.RectLabel import RectLabel
from src.UIComponents.Text import Text
from src.UIComponents.Scene import Scene
=======
import src.constants.Color as Color
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.UIComponents.scene import Scene
>>>>>>> GSD-Alek:FlashPoint/src/scenes/host_menu_scene.py


class HostMenuScene(Scene):
    def __init__(self, screen):
        Scene.__init__(self, screen)
        self._init_background()

        self._init_btn_new_game(575, 481, "New Game", Color.STANDARDBTN, Color.BLACK)
        self._init_btn_leg(575, 371, "Load Game", Color.STANDARDBTN, Color.BLACK)
        self._init_btn_back(20, 20, "Back", Color.STANDARDBTN, Color.BLACK)

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/flashpoint_background.png")
        self.sprite_grp.add(background_box)

    def _init_log_box(self):
        box_size = (self.resolution[0] / 2, self.resolution[1] / 2)
        x_pos = self.resolution[0] / 2 - box_size[0] / 2
        y_pos = self.resolution[1] / 2 - box_size[1] / 2
        log_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.GREEN)
        self.sprite_grp.add(log_box)

    def _init_btn_new_game(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonNewGame = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                        Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonNewGame)

    def _init_btn_leg(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonLEG = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                    Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonLEG)

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonBack)
