import os

import pygame
import json
import logging

from src.core.serializer import JSONSerializer
from src.models.game_units.player_model import PlayerModel
from src.UIComponents.file_importer import FileImporter
from src.UIComponents.input_box import InputBox
from src.scenes.game_board_scene import GameBoardScene
from src.scenes.host_join_scene import HostJoinScene
from src.scenes.host_menu_scene import HostMenuScene
from src.scenes.join_scene import JoinScene
from src.scenes.load_game_scene import LoadGame
from src.scenes.start_scene import StartScene
from src.scenes.create_game_menu import CreateGameMenu
from src.core.event_queue import EventQueue
from src.scenes.character_scene import CharacterScene
from src.scenes.lobby_scene import LobbyScene
from src.core.networking import Networking
from src.constants.change_scene_enum import ChangeSceneEnum
import src.constants.main_constants as MainConst

logger = logging.getLogger("SManager")
logger.setLevel(logging.INFO)


class SceneManager(object):
    """Controller class for managing scenes, and their interactions. If an object needs to be passed from one scene
    to another, it must go through this class."""

    __instance = None

    @staticmethod
    def get_instance():
        if not SceneManager.__instance:
            SceneManager()
        return SceneManager.__instance

    def __init__(self):
        if SceneManager.__instance is None:
            SceneManager.__instance = SceneManager.SMInner(pygame.display.set_mode(MainConst.SCREEN_RESOLUTION))
        else:
            logger.exception("Attempted to instantiate another singleton")
            raise Exception("SceneManager is a Singleton")

    def __getattr__(self, name):
        return getattr(self.__instance, name)

    @staticmethod
    def draw():
        SceneManager.get_instance().draw()

    @staticmethod
    def update(event_queue: EventQueue):
        SceneManager.get_instance().update(event_queue)

    class SMInner(object):
        def __init__(self, screen: pygame.Surface):
            """
            Scene Manager. Initialize this before the game loop
            :param screen: should be the main display
           """
            self.profiles = "media/profiles.json"
            self.screen = screen
            self._active_scene = StartScene(self.screen)
            self._current_player = None
            self.update_profiles()

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
            if args and isinstance(args[0], PlayerModel):
                self._current_player = args[0]
            self._active_scene = next_scene(self.screen, *args)

            # Step two: Set the buttons.
            if isinstance(self._active_scene, StartScene):
                self.update_profiles()

            FileImporter.play_audio("media/soundeffects/ButtonClick.wav", fade_ms=10)

        def draw(self):
            self._active_scene.draw(self.screen)

        def update(self, event_queue: EventQueue):
            self._active_scene.update(event_queue)
            for event in event_queue:
                if isinstance(event, ChangeSceneEnum):
                    if event == ChangeSceneEnum.REGISTER:
                        self.create_profile(self._active_scene.text_bar1)
                        self.update_profiles()
                    elif event == ChangeSceneEnum.STARTSCENE:
                        self.next(StartScene)
                    elif event == ChangeSceneEnum.CHARACTERSCENE:
                        self.next(CharacterScene, self._current_player)
                    elif event == ChangeSceneEnum.CREATEGAMEMENU:
                        self.next(CreateGameMenu, self._current_player)
                    elif event == ChangeSceneEnum.HOSTJOINSCENE:
                        self.next(HostJoinScene, self._current_player)
                    elif event == ChangeSceneEnum.HOSTMENUSCENE:
                        self.next(HostMenuScene, self._current_player)
                    elif event == ChangeSceneEnum.JOINSCENE:
                        self.next(JoinScene, self._current_player)
                    elif event == ChangeSceneEnum.LOADGAME:
                        self.next(LoadGame, self._current_player)
                    elif event == ChangeSceneEnum.LOBBYSCENE:
                        self.next(LobbyScene, self._current_player)
                    elif event == ChangeSceneEnum.GAMEBOARDSCENE:
                        self.next(GameBoardScene, self._current_player)

        # ------------ Stuff for profiles and start scene ------------ #

        def update_profiles(self):
            if not os.path.exists(self.profiles):
                with open(self.profiles, mode="w+", encoding='utf-8') as myFile:
                    myFile.write("[]")
            with open(self.profiles, mode='r', encoding='utf-8') as myFile:
                temp = json.load(myFile)
                for i, user in enumerate(temp):
                    player: PlayerModel = JSONSerializer.deserialize(user)
                    self._active_scene.profile.set_profile(i, player.nickname, self.next, HostJoinScene, player)
                    self._active_scene.profile.remove_profile_callback(i, self.remove_profile, player.nickname)

        def create_profile(self, text_bar: InputBox):
            temp = {}
            with open(self.profiles, mode='r+', encoding='utf-8') as myFile:

                temp = json.load(myFile)
                size = len(temp)
                if size >= 3:
                    return

                if not text_bar.text.strip():
                    return

                # Create a player model
                player_model = PlayerModel(
                    ip=Networking.get_instance().get_ip(),
                    nickname=text_bar.text.strip()
                )
                player = JSONSerializer.serialize(player_model)
                temp.append(player)

            with open(self.profiles, mode='w', encoding='utf-8') as myFile:
                json.dump(temp, myFile)

            self.update_profiles()

        def remove_profile(self, removename: str):
            temp = {}
            with open(self.profiles, mode='r+', encoding='utf-8') as myFile:
                temp = json.load(myFile)
                for perm in temp:
                    for name in perm.values():
                        if name == removename:
                            temp.remove(perm)
                        else:
                            continue

            with open(self.profiles, mode='w', encoding='utf-8') as myFile:
                json.dump(temp, myFile)

            self.update_profiles()
