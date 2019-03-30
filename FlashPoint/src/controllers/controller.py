from abc import ABC, abstractmethod

from src.UIComponents.interactable import Interactable
from src.models.game_board.tile_model import TileModel
from src.models.game_units.player_model import PlayerModel
from src.sprites.tile_sprite import TileSprite


class Controller(ABC):
    """Abstract Base Class For controllers. All controllers must implement these methods.
        Also note that controllers should be singletons. Meaning they should have a class variable called _instance,
        should raise an exception if instantiated twice, and should have a class method called instance().
    """

    def __init__(self, current_player: PlayerModel):
        super().__init__()

        self._current_player = current_player

    @abstractmethod
    def process_input(self, tile_sprite: TileSprite):
        """
        Gets called from TileInputController. Should have the following steps:

        1.) run checks
        2.) If checks passed, tile_sprite.menu(s)_for_this_controller.enable()
            -Set the onclick of the menu to be send_event_and_close_menu
        3.) Else tile_sprite.menu(s)_for_this_controller.disable()


        """
        pass

    @abstractmethod
    def run_checks(self, tile_model: TileModel) -> bool:
        """
        Determine if this tile is valid for the operation this controller is responsible for.
        This should get called both when determining whether to display the menu, AND when determining whether
        to send the event. (ie called from process_input and from send_event_close_menu)

        Some common checks:
            - Is it the current player's turn (some moves don't require this, some do)
            - Does the player have enough AP?
            - Is the player in the correct spot for the action?
            - etc...
        """
        pass

    @abstractmethod
    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        """
        Create the event with all necessary parameters, send over the network. Be sure to close the menu by calling
        disable().
        """
        pass
