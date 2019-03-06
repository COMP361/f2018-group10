import json
from datetime import datetime

import pygame
from src.constants.change_scene_enum import ChangeSceneEnum
from src.core.custom_event import CustomEvent

from src.UIComponents.rect_label import RectLabel
from src.action_events.turn_events.choose_starting_position_event import ChooseStartingPositionEvent
from src.constants.state_enums import SpaceKindEnum
from src.core.networking import Networking

from src.UIComponents.chat_box import ChatBox
from src.UIComponents.menu_window import MenuWindow
from src.core.event_queue import EventQueue
from src.core.networking import Networking
from src.core.serializer import JSONSerializer
from src.models.game_state_model import GameStateModel
from src.models.game_units import player_model
from src.models.game_units.player_model import PlayerModel
from src.sprites.game_board import GameBoard
from src.sprites.hud.player_state import PlayerState
from src.sprites.hud.current_player_state import CurrentPlayerState
from src.sprites.hud.time_bar import TimeBar
from src.sprites.hud.ingame_states import InGameStates
import src.constants.color as Color
from src.UIComponents.rect_button import RectButton
from src.UIComponents.text import Text
from src.sprites.player_sprite import PlayerSprite


class GameBoardScene(object):
    """Scene for displaying the main game view"""

    def __init__(self, screen: pygame.display, current_player: PlayerModel):
        """:param screen : The display passed from main on which to draw the Scene."""

        self._save_games_file = "media/save_games.json"
        self.screen = screen
        self._game = GameStateModel.instance()
        self._current_player = current_player

        self.quit_btn = RectButton(200, 250, 100, 50, Color.STANDARDBTN, 0,
                                   Text(pygame.font.SysFont('Arial', 20), "Quit", Color.BLACK))

        self.active_sprites = pygame.sprite.Group()  # Maybe add separate groups for different things later
        self.game_board = GameBoard()
        self.chat_box = ChatBox(self._current_player)
        self.menu = None
        self._init_sprites()
        self.choose_start_pos_controller = ChooseStartingPositionController(self, current_player)

    def _init_sprites(self):
        for i, player in enumerate(self._game.players):
            self.active_sprites.add(PlayerState(0, 30 + 64 * i, player.nickname, player.color))

        self.active_sprites.add(
            CurrentPlayerState(1130, 550, self._current_player.nickname, self._current_player.color))
        self.active_sprites.add(TimeBar(0, 0))
        self.active_sprites.add(
            InGameStates(250, 650, self._game.damage, self._game.victims_saved, self._game.victims_lost))
        self.active_sprites.add(self._init_menu_button())

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
        EventQueue.post(CustomEvent(ChangeSceneEnum.STARTSCENE))

    # Example of how to use the MenuClass YOU NEED TO MAKE ALL YOUR BUTTONS EXTEND INTERACTABLE!!!!!!!!!!!!!!!!!
    def _init_menu_button(self):
        btn = RectButton(0, 0, 30, 30, background=Color.GREEN, txt_obj=Text(pygame.font.SysFont('Arial', 23), ""))
        btn.on_click(self._click_action)
        btn.set_transparent_background(True)
        return btn

    def _click_action(self):
        menu = MenuWindow([self.active_sprites, self.game_board], 500, 500, (400, 150))

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
        self.game_board.draw(screen)
        self.active_sprites.draw(screen)

        if self.menu and not self.menu.is_closed:
            self.menu.draw(screen)

        self.chat_box.draw(screen)

    def update(self, event_queue: EventQueue):
        """Call the update() function of everything in this class."""

        self.chat_box.update(event_queue)
        self.game_board.update(event_queue)
        self.game_board.update(event_queue)
        self.active_sprites.update(event_queue)
        if self.menu and not self.menu.is_closed:
            self.menu.update(event_queue)

        self.chat_box.update(event_queue)


""""TODO: Controller for starting position"""


class ChooseStartingPositionController(object):

    def __init__(self, game_scene: GameBoardScene,player: PlayerModel):
        self.scene = game_scene
        self.player = player
        """The offset of this rectlabel might be wickedly off, please someone has to check it"""
        self.choose_label = RectLabel(500, 0, 300, 75, Color.GREY, 0,
                                      Text(pygame.font.SysFont('Agency FB', 30), "Choose starting position",
                                           Color.ORANGE))
        self.scene.active_sprites.add(self.choose_label)
        self.board_state = GameStateModel.instance()
        self.game_board = self.board_state.game_board
        self.grid = GameBoard().grid

    def update(self):
        """Loop through the grid to find where the mouse is pointing"""
        for i in self.grid[0]:
            for j in self.grid:
                """1. get the tile at i,j index
                    2. see if that tile is outdoors or indoors
                    3. if indoors: hover is red, cannot click
                    4. if outdoors: hover is green, can click
                    5. if outdoors and clicked, check if there is no player object on that tile
                    6.a if there is a player sprite on that tile: hover red, cant click
                    6b. instantiate ChooseStartingPositionEvent(this curr tile)
                    6-1a. break out of this loop
                    6-1b. delete this controller, """
                curr_tile = self.grid[i][j]
                is_legal = True
                # get associated tile_model
                tile_model = self.game_board.get_tile_at(i, j)
                out = tile_model.get_space_kind()

                for models in tile_model.associated_models():
                    if isinstance(models, PlayerModel):

                        is_legal = False

                if is_legal and out is SpaceKindEnum.OUTDOOR:
                    if curr_tile.hover():
                        curr_tile.highlight(Color.GREEN)

                    if curr_tile.is_clicked():
                        ChooseStartingPositionEvent(tile_model)
                        self.scene.active_sprites.add(PlayerSprite(curr_tile))
                        self.choose_label.kill()
                        del self
                        # delete this controller in case of success scenario, the backend event has been instantiated
                        break

                else:
                    if curr_tile.hover():
                        curr_tile.highlight(Color.RED)

                """"if out is SpaceKindEnum.INDOOR:
                    if curr_tile.hover():
                        curr_tile.highlight(Color.RED)
                    

                elif out is SpaceKindEnum.OUTDOOR:
                    
                    # have to loop through tile_model to check if there is a player on that tile:
                    for models in tile_model.associated_models():
                        if isinstance(models, PlayerModel):
                            
                            
                    if curr_tile.hover():
                        curr_tile.highlight(Color.GREEN)
                    
                    if curr_tile.is_clicked():
                        """
