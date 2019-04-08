import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_state_model import GameStateModel
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.victim_model import VictimModel

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

    # TODO: Move this check code to the controller
    def check(self) -> bool:
        """
        If the player is already carrying
        another victim or a hazmat, then
        they cannot pick up another hazmat.

        :return: True if the player is carrying
                nothing, False otherwise.
        """
        if isinstance(self.player.carrying_victim, VictimModel) or isinstance(self.player.carrying_hazmat, HazmatModel):
            return False

        return True

    def execute(self):
        logger.info("Executing Pickup Hazmat Event")
        self.player.carrying_hazmat = self.hazmat
        self.hazmat_tile.remove_associated_model(self.hazmat)
