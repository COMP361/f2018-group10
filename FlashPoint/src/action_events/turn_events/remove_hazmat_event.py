import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.models.game_state_model import GameStateModel
from src.models.game_units.hazmat_model import HazmatModel

logger = logging.getLogger("FlashPoint")

class RemoveHazmatEvent(TurnEvent):

    def __init__(self, row: int, column: int):
        super().__init__()
        self.row = row
        self.column = column
        game: GameStateModel = GameStateModel.instance()
        self.current_player = game.players_turn

    def execute(self):
        logger.info("Executing Remove Hazmat Event")
        self.game: GameStateModel = GameStateModel.instance()
        self.game_board = self.game.game_board
        tile_model = self.game_board.get_tile_at(self.row, self.column)
        for model in tile_model.associated_models:
            if isinstance(model, HazmatModel):
                tile_model.remove_associated_model(model)
                model.set_pos(-1, -1)
                logger.info(f"Hazmat at: ({tile_model.row}, {tile_model.column}) removed.")
                break

        self.current_player.ap = self.current_player.ap - 2
