import sys

# If PyCharm is issuing warnings on pygame methods, suppress it. it's a bug with PyCharm
import pygame

import src.constants.Color as Color
from src.HostJoinScene import HostJoinScene
from src.HostMenuScene import HostMenuScene
from src.JoinScene import JoinScene
from src.StartScene import StartScene


def click(btn: RectButton):
    print("Holy Francis")
    btn.change_color((76, 255, 255))

class Main(object):
    """Class for running the main game loop and maintaining game state."""
    SCREEN_RESOLUTION = (1280, 700)
    WINDOW_TITLE = "Flash Point"

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(Main.WINDOW_TITLE)
        self.screen = pygame.display.set_mode(Main.SCREEN_RESOLUTION)
        self.clock = pygame.time.Clock()

        # each of these comments below are each of the scenes

        self.current_scene = StartScene(self.screen)
        # self.current_scene = JoinScene(self.screen)
        # self.current_scene = HostMenuScene(self.screen)
        # self.current_scene = HostJoinScene(self.screen)

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
