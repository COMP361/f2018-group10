import pygame
import logging

from src.models.game_units.player_model import PlayerModel
from src.UIComponents.file_importer import FileImporter
from src.scenes.choose_board_scene import ChooseBoard
from src.scenes.game_board_scene import GameBoardScene
from src.scenes.host_join_scene import HostJoinScene
from src.scenes.host_menu_scene import HostMenuScene
from src.scenes.join_scene import JoinScene
from src.scenes.load_game_scene import LoadGame
from src.scenes.start_scene import StartScene
from src.scenes.set_max_players_scene import SetMaxPlayers
from src.scenes.create_game_menu import CreateGameMenu
from src.core.event_queue import EventQueue
from src.scenes.character_scene import CharacterScene
from src.scenes.lobby_scene import LobbyScene
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
            self.screen = screen
            self._active_scene = StartScene(self.screen)
            self._current_player = None

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

            FileImporter.play_audio("media/soundeffects/ButtonClick.wav", fade_ms=10)

        def draw(self):
            self._active_scene.draw(self.screen)

        def update(self, event_queue: EventQueue):
            self._active_scene.update(event_queue)
            for event in event_queue:
                if event.type == ChangeSceneEnum.STARTSCENE:
                    self.next(StartScene)
                elif event.type == ChangeSceneEnum.SETMAXPLAYERSCENE:
                    self.next(SetMaxPlayers, self._current_player)
                elif event.type == ChangeSceneEnum.CHOOSEBOARDSCENE:
                    self.next(ChooseBoard, self._current_player)
                elif event.type == ChangeSceneEnum.CHARACTERSCENE:
                    self.next(CharacterScene, self._current_player)
                elif event.type == ChangeSceneEnum.CREATEGAMEMENU:
                    self.next(CreateGameMenu, self._current_player)
                elif event.type == ChangeSceneEnum.HOSTJOINSCENE:
                    self._current_player = event.player
                    self.next(HostJoinScene, self._current_player)
                elif event.type == ChangeSceneEnum.HOSTMENUSCENE:
                    self.next(HostMenuScene, self._current_player)
                elif event.type == ChangeSceneEnum.JOINSCENE:
                    self.next(JoinScene, self._current_player)
                elif event.type == ChangeSceneEnum.LOADGAME:
                    self.next(LoadGame, self._current_player)
                elif event.type == ChangeSceneEnum.LOBBYSCENE:
                    self.next(LobbyScene, self._current_player)
                elif event.type == ChangeSceneEnum.GAMEBOARDSCENE:
                    EventQueue.unblock()
                    self.next(GameBoardScene, self._current_player)
