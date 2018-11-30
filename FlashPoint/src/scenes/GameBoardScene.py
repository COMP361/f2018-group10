import pygame

from src.Windows.UIComponents.MenuWindow import MenuWindow
from src.Windows.UIComponents.RectButton import RectButton
from src.Windows.UIComponents.Text import Text
from src.Windows.ChatBox.ChatBox import ChatBox
from src.core.EventQueue import EventQueue
from src.game_elements.game_board.GameBoard import GameBoard
from src.game_state.PlayerState import PlayerState
from src.game_state.CurrentPlayerState import CurrentPlayerState
from src.game_state.TimeBar import TimeBar
from src.game_state.DamageState import DamageState
from src.game_state.VictimSaved import VictimSaved
from src.game_state.VictimDead import VictimDead


import src.constants.Color as Color


class GameBoardScene(object):
    """Scene for displaying the main game view"""
    def __init__(self, screen: pygame.display):
        """:param screen : The display passed from main on which to draw the Scene."""
        self.screen = screen
        self.quit_btn = None
        self.active_sprites = pygame.sprite.Group()   # Maybe add separate groups for different things later
        self.game_board = GameBoard()
        self.chat_box = ChatBox()
        self.menu = None
        self._init_sprites()

    def _init_sprites(self):
        self.active_sprites.add(PlayerState(0, 50, "Tim", Color.CYAN))
        self.active_sprites.add(PlayerState(0, 114, "Nuri", Color.GREEN))
        self.active_sprites.add(PlayerState(0, 178, "Francis", Color.WHITE))
        self.active_sprites.add(PlayerState(0, 242, "Haw", Color.YELLOW))
        self.active_sprites.add(PlayerState(0, 306, "Alek", Color.MAGENTA))
        self.active_sprites.add(CurrentPlayerState(1080, 500, "Tim"))
        self.active_sprites.add(TimeBar(0, 0))
        self.active_sprites.add(DamageState(399, 612))
        self.active_sprites.add(VictimSaved(626, 612))
        self.active_sprites.add(VictimDead(853, 612))
        self.active_sprites.add(self._init_menu_button())

    # Example of how to use the MenuClass YOU NEED TO MAKE ALL YOUR BUTTONS EXTEND INTERACTABLE!!!!!!!!!!!!!!!!!
    def _init_menu_button(self):
        btn = RectButton(0, 0, 100, 50, background=Color.GREEN, txt_obj=Text(pygame.font.SysFont('Arial', 23), "Menu"))
        btn.on_click(self._click_action)
        return btn

    def _click_action(self):
        menu = MenuWindow([self.active_sprites, self.game_board], 500, 500, (400, 150))
        back_btn = RectButton(0, 0, 70, 50, txt_obj=Text(pygame.font.SysFont('Arial', 23), "Back"))
        save_btn = RectButton(100, 150, 100, 50, txt_obj=Text(pygame.font.SysFont('Arial', 23), "Save"))
        quit_btn = RectButton(100, 250, 100, 50, txt_obj=Text(pygame.font.SysFont('Arial', 23), "Quit"))

        back_btn.on_click(menu.close)
        # save_btn.on_click()   # Nothing yet

        menu.add_component(back_btn)
        menu.add_component(save_btn)
        menu.add_component(quit_btn)

        # Used by scene manager to know when to go back to lobby.
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
        self.game_board.update(event_queue)
        self.active_sprites.update(event_queue)

        if self.menu and not self.menu.is_closed:
            self.menu.update(event_queue)

        self.chat_box.update(event_queue)

