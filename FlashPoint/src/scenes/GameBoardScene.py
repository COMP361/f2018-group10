import pygame

from src.Windows.ChatBox.ChatBox import ChatBox
from src.core.EventQueue import EventQueue
from src.game_elements.game_board.GameBoard import GameBoard


class GameBoardScene(object):
    """Scene for displaying the main game view"""
    def __init__(self, screen: pygame.display):
        """:param screen : The display passed from main on which to draw the Scene."""
        self.screen = screen
        self.active_sprites = pygame.sprite.Group()   # Maybe add separate groups for different things later
        self.game_board = GameBoard()
        self.chat_box = ChatBox()

    def draw(self, screen: pygame.display):
        """Draw all currently active sprites."""
        self.game_board.draw(screen)
        self.active_sprites.draw(screen)
        self.chat_box.draw(screen)

    def update(self, event_queue: EventQueue):
        """Call the update() function of everything in this class."""
        self.game_board.update(event_queue)
        self.active_sprites.update(event_queue)
        self.chat_box.update(event_queue)
