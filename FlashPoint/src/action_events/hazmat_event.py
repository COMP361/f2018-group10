from src.action_events.action_event import ActionEvent
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_units.poi_model import POIModel


class HazmatEvent(ActionEvent):

    def __init__(self, row: int, column: int):
        super().__init__()
        self.row = row
        self.column = column
        self.game_board = self.board = GameStateModel.instance().game_board
        self.current_player = GameStateModel.instance().players_turn

    def execute(self):


        self.current_player.ap -= 2

        tile_model: TileModel = self.game_board.get_tile_at(self.row, self.column)

        for model in tile_model.associated_models:
            if isinstance(model, HazmatModel):
                tile_model.associated_models.remove(model)



