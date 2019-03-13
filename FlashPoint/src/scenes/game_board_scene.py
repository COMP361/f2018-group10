import json
from datetime import datetime

import pygame

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
import src.constants.color as Color
from src.UIComponents.rect_button import RectButton
from src.UIComponents.text import Text
from src.sprites.notify_player_turn import NotifyPlayerTurn


class GameBoardScene(object):
    """
    Scene for displaying the main game view
    """
    def __init__(self, screen: pygame.display, current_player: PlayerModel):
        """
        :param screen : The display passed from main on which to draw the Scene.
        """
        self._save_games_file = "media/save_games.json"
        self.screen = screen
        self._game: GameStateModel = GameStateModel.instance()
        if Networking.get_instance().is_host:
            self._current_player = self._game.host
        else:
            self._current_player = [player for player in self._game.players if player == current_player][0]
        self._current_sprite = None

        self.quit_btn = RectButton(200, 250, 100, 50, Color.STANDARDBTN, 0,
                                   Text(pygame.font.SysFont('Arial', 20), "Quit", Color.BLACK))

        self.active_sprites = pygame.sprite.Group()   # Maybe add separate groups for different things later
        self.game_board_sprite = GameBoard(current_player)
        self.chat_box = ChatBox(self._current_player)
        self.menu = None
        self._init_sprites()
        self.tile_input_controller = TileInputController(self._current_player)
        self.chop_controller = ChopController(self._current_player)
        self.door_controller = DoorController(self._current_player)
        for poi in self._game.game_board.active_pois:
            poi_sprite = POISprite(poi)
            self.game_board_sprite.add(poi_sprite)

        if Networking.get_instance().is_host:
            GameStateModel.instance()._notify_player_index()

    def _init_sprites(self):
        for i, player in enumerate(self._game.players):
            self.active_sprites.add(PlayerState(0, 30 + 64*i, player.nickname, player.color,player))
        self._current_sprite = CurrentPlayerState(1130, 550, self._current_player.nickname,self._current_player.color,self._current_player)
        self.active_sprites.add(self._current_sprite)
        self.notify_turn_popup = NotifyPlayerTurn(self._current_player, self._current_sprite, self.active_sprites)
        self.active_sprites.add(self.notify_turn_popup)
        self.active_sprites.add(self.notify_turn_popup._init_not_your_turn())
        self.active_sprites.add(TimeBar(0, 0))
        self.ingame_states = InGameStates(250, 650, self._game.damage, self._game.victims_saved, self._game.victims_lost)
        self.active_sprites.add(self.ingame_states)
        self.menu_btn = self._init_menu_button()
        self.active_sprites.add(self.menu_btn)

    def _save(self):
        """Save the current game state to the hosts machine"""
        with open(self._save_games_file, mode='r+', encoding='utf-8') as myFile:
            temp = json.load(myFile)
            game_data = JSONSerializer.serialize(self._game)
            game_data["time"] = datetime.now().strftime("%d/%m/%y-%H:%M:%S")
            temp.append(game_data)

        with open(self._save_games_file, mode='w', encoding='utf-8') as myFile:
            json.dump(temp, myFile)

        self.menu.close()

    def _quit_btn_on_click(self):
        Networking.get_instance().disconnect()
        TileInputController.__del__()
        ChopController._instance = None
        DoorController._instance = None
        EventQueue.post(CustomEvent(ChangeSceneEnum.STARTSCENE))

    # Example of how to use the MenuClass YOU NEED TO MAKE ALL YOUR BUTTONS EXTEND INTERACTABLE!!!!!!!!!!!!!!!!!
    def _init_menu_button(self):
        btn = RectButton(0, 0, 30, 30, background=Color.GREEN, txt_obj=Text(pygame.font.SysFont('Arial', 23), ""))
        btn.on_click(self._click_action)
        btn.set_transparent_background(True)
        return btn

    def _click_action(self):
        menu = MenuWindow([self.active_sprites, self.game_board_sprite], 500, 500, (400, 150))

        save_btn = RectButton(200, 150, 100, 50, Color.STANDARDBTN, 0,
                              Text(pygame.font.SysFont('Agency FB', 20), "Save", Color.BLACK))

        quit_btn = RectButton(200, 250, 100, 50, Color.STANDARDBTN, 0,
                              Text(pygame.font.SysFont('Agency FB', 20), "Quit", Color.BLACK))

        back_btn = RectButton(50, 50, 50, 50, "media/GameHud/crosss.png", 0)

        # cross = pygame.image.load("media/GameHud/cross.png")

        back_btn.on_click(menu.close)
        quit_btn.on_click(self._quit_btn_on_click)
        save_btn.on_click(self._save)

        menu.add_component(back_btn)
        menu.add_component(save_btn)
        menu.add_component(quit_btn)

        self.quit_btn = quit_btn
        self.menu = menu

    def draw(self, screen: pygame.display):
        """Draw all currently active sprites."""
        self.game_board_sprite.draw(screen)
        self.chat_box.draw(screen)
        self.active_sprites.draw(screen)

        if self.menu and not self.menu.is_closed:
            self.menu.draw(screen)

    def update(self, event_queue: EventQueue):
        """Call the update() function of everything in this class."""
        self.active_sprites.update(event_queue)
        self.chat_box.update(event_queue)

        if not self.ignore_area():
            self.game_board_sprite.update(event_queue)
            self.tile_input_controller.update(event_queue)
            self.chop_controller.update(event_queue)
            self.door_controller.update(event_queue)

        if self.menu and not self.menu.is_closed:
            self.menu.update(event_queue)

        self.notify_turn_popup.update(event_queue)
        # self.choose_start_pos_controller.update(event_queue)

    def ignore_area(self):
        ignore = False
        mouse_pos = pygame.mouse.get_pos()

        ignore = ignore or (self.chat_box.box.x < mouse_pos[0] < self.chat_box.box.x + self.chat_box.box.width and
                            self.chat_box.box.y < mouse_pos[1] < self.chat_box.box.y + self.chat_box.box.height)

        for sprite in self.active_sprites:
            ignore = ignore or (sprite.rect.x < mouse_pos[0] < sprite.rect.x + sprite.rect.width and
                                sprite.rect.y < mouse_pos[1] < sprite.rect.y + sprite.rect.height)

        return ignore
