import pygame
from src.UIComponents.RectLabel import RectLabel
from src.UIComponents.Text import Text
from src.constants.Color import Color


class Login:
    def __init__(self):
        pass

    def draw(self):

        fonts = pygame.font.Font('freesansbold.ttf',10)
        txtObj = Text(fonts, "KIM", Color.BLUE.value)
        rectan = pygame.Rect(10,20,30,50)
        label = RectLabel(rectan, Color.GREEN.value, txtObj, 20)
        label.render()

    def update(self):
        pass

