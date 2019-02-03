import sys

# If PyCharm is issuing warnings on pygame methods, suppress it. it's a bug with PyCharm
import pygame

import src.constants.Color as Color
import src.constants.MainConstants as MainConst
from src.UIComponents.FileImporter import FileImporter
from src.UIComponents.SceneManager import SceneManager
from src.core.EventQueue import EventQueue


class Main(object):
    """Class for running the main game loop and maintaining game state."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(MainConst.WINDOW_TITLE)
        self.screen = pygame.display.set_mode(MainConst.SCREEN_RESOLUTION)
        self.clock = pygame.time.Clock()
        self.scene_manager = SceneManager(self.screen)
        self.event_queue = EventQueue()
        self.background = FileImporter.import_image("media/WoodBack.jpg")


    def main(self):
        # Run main loop
        #FileImporter.play_music("media/music/jorge_music/nightbells.mp3", -1)

        while True:
            # Lock frame rate at 60 FPS. Should only be called once per loop.
            self.clock.tick(60)
            self.event_queue.fill_queue()
           # self.screen.fill(Color.BLACK)



            for event in self.event_queue:
                if event.type == pygame.QUIT:
                    sys.exit()

            # Clear the screen to black
            #self.screen.fill(Color.BLACK)
            self.screen.blit(self.background, (0,0))

            self.scene_manager.draw()
            self.scene_manager.update(self.event_queue)

            self.event_queue.flush_queue()

            pygame.display.flip()


if __name__ == '__main__':
    Main().main()
