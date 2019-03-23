import sys

# If PyCharm is issuing warnings on pygame methods, suppress it. it's a bug with PyCharm
import pygame

import src.constants.color as Color
import src.constants.main_constants as MainConst
from src.UIComponents.file_importer import FileImporter
from src.core.networking import Networking
from src.scenes.scene_manager import SceneManager
from src.core.event_queue import EventQueue


class Main(object):
    """Class for running the main game loop and maintaining game state."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(MainConst.WINDOW_TITLE)
        self.screen = pygame.display.set_mode(MainConst.SCREEN_RESOLUTION)
        self.clock = pygame.time.Clock()
        SceneManager()
        EventQueue()

    def main(self):
        # Run main loop
        # FileImporter.play_music("media/music/intro_music/Kontrabandz-Get Down-kissvk.com.mp3", -1)
        # FileImporter.play_music("media/music/Get_Down.wav", -1)
        while True:
            # Lock frame rate at 60 FPS. Should only be called once per loop.
            self.clock.tick(60)
            EventQueue.fill_queue()
            self.screen.fill(Color.BLACK)

            for event in EventQueue.get_instance():
                if event.type == pygame.QUIT:
                    Networking.get_instance().disconnect()
                    sys.exit()

            # Clear the screen to black
            self.screen.fill(Color.BLACK)

            SceneManager.draw()
            SceneManager.update(EventQueue.get_instance())

            EventQueue.flush_queue()

            pygame.display.flip()


if __name__ == '__main__':
    Main().main()
