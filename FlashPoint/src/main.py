import sys
import traceback
import logging

import pygame

import src.constants.color as Color
import src.constants.main_constants as MainConst
from src.core.networking import Networking
from src.scenes.scene_manager import SceneManager
from src.core.event_queue import EventQueue

logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s', level=logging.DEBUG)

logger = logging.getLogger("FlashPoint")


class Main(object):
    """Class for running the main game loop and maintaining game state."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(MainConst.WINDOW_TITLE)
        self.screen = pygame.display.set_mode(MainConst.SCREEN_RESOLUTION, pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        SceneManager()
        EventQueue()

    def main(self):

        # Run main loop
        # FileImporter.play_music("src/media/music/intro_music/Kontrabandz-Get Down-kissvk.com.mp3", -1)
        #  FileImporter.play_music("src/media/music/Get_Down.wav", -1)

        while True:
            # Lock frame rate at 60 FPS
            try:
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
            except Exception as e:
                info = sys.exc_info()
                logger.error("Exception was raised! Continuing, even though we might be screwed.")
                traceback.print_exception(*info)


def run():
    Main().main()


if __name__ == '__main__':
    run()
