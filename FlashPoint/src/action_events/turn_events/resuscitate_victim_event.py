import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import VictimStateEnum
from src.models.game_state_model import GameStateModel
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_units.victim_model import VictimModel

logger = logging.getLogger("FlashPoint")


class ResuscitateEvent(TurnEvent):

    def __init__(self, row: int, column: int):
        super().__init__()
        self.row = row
        self.column = column
        self.game: GameStateModel = GameStateModel.instance()
        self.game_board = self.game.game_board
        self.current_player = self.game.players_turn

    def execute(self):
        logger.info("Executing Resuscitate Event")
        tile_model = self.game_board.get_tile_at(self.row, self.column)
        for model in tile_model.associated_models:
            if isinstance(model, VictimModel):
                model.state = VictimStateEnum.TREATED

                logger.info(f"Victim at: ({tile_model.row}, {tile_model.column}) treated.")
                break

        self.current_player.ap = self.current_player.ap - 1
