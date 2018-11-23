from src.Windows.UIComponents.RectButton import RectButton
from src.Windows.UIComponents.FileImporter import FileImporter
import pygame


class CharacterScene:

    def __init__(self):
        _init_btn(self, 0, 0, "src/Windows/CharacterSelectionMenu/Cafs_Firefighter.png")
        _init_btn(self, 0, 35, "src/Windows/CharacterSelectionMenu/Drive_Operator.png")
        _init_btn(self, 0, 70, "src/Windows/CharacterSelectionMenu/Fire_Captain.png")
        _init_btn(self, 0, 105, "src/Windows/CharacterSelectionMenu/Generalist.png")
        _init_btn(self, 0, 140, "src/Windows/CharacterSelectionMenu/Hazmat_Technician.png")
        _init_btn(self, 0, 175, "src/Windows/CharacterSelectionMenu/Imaging_Technician.png")
        _init_btn(self, 0, 210, "src/Windows/CharacterSelectionMenu/Paramedic.png")
        _init_btn(self, 0, 245, "src/Windows/CharacterSelectionMenu/Rescue_Specialist.png")

        self.btn_grp = pygame.sprite.Group()


def update(self):
    pass


def draw(self):
    pygame.init()
    screen = pygame.display.set_mode(1280, 720)


def _init_btn(self, x, y, file_path):
    btn = RectButton.__init__(self.btn, x, y, 30, 30,
                              FileImporter.import_image(file_path))
    self.btn_grp.add(btn)
