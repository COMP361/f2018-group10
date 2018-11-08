import sys

import pygame

import src.constants.Color as Color
from src.scenes.GameBoardScene import GameBoardScene


class Main(object):
    """Class for running the main game loop and maintaining game state."""
    SCREEN_RESOLUTION = (1280, 700)
    WINDOW_TITLE = "Flash Point"

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(Main.WINDOW_TITLE)
        self.screen = pygame.display.set_mode(Main.SCREEN_RESOLUTION)
        self.clock = pygame.time.Clock()
        self.current_scene = GameBoardScene(self.screen)
        
    def main(self):
        # Run main game loop
        while True:
            # Lock frame rate at 60 FPS. Should only be called once per loop.
            self.clock.tick(60)
            
            # Check events for if the user closed the window.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


            # Clear the screen to black
            self.screen.fill(Color.BLACK)

            self.current_scene.update()
            self.current_scene.draw()
            # Flip double buffer
            pygame.display.flip()


# Should only be used for debugging purposes
if __name__ == '__main__':
    Main().main()
