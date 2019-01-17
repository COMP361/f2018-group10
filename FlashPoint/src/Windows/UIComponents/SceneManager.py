from typing import Optional

import pygame

from src.Windows.UIComponents.Scene import Scene
from src.Windows.UIComponents.FileImporter import FileImporter
from src.scenes.GameBoardScene import GameBoardScene
from src.scenes.HostJoinScene import HostJoinScene
from src.scenes.HostMenuScene import HostMenuScene
from src.scenes.JoinScene import JoinScene
from src.scenes.StartScene import StartScene
from src.scenes.Game_Intial_Menu import CreateGameMenu
from src.core.EventQueue import EventQueue
from src.scenes.characterScene import CharacterScene
from src.scenes.LobbyScene import LobbyScene

from src.core.Networking import Networking


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

    def next(self, next_scene: callable, *args):
        """Switch to the next logical scene. args is assumed to be: [SceneClass]
            Its not pretty, but it makes sure that ONLY THE CURRENT SCENE EXISTS IN THE GAME STATE

            Basically, Nuri, when you need to make a new scene, add it here as a condition.
            The way it works is that if an argument was passed, it assumes the argument is a reference to a class
            (not object!! JoinScene vs JoinScene()). It then instantiates the class.

            Then, all the conditions are checked. If there were no args, instantiate the next scene, otherwise use
            the one in args (next_scene). Then, attach all your buttons for that scene.
        """
        # Step one: Create the next scene.
        self._active_scene = next_scene(self.screen, *args)

        # Step two: Set the buttons.
        if isinstance(self._active_scene, StartScene):
            self._active_scene.buttonLogin.on_click(self.next, HostJoinScene)
            self._active_scene.buttonRegister.on_click(self.next, HostJoinScene)

        if isinstance(self._active_scene, HostJoinScene):
            self._active_scene.buttonJoin.on_click(self.next, JoinScene)
            self._active_scene.buttonHost.on_click(self.host, HostMenuScene)
            self._active_scene.buttonBack.on_click(self.next, StartScene)

        if isinstance(self._active_scene, JoinScene):
            self._active_scene.buttonBack.on_click(self.next, HostJoinScene)
            self._active_scene.buttonConnect.on_click(self.join, self._active_scene.text_bar_msg, LobbyScene, True)

        if isinstance(self._active_scene, HostMenuScene):
            self._active_scene.buttonBack.on_click(self.disconnect, HostJoinScene)
            self._active_scene.buttonNewGame.on_click(self.next, CreateGameMenu)

        if isinstance(self._active_scene, CreateGameMenu):
            self._active_scene.buttonBack.on_click(self.disconnect, HostJoinScene)
            self._active_scene.buttonExp.on_click(self.next, LobbyScene, True)
            self._active_scene.buttonFamily.on_click(self.next, LobbyScene, False)

        if isinstance(self._active_scene, CharacterScene):
            self._active_scene.buttonBack.on_click(self.next, LobbyScene, True)
            self._active_scene.buttonConfirm.on_click(self.next, LobbyScene, True)

        if isinstance(self._active_scene, LobbyScene):
            if self._active_scene.is_experienced:
                self._active_scene.buttonSelChar.on_click(self.next, CharacterScene)

            self._active_scene.buttonBack.on_click(self.disconnect, HostJoinScene)
            self._active_scene.buttonReady.on_click(self.next, GameBoardScene)

        if isinstance(self._active_scene, GameBoardScene):
            self._active_scene.quit_btn.on_click(self.next, StartScene)

        FileImporter.play_audio("media/soundeffects/ButtonClick.wav", fade_ms=10)

    def draw(self):
        self._active_scene.draw(self.screen)

    def update(self, event_queue: EventQueue):
        self._active_scene.update(event_queue)
        for event in event_queue:
            self.handle_event(event)

    def handle_event(self, event):
        # join event
        if event.type == pygame.USEREVENT+1:
            self.join(event.ip, LobbyScene, True)

    def host(self, next_scene: Optional[callable] = None, *args):
        Networking.get_instance().create_host()

        if next_scene is not None:
            self.next(next_scene, args)

    def join(self, ip_addr, next_scene: Optional[callable] = None, *args):
        if isinstance(self._active_scene, JoinScene):
            is_join_scene = True
        else:
            is_join_scene = False

        try:
            Networking.get_instance().join_host(ip_addr)

            if next_scene is not None:
                self.next(next_scene, args)
        except ConnectionError:
            msg = "Unable to connect"
            print(msg)
            if is_join_scene:
                self._active_scene.init_error_message(msg)
        except OSError:
            msg = "Invalid IP address"
            print(msg)
            if is_join_scene:
                self._active_scene.init_error_message(msg)

    def disconnect(self, next_scene: Optional[callable] = None, *args):
        Networking.get_instance().disconnect()

        if next_scene is not None:
            self.next(next_scene, args)
