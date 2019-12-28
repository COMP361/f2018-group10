import json
from typing import Dict

from src.action_events.action_event import ActionEvent
from src.constants.state_enums import GameBoardTypeEnum
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_state_model import GameStateModel


class RandomBoardSetupEvent(ActionEvent):

    def __init__(self, board_json: Dict):
        super().__init__()
        self._board_info = board_json

    def execute(self, *args, **kwargs):
        with open("media/random_inside_walls_doors.json", "w+") as f:
            json.dump(self._board_info, f)
        GameStateModel.instance().game_board = GameBoardModel(GameBoardTypeEnum.RANDOM, self._board_info)
