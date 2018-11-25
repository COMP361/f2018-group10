import sys

# If PyCharm is issuing warnings on pygame methods, suppress it. it's a bug with PyCharm
import pygame

import src.constants.Color as Color
from src.HostJoinScene import HostJoinScene
from src.HostMenuScene import HostMenuScene
from src.JoinScene import JoinScene
from src.StartScene import StartScene
from src.Windows.CharacterSelectionMenu.CharacterScene import CharacterSelectionMenu
from src.Game_Intial_Menu import GameIntialMenu

from src.Windows.UIComponents.SceneManager import SceneManager


class Main(object):
    """Class for running the main game loop and maintaining game state."""
    SCREEN_RESOLUTION = (1280, 700)
    WINDOW_TITLE = "Flash Point"

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(Main.WINDOW_TITLE)
        self.screen = pygame.display.set_mode(Main.SCREEN_RESOLUTION)
        self.clock = pygame.time.Clock()
        self._init_buttons()

        # this is what will help us switch from one scene to another.

        # each of these comments below are each of the scenes

    def main(self):
        # Initialize pygame modules, get the screen and clock

        # Run main loop
        while True:
            # Lock frame rate at 60 FPS. Should only be called once per loop.
            self.clock.tick(60)

            self.screen.fill(Color.BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Clear the screen to black and flip the double buffer

            self.manager.draw()
            self.manager.update()

            pygame.display.flip()

    def _init_buttons(self):
        self.hjs = HostJoinScene(self.screen)
        self.hms = HostMenuScene(self.screen)
        self.js = JoinScene(self.screen)
        self.ss = StartScene(self.screen)
        self.css = CharacterSelectionMenu(self.screen)
        self.gim = GameIntialMenu(self.screen)
        self.manager = SceneManager(self.screen, self.ss)
        self.ss.buttonLogin.on_click(self.manager.switch, self.hjs)
        self.ss.buttonRegister.on_click(self.manager.switch, self.hjs)
        self.hjs.buttonJoin.on_click(self.manager.switch, self.js)
        self.hjs.buttonHost.on_click(self.manager.switch, self.hms)
        self.hjs.buttonBack.on_click(self.manager.switch, self.ss)
        self.hms.buttonBack.on_click(self.manager.switch, self.hjs)
        self.js.buttonBack.on_click(self.manager.switch, self.hjs)
        self.hms.button1.on_click(self.manager.switch, self.gim)
        self.gim.buttonBack.on_click(self.manager.switch,self.hms)
        #self.gim.buttonRegister.on_click(self.manager.switch, self.)


if __name__ == '__main__':
    Main().main()
