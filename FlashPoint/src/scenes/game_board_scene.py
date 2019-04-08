import itertools
import json
import os
from datetime import datetime
from typing import List

import pygame

from src.action_events.fire_placement_event import FirePlacementEvent
from src.action_events.set_initial_hotspot_event import SetInitialHotspotEvent
from src.action_events.set_initial_poi_experienced_event import SetInitialPOIExperiencedEvent
from src.constants.custom_event_enums import CustomEventEnum
from src.constants.state_enums import GameKindEnum, GameStateEnum, GameBoardTypeEnum
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_units.victim_model import VictimModel
from src.sprites.dodge_prompt import DodgePrompt
from src.sprites.hazmat_sprite import HazmatSprite
from src.sprites.victim_sprite import VictimSprite
from src.models.game_units.poi_model import POIModel
from src.observers.GameBoardObserver import GameBoardObserver
from src.observers.game_state_observer import GameStateObserver

from src.action_events.place_hazmat_event import PlaceHazmatEvent
from src.action_events.set_initial_poi_family_event import SetInitialPOIFamilyEvent
from src.controllers.chop_controller import ChopController
from src.controllers.door_controller import DoorController
from src.sprites.poi_sprite import POISprite
from src.controllers.tile_input_controller import TileInputController
from src.constants.change_scene_enum import ChangeSceneEnum
from src.core.custom_event import CustomEvent

from src.UIComponents.chat_box import ChatBox
from src.UIComponents.menu_window import MenuWindow
from src.core.event_queue import EventQueue
from src.core.networking import Networking
from src.core.serializer import JSONSerializer
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.sprites.game_board import GameBoard
from src.sprites.hud.player_state import PlayerState
from src.sprites.hud.current_player_state import CurrentPlayerState
from src.sprites.hud.time_bar import TimeBar
from src.sprites.hud.ingame_states import InGameStates
from src.sprites.player_sprite import PlayerSprite
import src.constants.color as Color
from src.UIComponents.rect_button import RectButton
from src.UIComponents.text import Text
from src.sprites.notify_player_turn import NotifyPlayerTurn


