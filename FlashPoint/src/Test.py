import pygame
import sys


class Display:
    def __init__(self, screen):
        self.screen = screen

    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 200, 0)
    blue = (0, 0, 200)
    display_width = 800
    display_height = 600

    def game_intro(self):
        intro = True

        def text_objects(text, font):
            textSurface = font.render(text, True, self.black)
            return textSurface, textSurface.get_rect()

        def button(msg, x, y, w, h, ic, ac):
            mouse = pygame.mouse.get_pos()

            if x + w > mouse[0] > x and y + h > mouse[1] > y:
                pygame.draw.rect(self.screen, ac, (x, y, w, h))
            else:
                pygame.draw.rect(self.screen, ic, (x, y, w, h))

            smallText = pygame.font.Font("freesansbold.ttf", 20)
            textSurf, textRect = text_objects(msg, smallText)
            textRect.center = ((x + (w / 2)), (y + (h / 2)))
            self.screen.blit(textSurf, textRect)

        while intro:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            largeText = pygame.font.Font('freesansbold.ttf', 115)
            TextSurf, TextRect = text_objects("HOLY Francis", largeText)
            # infoObject = pygame.display.Info()
            # TextRect.center = ((infoObject.current_w / 2), (infoObject.current_h / 2))
            self.screen.blit(TextSurf, TextRect)
            # pygame.draw.rect(self.screen, self.black, (150, 450, 100, 50))
            # pygame.draw.rect(self.screen, self.green, (550, 450, 100, 50))

            button("Play", 150, 450, 100, 50, self.blue, self.green)

            pygame.display.update()
