from typing import Optional

import pygame
import json

import src.constants.CustomEvents as CustomEvents
from src.constants.state_enums import GameKindEnum
from src.core.serializer import JSONSerializer
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.UIComponents.file_importer import FileImporter
from src.UIComponents.input_box import InputBox
from src.scenes.game_board_scene import GameBoardScene
from src.scenes.host_join_scene import HostJoinScene
from src.scenes.host_menu_scene import HostMenuScene
from src.scenes.join_scene import JoinScene
from src.scenes.start_scene import StartScene
from src.scenes.create_game_menu import CreateGameMenu
from src.core.event_queue import EventQueue
from src.scenes.character_scene import CharacterScene
from src.scenes.lobby_scene import LobbyScene
from src.core.networking import Networking


class SceneManager(object):
    """Controller class for managing scenes, and their interactions. If an object needs to be passed from one scene
    to another, it must go through this class."""

    def __init__(self, screen: pygame.Surface):
        """
        Scene Manager. Initialize this before the game loop
        :param screen: should be the main display
       """
        self.profiles = "media/profiles.json"
        self.screen = screen
        self._active_scene = StartScene(self.screen)
        self._current_player = None
        self._game = None

        self._active_scene.buttonRegister.on_click(self.create_profile, self._active_scene.text_bar1)
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
            self._active_scene.buttonRegister.on_click(self.create_profile, self._active_scene.text_bar1)
            self.update_profiles()

        if isinstance(self._active_scene, HostJoinScene):
            self._active_scene.buttonJoin.on_click(self.next, JoinScene, self._current_player)
            self._active_scene.buttonHost.on_click(self.host, HostMenuScene, self._current_player)
            self._active_scene.buttonBack.on_click(self.next, StartScene)

        if isinstance(self._active_scene, JoinScene):
            self._active_scene.buttonBack.on_click(self.next, HostJoinScene, self._current_player)
            self._active_scene.buttonConnect.on_click(self.join, self._active_scene.text_bar_msg, LobbyScene)

        if isinstance(self._active_scene, HostMenuScene):
            self._active_scene.buttonBack.on_click(self.disconnect, HostJoinScene, self._current_player)
            self._active_scene.buttonNewGame.on_click(self.next, CreateGameMenu, self._current_player)

        if isinstance(self._active_scene, CreateGameMenu):
            self._active_scene.buttonBack.on_click(self.disconnect, HostJoinScene)
            self._active_scene.buttonExp.on_click(self.create_new_game, GameKindEnum.EXPERIENCED)
            self._active_scene.buttonFamily.on_click(self.create_new_game, GameKindEnum.FAMILY)

        if isinstance(self._active_scene, CharacterScene):
            self._active_scene.buttonBack.on_click(self.next, LobbyScene, self._current_player, self._game)
            self._active_scene.buttonConfirm.on_click(self.next, LobbyScene, self._current_player, self._game)

        if isinstance(self._active_scene, LobbyScene):
            if self._game.rules == GameKindEnum.EXPERIENCED:
                self._active_scene.buttonSelChar.on_click(self.next, CharacterScene, self._current_player)

            self._active_scene.buttonBack.on_click(self.disconnect, HostJoinScene, self._current_player)
            self._active_scene.buttonReady.on_click(self.next, GameBoardScene, self._game)

        if isinstance(self._active_scene, GameBoardScene):
            self._active_scene.quit_btn.on_click(self.disconnect, StartScene)

        FileImporter.play_audio("media/soundeffects/ButtonClick.wav", fade_ms=10)

    def draw(self):
        self._active_scene.draw(self.screen)

    def update(self, event_queue: EventQueue):
        self._active_scene.update(event_queue)
        for event in event_queue:
            self.handle_event(event)

    def handle_event(self, event):
        # join event
        if event.type == CustomEvents.JOIN:
            self.join(event.ip, LobbyScene, self._current_player, self._game)

    # ------------- GAME CREATE/LOAD STUFF ----------#

    def create_new_game(self, game_kind: GameKindEnum):
        """Instantiate a new family game and move to the lobby scene."""
        self._game = GameStateModel(self._current_player, game_kind)
        self.next(LobbyScene, self._current_player, self._game)

    # ------------- NETWORKING STUFF ----------------#

    def host(self, next_scene: Optional[callable] = None, *args):
        """
        Start the host process in Networking
        :param next_scene: next scene to be called after the process completes
        :param args: extra arguments for the next scene
        :return:
        """
        Networking.get_instance().create_host()

        if next_scene is not None:
            self.next(next_scene, *args)

    def join(self, ip_addr, next_scene: Optional[callable] = None, *args):
        """
        Start the join host process in Networking
        :param ip_addr: ip address to connect
        :param next_scene: next scene to be called after the process completes
        :param args: extra arguments for the next scene
        :return:
        """
        if isinstance(self._active_scene, JoinScene):
            is_join_scene = True
        else:
            is_join_scene = False

        try:
            Networking.get_instance().join_host(ip_addr)

            if next_scene is not None:
                self.next(next_scene, *args)
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
        """
        Start the disconnection process
        :param next_scene: next scene to be called after the process completes
        :param args: extra arguments for the next scene
        :return:
        """
        Networking.get_instance().disconnect()

        if next_scene is not None:
            self.next(next_scene, *args)

    # ------------ Stuff for profiles and start scene ------------ #

    def update_profiles(self):
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
