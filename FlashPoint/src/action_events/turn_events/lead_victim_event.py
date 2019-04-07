import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.victim_model import VictimModel

logger = logging.getLogger("FlashPoint")


class LeadVictimEvent(TurnEvent):

    def __init__(self, victim_row: int, victim_column: int):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        self.victim_tile = game.game_board.get_tile_at(victim_row, victim_column)
        for assoc_model in self.victim_tile.associated_models:
            if isinstance(assoc_model, VictimModel):
                self.victim = assoc_model
                break

        self.player: PlayerModel = game.players_turn

    # TODO: Move this check code to the controller
    def check(self) -> bool:
        """
        If the player is already leading
        a victim, they cannot lead another victim.

        :return: True if the player is not leading
                a victim, False otherwise.
        """
        if isinstance(self.player.leading_victim, VictimModel):
            return False

        return True

    def execute(self):
        logger.info("Executing Lead Victim Event")
        self.player.leading_victim = self.victim
        self.victim_tile.remove_associated_model(self.victim)