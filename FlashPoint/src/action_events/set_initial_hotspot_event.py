import logging
import random

from src.action_events.action_event import ActionEvent
from src.constants.state_enums import DifficultyLevelEnum
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_state_model import GameStateModel

logger = logging.getLogger("FlashPoint")


class SetInitialHotspotEvent(ActionEvent):
    """Event for placing Hot Spot markers at
        the beginning of the experienced game"""

    def __init__(self, seed: int = 0):
        super().__init__()
        if seed == 0:
            self.seed = random.randint(1, 6969)
        else:
            self.seed = seed

        self.game: GameStateModel = GameStateModel.instance()
        self.game_board: GameBoardModel = self.game.game_board
        self.num_hotspots_to_place = 0

    def _determine_num_to_place(self):
        # Determine the number of
        # hotspots that have to be placed.
        if self.game.difficulty_level != DifficultyLevelEnum.RECRUIT:
            self.num_hotspots_to_place = self.num_hotspots_to_place + 3

        num_players = len(self.game.players)
        if num_players == 3:
            self.num_hotspots_to_place = self.num_hotspots_to_place + 2
        elif num_players > 3:
            self.num_hotspots_to_place = self.num_hotspots_to_place + 3

    def execute(self, *args, **kwargs):
        # NOTE:
        # Event still has to be executed
        # even if 0 hotspots are to be placed
        # since the hotspot bank has to be set
        # at the end.

        # Pick random location: roll dice
        random.seed(self.seed)
        logger.info("Executing Set Initial Hot Spot Event")
        self._determine_num_to_place()
        logger.info("{h} hotspots have to be placed".format(h=self.num_hotspots_to_place))
        num_placed = 0
        while num_placed < self.num_hotspots_to_place:
            row = self.game.roll_red_dice()
            column = self.game.roll_black_dice()
            target_tile = self.game_board.get_tile_at(row, column)
            if target_tile.is_hotspot:
                continue

            target_tile.is_hotspot = True
            num_placed += 1

        # If the difficulty level is Heroic, put 12
        # hotspots in the bank that will be used later,
        # otherwise put 6 in the bank.
        if self.game.difficulty_level == DifficultyLevelEnum.HEROIC:
            self.game_board.hotspot_bank = 12
        else:
            self.game_board.hotspot_bank = 6