class GameBoardScene(GameBoardObserver, GameStateObserver):
    """
    Scene for displaying the main game view
    """

    def __init__(self, screen: pygame.display, current_player: PlayerModel):
        """
        :param screen : The display passed from main on which to draw the Scene.
        :param current_player: The player on this local machine.
        """

        self._screen = screen
        self._save_games_file = "media/saved_games.json"
        self._game: GameStateModel = GameStateModel.instance()
        self._game.game_board.add_observer(self)
        self._init_current_player(current_player)
        self._active_sprites = pygame.sprite.Group()  # Maybe add separate groups for different things later
        self._player_hud_sprites = pygame.sprite.Group()

        # Initialize UI elements
        self._init_ui_elements()

        # Initialize controllers
        self._init_controllers()

        # Send initialization events
        if self._game.board_type != GameBoardTypeEnum.LOADED:
            self._send_game_board_initialize()
        else:
            self._init_loaded_sprites()
        self._game._notify_player_index()

    def _init_ui_elements(self):
        """Initialize all things to be drawn on this screen."""
        self._menu = None
        self._dodge_prompt = DodgePrompt()
        self._game_board_sprite = GameBoard(self._current_player)
        self._menu_btn = self._init_menu_button()
        self._chat_box = ChatBox(self._current_player)

        # Now add everything to the sprite group that needs to be added.
        self._init_active_sprites()

    def _init_active_sprites(self):
        """Set all the initial Sprites and add them to the sprite Group."""

        for i, player in enumerate(self._game.players):
            self._player_hud_sprites.add(PlayerState(0, 30 + 64 * i, player.nickname, player.color, player))

        # Notify player turn stuff
        current_player_info_sprite = CurrentPlayerState(1130, 550, self._current_player.nickname,
                                                        self._current_player.color, self._current_player)
        self._active_sprites.add(current_player_info_sprite)
        notify_player_turn = NotifyPlayerTurn(self._current_player, current_player_info_sprite,
                                              self._active_sprites)
        self._active_sprites.add(notify_player_turn)
        self._active_sprites.add(notify_player_turn.init_not_your_turn())

        # HUD stuff
        self._active_sprites.add(TimeBar(0, 0))
        self._active_sprites.add(
            InGameStates(250, 650, self._game.damage, self._game.victims_saved, self._game.victims_lost))
        self._active_sprites.add(self._menu_btn)

    def _init_loaded_sprites(self):
        """Find all models that were loaded but don't have corresponding observers/sprites."""
        self.notify_active_poi(self._game.game_board.active_pois)
        for tile in self._game.game_board.tiles:
            for obj in tile.associated_models:
                if isinstance(obj, HazmatModel):
                    self._game_board_sprite.add(HazmatSprite(tile))

    def _init_controllers(self):
        """Instantiate all controllers."""
        ChopController(self._current_player)
        DoorController(self._current_player)
        TileInputController(self._current_player)

    def _init_current_player(self, current_player: PlayerModel):
        """Set reference of the current player to point to the one in the game state."""
        if Networking.get_instance().is_host:
            self._current_player = self._game.players[0]
        else:
            self._current_player = [player for player in self._game.players if player == current_player][0]

    def _send_game_board_initialize(self):
        """Send any game board initialization events."""
        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(FirePlacementEvent())

            if self._game.rules == GameKindEnum.EXPERIENCED:
                Networking.get_instance().send_to_all_client(SetInitialPOIExperiencedEvent())
                Networking.get_instance().send_to_all_client(PlaceHazmatEvent())
                Networking.get_instance().send_to_all_client(SetInitialHotspotEvent())
            else:
                Networking.get_instance().send_to_all_client(SetInitialPOIFamilyEvent())

        for player in self._game.players:
            player.set_initial_ap(self._game.rules)

        GameStateModel.instance().add_observer(self)

    def _save(self):
        """Save the current game state to the hosts machine"""
        if not os.path.exists(self._save_games_file):
            with open(self._save_games_file, mode="w+", encoding='utf-8') as myFile:
                myFile.write("[]")

        with open(self._save_games_file, mode='r+', encoding='utf-8') as myFile:
            temp = json.load(myFile)
            game_data = JSONSerializer.serialize(self._game)
            game_data["time"] = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
            temp.append(game_data)

        with open(self._save_games_file, mode='w', encoding='utf-8') as myFile:
            json.dump(temp, myFile)

        self._menu.close()

    @staticmethod
    def _quit_btn_on_click():
        Networking.get_instance().disconnect()
        TileInputController.__del__()
        ChopController._instance = None
        DoorController._instance = None
        EventQueue.post(CustomEvent(ChangeSceneEnum.STARTSCENE))

    # Example of how to use the MenuClass YOU NEED TO MAKE ALL YOUR BUTTONS EXTEND INTERACTABLE!
    def _init_menu_button(self):
        btn = RectButton(0, 0, 30, 30, background=Color.GREEN, txt_obj=Text(pygame.font.SysFont('Arial', 23), ""))
        btn.on_click(self._open_menu)
        btn.set_transparent_background(True)
        return btn

    def _open_menu(self):
        menu = MenuWindow([self._active_sprites, self._game_board_sprite], 500, 500, (400, 150))

        save_btn = RectButton(200, 150, 100, 50, Color.STANDARDBTN, 0,
                              Text(pygame.font.SysFont('Agency FB', 20), "Save", Color.BLACK))

        quit_btn = RectButton(200, 250, 100, 50, Color.STANDARDBTN, 0,
                              Text(pygame.font.SysFont('Agency FB', 20), "Quit", Color.BLACK))

        back_btn = RectButton(50, 50, 50, 50, "media/GameHud/crosss.png", 0)

        back_btn.on_click(menu.close)
        quit_btn.on_click(self._quit_btn_on_click)
        save_btn.on_click(self._save)

        menu.add_component(back_btn)
        menu.add_component(save_btn)
        menu.add_component(quit_btn)

        self._menu = menu

    def draw(self, screen: pygame.display):
        """Draw all currently active sprites."""
        self._game_board_sprite.draw(screen)
        self._chat_box.draw(screen)
        self._active_sprites.draw(screen)
        self._player_hud_sprites.draw(screen)
        self._dodge_prompt.draw(screen)
        if self._menu and not self._menu.is_closed:
            self._menu.draw(screen)

    def update(self, event_queue: EventQueue):
        """Call the update() function of everything in this class."""
        self._active_sprites.update(event_queue)
        self._chat_box.update(event_queue)
        self._player_hud_sprites.update(event_queue)
        self._dodge_prompt.update(event_queue)

        if not self.ignore_area():
            TileInputController.update(event_queue)
            self._game_board_sprite.update(event_queue)
            ChopController.instance().update(event_queue)
            DoorController.instance().update(event_queue)
        if self._menu and not self._menu.is_closed:
            self._menu.update(event_queue)

        for event in event_queue:
            if event.type == CustomEventEnum.DODGE_PROMPT:
                self._dodge_prompt.enabled = True

    def ignore_area(self):
        """A region in which all inputs are ignored."""
        ignore = False
        mouse_pos = pygame.mouse.get_pos()

        ignore = ignore or (self._chat_box.box.x < mouse_pos[0] < self._chat_box.box.x + self._chat_box.box.width and
                            self._chat_box.box.y < mouse_pos[1] < self._chat_box.box.y + self._chat_box.box.height)

        for sprite in itertools.chain(self._player_hud_sprites.sprites(), self._active_sprites.sprites()):
            ignore = ignore or (sprite.rect.x < mouse_pos[0] < sprite.rect.x + sprite.rect.width and
                                sprite.rect.y < mouse_pos[1] < sprite.rect.y + sprite.rect.height)

        return ignore

    def notify_active_poi(self, active_pois: List[POIModel]):
        # Removes are already handled by the sprites themselves, therefore only need to deal with adds.
        for sprite in self._game_board_sprite:
            if isinstance(sprite, POISprite) or isinstance(sprite, VictimSprite):
                sprite.kill()

        for poi in active_pois:
            if isinstance(poi, POIModel):
                self._game_board_sprite.add(POISprite(poi))
            elif isinstance(poi, VictimModel):
                victim_sprite = VictimSprite(poi.row, poi.column)
                poi.add_observer(victim_sprite)
                self._game_board_sprite.add(victim_sprite)

    def notify_player_index(self, player_index: int):
        pass

    def notify_game_state(self, game_state: GameStateEnum):
        pass

    def damage_changed(self, new_damage: int):
        pass

    def saved_victims(self, victims_saved: int):
        pass

    def dead_victims(self, victims_dead: int):
        pass

    def player_added(self, player: PlayerModel):
        pass

    def player_removed(self, player: PlayerModel):
        self.player_list_changed()
        # Remove player sprite from game board
        for sprite in GameBoard.instance().sprites():
            if isinstance(sprite, PlayerSprite):
                if sprite.associated_player is player:
                    GameBoard.instance().remove(sprite)
                    break

    def player_list_changed(self):
        # Refresh the list of players in HUD
        self._player_hud_sprites.empty()
        for i, player in enumerate(self._game.players):
            self._player_hud_sprites.add(PlayerState(0, 30 + 64 * i, player.nickname, player.color, player))
