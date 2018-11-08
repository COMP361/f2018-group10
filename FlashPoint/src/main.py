import sys

# If PyCharm is issuing warnings on pygame methods, suppress it. it's a bug with PyCharm
import pygame

from src.Windows.UIComponents.RectButton import RectButton
from src.Windows.UIComponents.Text import Text


def main():
    # Initialize pygame modules, get the screen and clock
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    btn_grp = pygame.sprite.Group()
    btn1 = RectButton(10, 10, 300, 100, (255, 76, 255), 0, Text(pygame.font.SysFont('Arial', 12), "Hover me", (0, 255,0)))
    btn_grp.add(btn1)

    # Run main loop
    while True:
        # Lock frame rate at 60 FPS. Should only be called once per loop.
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Clear the screen to black and flip the double buffer
        screen.fill((0, 0, 0))
        btn_grp.draw(screen)
        btn_grp.update()
        pygame.display.flip()


if __name__ == '__main__':
    main()
