import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_board.null_model import NullModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.victim_model import VictimModel

logger = logging.getLogger("FlashPoint")

class StopLeadingVictimEvent(TurnEvent):

    def __init__(self, victim_row: int, victim_column: int):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        self.victim_tile = game.game_board.get_tile_at(victim_row, victim_column)
        self.player = game.players_turn

    # TODO: Move this code to the controller.
    def check(self):
        """
        If the player is not leading a
        victim, then they cannot stop leading it.

        :return: True if player is leading a
                victim, False otherwise.
        """
        if isinstance(self.player.leading_victim, VictimModel):
            return True

        return False

    def execute(self):
        logger.info("Executing Stop Leading Victim Event")
        self.victim_tile.add_associated_model(self.player.leading_victim)
        self.player.leading_victim = NullModel()