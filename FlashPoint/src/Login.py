import pygame
from src.Windows.UIComponents.RectButton import RectButton
from src.Windows.UIComponents.Text import Text
from src.constants.Color import Color


class Login:
    def __init__(self,screen):
        self.screen = screen
        self.btn_grp = pygame.sprite.Group()
        self.btn1 = RectButton(10, 10, 60, 40, Color.GREEN.value, 0, Text(pygame.font.SysFont('Arial', 12), "Hover me", (0, 255, 0, 0)))

    def draw(self):

        # fonts = pygame.font.Font('freesansbold.ttf',10)
        # txtObj = Text(fonts, "KIM", Color.BLUE.value)
        # rectan = pygame.Rect(10,20,30,50)
        # label = RectLabel(10, 20, 30, 50, Color.GREEN.value, 0, txtObj)
        # btn_grp = pygame.sprite.Group()
        # btn1 = RectButton(10, 10, 60, 40, Color.GREEN.value, 0, Text(pygame.font.SysFont('Arial', 12), "Hover me", (0, 255, 0,0)))
        self.btn_grp.add(self.btn1)
        self.btn_grp.draw(self.screen)
        self.btn_grp.update()
        #lab_grp = pygame.sprite.Group()
        #label.render(self)

    def update(self):
        pass

