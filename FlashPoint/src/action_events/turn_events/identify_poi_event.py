import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import PlayerRoleEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.poi_model import POIModel

logger = logging.getLogger("FlashPoint")

class IdentifyPOIEvent(TurnEvent):
    """
    Event for Imaging Technician to identify
    a POI anywhere on the board.
    """

    def __init__(self, row: int, column: int):
        super().__init__()
        self.row = row
        self.column = column
        game: GameStateModel = GameStateModel.instance()
        self.current_player = game.players_turn

    def execute(self):
        logger.info("Executing Identify POI Event")
        self.game: GameStateModel = GameStateModel.instance()
        self.game_board = self.game.game_board
        tile_model = self.game_board.get_tile_at(self.row, self.column)
        for model in tile_model.associated_models:
            if isinstance(model, POIModel):
                self.game_board.flip_poi(model)
                break

        if self.current_player.role != PlayerRoleEnum.DOGE:
            self.current_player.ap = self.current_player.ap - 1
