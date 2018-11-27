import pygame

from src.scenes.HostJoinScene import HostJoinScene
from src.scenes.HostMenuScene import HostMenuScene
from src.scenes.JoinScene import JoinScene
from src.scenes.StartScene import StartScene
from src.scenes.Game_Intial_Menu import CreateGameMenu
from src.core.EventQueue import EventQueue
from src.scenes.characterScene import CharacterScene


class SceneManager(object):
    def __init__(self, screen: pygame.Surface):
        """
        Scene Manager. Initialize this before the game loop
        :param screen: should be the main display
        """
        self.screen = screen
        self._active_scene = StartScene(self.screen)
        self._active_scene.buttonLogin.on_click(self.next, HostJoinScene)
        self._active_scene.buttonRegister.on_click(self.next, HostJoinScene)

    def next(self, next_scene: callable):
        """Switch to the next logical scene. args is assumed to be: [SceneClass]
            Its not pretty, but it makes sure that ONLY THE CURRENT SCENE EXISTS IN THE GAME STATE

            Basically, Nuri, when you need to make a new scene, add it here as a condition.
            The way it works is that if an argument was passed, it assumes the argument is a reference to a class
            (not object!! JoinScene vs JoinScene()). It then instantiates the class.

            Then, all the conditions are checked. If there were no args, instantiate the next scene, otherwise use
            the one in args (next_scene). Then, attach all your buttons for that scene.
        """
        # Step one: Create the next scene.
        self._active_scene = next_scene(self.screen)

        # Step two: Set the buttons.
        if isinstance(self._active_scene, StartScene):
            self._active_scene.buttonLogin.on_click(self.next, HostJoinScene)
            self._active_scene.buttonRegister.on_click(self.next, HostJoinScene)

        if isinstance(self._active_scene, HostJoinScene):
            self._active_scene.buttonJoin.on_click(self.next, JoinScene)
            self._active_scene.buttonHost.on_click(self.next, HostMenuScene)
            self._active_scene.buttonBack.on_click(self.next, StartScene)

        if isinstance(self._active_scene, JoinScene):
            self._active_scene.buttonBack.on_click(self.next, HostJoinScene)
            self._active_scene.button.on_click(self.next, CharacterScene)

        if isinstance(self._active_scene, HostMenuScene):
            self._active_scene.buttonBack.on_click(self.next, HostJoinScene)
            self._active_scene.button1.on_click(self.next, CreateGameMenu)

        if isinstance(self._active_scene, CreateGameMenu):
            self._active_scene.buttonBack.on_click(self.next, HostJoinScene)
            self._active_scene.buttonRegister.on_click(self.next, CharacterScene)
        if isinstance(self._active_scene, CharacterScene):
            self._active_scene.buttonBack.on_click(self.next, CreateGameMenu)  # fix to lobby

    def draw(self):
        self._active_scene.draw(self.screen)

    def update(self, event_queue: EventQueue):
        self._active_scene.update(event_queue)
