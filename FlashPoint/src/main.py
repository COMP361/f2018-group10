import sys

# If PyCharm is issuing warnings on pygame methods, suppress it. it's a bug with PyCharm
import pygame

import src.constants.Color as Color
from src.StartScene import StartScene


class Main(object):
    """Class for running the main game loop and maintaining game state."""
    SCREEN_RESOLUTION = (1280, 700)
    WINDOW_TITLE = "Flash Point"

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(Main.WINDOW_TITLE)
        self.screen = pygame.display.set_mode(Main.SCREEN_RESOLUTION)
        self.clock = pygame.time.Clock()

        self.current_scene = StartScene(self.screen)

    def main(self):
        # Initialize pygame modules, get the screen and clock

        # Run main loop
        while True:
            # Lock frame rate at 60 FPS. Should only be called once per loop.
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Clear the screen to black and flip the double buffer
            self.screen.fill(Color.BLACK)

            self.current_scene.draw()
            self.current_scene.update()

            pygame.display.flip()


if __name__ == '__main__':
    Main().main()
