import json
from datetime import datetime

import pygame

from src.UIComponents.chat_box import ChatBox
from src.UIComponents.menu_window import MenuWindow
from src.core.event_queue import EventQueue
from src.core.serializer import JSONSerializer
from src.models.game_state_model import GameStateModel
from src.sprites.game_board import GameBoard
from src.sprites.hud.player_state import PlayerState
from src.sprites.hud.current_player_state import CurrentPlayerState
from src.sprites.hud.time_bar import TimeBar
from src.sprites.hud.ingame_states import InGameStates
import src.constants.color as Color
from src.UIComponents.rect_button import RectButton
from src.UIComponents.text import Text


class GameBoardScene(object):
    """Scene for displaying the main game view"""
    def __init__(self, screen: pygame.display, game: GameStateModel):
        """:param screen : The display passed from main on which to draw the Scene."""
        self._save_games_file = "media/save_games.json"
        self.screen = screen
        self._game = game

        self.quit_btn = RectButton(200, 250, 100, 50, Color.STANDARDBTN, 0,
                                   Text(pygame.font.SysFont('Arial', 20), "Quit", Color.BLACK))
        self.active_sprites = pygame.sprite.Group()   # Maybe add separate groups for different things later
        self.game_board = GameBoard()
        self.chat_box = ChatBox()
        self.menu = None
        self._init_sprites()

    def _init_sprites(self):
        self.active_sprites.add(PlayerState(0, 30, "Tim", Color.CYAN))
        self.active_sprites.add(PlayerState(0, 94, "Nuri", Color.GREEN))
        self.active_sprites.add(PlayerState(0, 158, "Francis", Color.WHITE))
        self.active_sprites.add(PlayerState(0, 222, "Haw", Color.YELLOW))
        self.active_sprites.add(PlayerState(0, 286, "Alek", Color.MAGENTA))
        self.active_sprites.add(CurrentPlayerState(1130, 550, "Tim"))
        self.active_sprites.add(TimeBar(0, 0))
        self.active_sprites.add(InGameStates(250, 650, 5, 5, 5))
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

    # Example of how to use the MenuClass YOU NEED TO MAKE ALL YOUR BUTTONS EXTEND INTERACTABLE!!!!!!!!!!!!!!!!!
    def _init_menu_button(self):
        btn = RectButton(0, 0, 30, 30, background=Color.GREEN, txt_obj=Text(pygame.font.SysFont('Arial', 23), ""))
        btn.on_click(self._click_action)
        btn.set_transparent_background(True)
        return btn

    def _click_action(self):
        menu = MenuWindow([self.active_sprites, self.game_board], 500, 500, (400, 150))
        back_btn = RectButton(10, 10, 70, 50, Color.STANDARDBTN, 0,
                              Text(pygame.font.SysFont('Arial', 20), "Back", Color.BLACK))
        save_btn = RectButton(200, 150, 100, 50, Color.STANDARDBTN, 0,
                              Text(pygame.font.SysFont('Arial', 20), "Save", Color.BLACK))

        back_btn.on_click(menu.close)

        save_btn.on_click(self._save)

        menu.add_component(back_btn)
        menu.add_component(save_btn)
        menu.add_component(self.quit_btn)

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
        self.game_board.update(event_queue)
        self.game_board.update(event_queue)
        self.active_sprites.update(event_queue)
        if self.menu and not self.menu.is_closed:
            self.menu.update(event_queue)

        self.chat_box.update(event_queue)
