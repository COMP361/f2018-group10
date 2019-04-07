import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_board.null_model import NullModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.hazmat_model import HazmatModel

logger = logging.getLogger("FlashPoint")

class DropHazmatEvent(TurnEvent):

    def __init__(self, hazmat_row: int, hazmat_column):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        self.hazmat_tile = game.game_board.get_tile_at(hazmat_row, hazmat_column)
        self.player = game.players_turn

    # TODO: Move this code to the controller.
    def check(self):
        """
        If the player is not carrying a
        hazmat, then they cannot drop it.

        :return: True if player is carrying a
                hazmat, False otherwise.
        """
        if isinstance(self.player.carrying_hazmat, HazmatModel):
            return True

        return False

    def execute(self):
        logger.info("Executing Drop Hazmat Event")
        self.hazmat_tile.add_associated_model(self.player.carrying_hazmat)
        self.player.carrying_hazmat = NullModel()
