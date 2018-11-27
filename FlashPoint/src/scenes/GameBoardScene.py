import pygame

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
        self.active_sprites = pygame.sprite.Group()   # Maybe add separate groups for different things later
        self.game_board = GameBoard()
        self._init_sprites()

    def _init_sprites(self):
        self.active_sprites.add(GameBoard())
        self.active_sprites.add(PlayerState(0, 50, "Tim",Color.CYAN))
        self.active_sprites.add(PlayerState(0, 114, "Nuri",Color.GREEN))
        self.active_sprites.add(PlayerState(0, 178, "Francis",Color.WHITE))
        self.active_sprites.add(PlayerState(0, 242, "Haw", Color.YELLOW))
        self.active_sprites.add(PlayerState(0, 306, "Alek", Color.MAGENTA))
        self.active_sprites.add(CurrentPlayerState(1080, 500 , "Tim"))
        self.active_sprites.add(TimeBar(0,0))
        self.active_sprites.add(DamageState(399, 612))
        self.active_sprites.add(VictimSaved(626, 612))
        self.active_sprites.add(VictimDead(853, 612))

    def draw(self):
        """Draw all currently active sprites."""
        self.game_board.draw(self.screen)
        self.active_sprites.draw(self.screen)

    def update(self):
        """Call the update() function of everything in this class."""
        self.game_board.update()
        self.active_sprites.update()
