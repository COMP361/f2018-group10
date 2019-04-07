import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_board.null_model import NullModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.victim_model import VictimModel

logger = logging.getLogger("FlashPoint")


class DropVictimEvent(TurnEvent):

    def __init__(self, victim: VictimModel):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        self.victim_tile = game.game_board.get_tile_at(victim.row, victim.column)
        self.player = game.players_turn

    def check(self):
        """
        If the player is not carrying a
        victim, then they cannot drop it.

        :return: True if player is carrying a
                victim, False otherwise.
        """
        if isinstance(self.player.carrying_victim, VictimModel):
            return True

        return False

    def execute(self):
        logger.info("Executing Drop Victim Event")
        self.victim_tile.add_associated_model(self.player.carrying_victim)
        self.player.carrying_victim = NullModel()
