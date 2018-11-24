from src.Windows.UIComponents.RectButton import RectButton

import pygame
import src.constants.Color as Color
from src.Windows.UIComponents.RectLabel import RectLabel
from src.Windows.UIComponents.Text import Text
from src.Windows.UIComponents.Scene import Scene


class CharacterSelectionMenu(object):

    def __init__(self, screen):
        self.the_scene = Scene.__init__(screen)

        self._init_character_box()

        self.btn0 = RectButton(0, 0, 200, 100, Color.BLUE, 0,
                               Text(pygame.font.SysFont('Arial', 20), "CAFS Firefighter", (0, 255, 0, 0)))

        self.btn1 = RectButton(0, 100, 200, 100, Color.BLUE, 0,
                               Text(pygame.font.SysFont('Arial', 20), "Driver/Operator", (0, 255, 0, 0)))
        self.btn2 = RectButton(0, 200, 200, 100, Color.BLUE, 0,
                               Text(pygame.font.SysFont('Arial', 20), "Fire Captain", (0, 255, 0, 0)))
        self.btn3 = RectButton(0, 300, 200, 100, Color.BLUE, 0,
                               Text(pygame.font.SysFont('Arial', 20), "Generalist", (0, 255, 0, 0)))
        self.btn4 = RectButton(0, 400, 200, 100, Color.BLUE, 0,
                               Text(pygame.font.SysFont('Arial', 20), "Hazmat Technician", (0, 255, 0, 0)))
        self.btn5 = RectButton(0, 500, 200, 100, Color.BLUE, 0,
                               Text(pygame.font.SysFont('Arial', 20), "Imaging Technician", (0, 255, 0, 0)))
        self.btn6 = RectButton(0, 600, 200, 100, Color.BLUE, 0,
                               Text(pygame.font.SysFont('Arial', 20), "Paramedic", (0, 255, 0, 0)))
        self.btn7 = RectButton(0, 700, 200, 100, Color.BLUE, 0,
                               Text(pygame.font.SysFont('Arial', 20), "Rescue Specialist", (0, 255, 0, 0)))

        self.btn8 = RectButton(800, 0, 200, 100, Color.RED, 0,
                               Text(pygame.font.SysFont('Arial', 20), "Back", (0, 255, 0, 0)))
        self.the_scene.sprite_grp.add(self.btn0)
        self.the_scene.sprite_grp.add(self.btn1)
        self.the_scene.sprite_grp.add(self.btn2)
        self.the_scene.sprite_grp.add(self.btn3)
        self.the_scene.sprite_grp.add(self.btn4)
        self.the_scene.sprite_grp.add(self.btn5)
        self.the_scene.sprite_grp.add(self.btn6)
        self.the_scene.sprite_grp.add(self.btn7)
        self.the_scene.sprite_grp.add(self.btn8)

    def update(self):
        self.the_scene.update()

    def draw(self):
        self.the_scene.draw()

    #
    # def _init_btn_img(self, x, y, file_path):
    #     btn = RectButton.__init__(x, y, 95, 95,
    #                               FileImporter.import_image(file_path))
    #     self.btn_grp.add(btn)

    def _init_character_box(self):
        box_size = (self.the_scene.resolution[0] / 2, self.the_scene.resolution[1] / 2)
        x_pos = self.the_scene.resolution[0] / 2 - box_size[0] / 2
        y_pos = self.the_scene.resolution[1] / 2 - box_size[1] / 2
        character_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], Color.GREEN)
        self.the_scene.add(character_box)
