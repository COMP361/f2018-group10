import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_board.null_model import NullModel
from src.models.game_state_model import GameStateModel

logger = logging.getLogger("FlashPoint")


class StopLeadingVictimEvent(TurnEvent):

    def __init__(self, victim_row: int, victim_column: int):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        self.victim_tile = game.game_board.get_tile_at(victim_row, victim_column)
        self.player = game.players_turn

    def execute(self):
        logger.info("Executing Stop Leading Victim Event")
        self.victim_tile.add_associated_model(self.player.leading_victim)
        self.player.leading_victim = NullModel()
