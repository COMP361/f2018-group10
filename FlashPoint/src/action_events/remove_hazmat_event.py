import logging

from src.action_events.action_event import ActionEvent
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.hazmat_model import HazmatModel

logger = logging.getLogger("FlashPoint")


class RemoveHazmatEvent(ActionEvent):

    def __init__(self, row: int, column: int):
        super().__init__()
        self.row = row
        self.column = column
        self.game_board = self.board = GameStateModel.instance().game_board
        self.current_player = GameStateModel.instance().players_turn

    def execute(self):
        print()
        logger.info("Executing HazmatEvent")
        self.current_player.ap -= 2

        tile_model: TileModel = self.game_board.get_tile_at(self.row, self.column)

        for model in tile_model.associated_models:
            if isinstance(model, HazmatModel):
                tile_model.associated_models.remove(model)
                logger.info(f"Hazmat at: {tile_model.row}, {tile_model.column} removed.")



