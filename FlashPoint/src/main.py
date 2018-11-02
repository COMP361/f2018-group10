import sys
from src.Login import Login
# If PyCharm is issuing warnings on pygame methods, suppress it. it's a bug with PyCharm
import pygame
#from src.Test import Display



def main():
    # Initialize pygame modules, get the screen and clock
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    # Run main loop
    while True:
        # Lock frame rate at 60 FPS. Should only be called once per loop.
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Clear the screen to black and flip the double buffer
        screen.fill((255, 255, 255))
        pygame.display.flip()
        #display = Display(screen)
        #display.game_intro()
        log = Login()
        log.display()


if __name__ == '__main__':
    main()
