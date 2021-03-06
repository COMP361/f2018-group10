import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_state_model import GameStateModel
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_units.player_model import PlayerModel

logger = logging.getLogger("FlashPoint")

class PickupHazmatEvent(TurnEvent):

    def __init__(self, hazmat_row: int, hazmat_column: int):
        super().__init__()
        game: GameStateModel = GameStateModel.instance()
        self.hazmat_tile = game.game_board.get_tile_at(hazmat_row, hazmat_column)
        for assoc_model in self.hazmat_tile.associated_models:
            if isinstance(assoc_model, HazmatModel):
                self.hazmat = assoc_model
                break

        self.player: PlayerModel = game.players_turn

    def execute(self):
        logger.info("Executing Pickup Hazmat Event")
        self.player.carrying_hazmat = self.hazmat
        self.hazmat_tile.remove_associated_model(self.hazmat)
