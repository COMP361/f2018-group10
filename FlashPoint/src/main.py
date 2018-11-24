import sys

# If PyCharm is issuing warnings on pygame methods, suppress it. it's a bug with PyCharm
import pygame

import src.constants.Color as Color
from src.HostJoinScene import HostJoinScene
from src.HostMenuScene import HostMenuScene
from src.JoinScene import JoinScene
from src.StartScene import StartScene
from src.Windows.CharacterSelectionMenu.CharacterScene import CharacterSelectionMenu

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

        self.hjs = HostJoinScene
        self.hms = HostMenuScene
        self.js = JoinScene
        self.ss = StartScene(self.screen)
        self.css = CharacterSelectionMenu

        self.manager = SceneManager  # this is what will help us switch from one scene to another.

        # each of these comments below are each of the scenes
        # self.start_scene = StartScene(self.screen)
        # self.hj_scene = HostJoinScene(self.screen)
        # self.js_scene = JoinScene(self.screen)
        # self.hm_scene = HostMenuScene(self.screen)
        # self.cs_scene = CharacterSelectionMenu(self.screen)
        #
        self.current_scene = self.cs_scene
        self.ss.buttonLogin.on_click(self.manager.switch(self.hjs.sprite_grp))
        self.StartScene.buttonRegister.on_click(self.switch, self.hj_scene)
        self.hj_scene.buttonJoin.on_click(self.switch, self.js_scene)
        self.hj_scene.buttonHost.on_click(self.switch, self.hm_scene)
        self.hj_scene.buttonBack.on_click(self.switch, self.start_scene)
        self.hm_scene.buttonBack.on_click(self.switch, self.hj_scene)
        self.js_scene.buttonBack.on_click(self.switch, self.hj_scene)

    def switch(self, scene):
        self.current_scene = scene

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


if __name__ == '__main__':
    Main().main()
