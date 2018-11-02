import pygame
from src.UIComponents.RectLabel import RectLabel
from src.UIComponents.Text import Text


class Login:
    def __init__(self):
        pass

    def display(self):
        blue = (0, 0, 200)
        green = (0, 200, 0)
        fonts = pygame.font.Font('freesansbold.ttf',10)
        txtObj = Text(fonts, "KIM", blue)
        rectan = pygame.Rect(10,20,30,50)
        label = RectLabel(rectan, green, txtObj, 20)


