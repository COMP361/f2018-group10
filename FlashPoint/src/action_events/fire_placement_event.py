import random
from typing import Tuple

from src.action_events.advance_fire_event import AdvanceFireEvent
from src.constants.state_enums import GameKindEnum, SpaceStatusEnum
from src.models.game_state_model import GameStateModel
from src.action_events.action_event import ActionEvent


class FirePlacementEvent(ActionEvent):
    """Event for placing fires at the beginning of the game."""

    def __init__(self):
        super().__init__()
        self.board = GameStateModel.instance().game_board

    def execute(self):
        game = GameStateModel.instance()
        if game.rules == GameKindEnum.FAMILY:
            game.game_board.set_fires_family()

        else:
            num_haz = 0
            if game.rules == GameKindEnum.RECRUIT:
                num_haz = 3

            elif game.rules == GameKindEnum.VETERAN:
                num_haz = 4

            elif game.rules == GameKindEnum.HEROIC:
                num_haz = 5

            self.set_fires_heroic_veteran_recruit(num_haz)

    def set_fires_heroic_veteran_recruit(self, num_hazmat):
        advance_event = AdvanceFireEvent()
        # first fire
        tile = self._experienced_placement()

        advance_event.black_dice = tile[0]
        advance_event.red_dice = tile[1]

        advance_event.explosion(self.board.get_tile_at(tile[0], tile[1]))

        # second fire
        tile = [self._roll_red_dice(), self._roll_black_dice()]
        while self.board.get_tile_at(tile[0], tile[1]).space_status == SpaceStatusEnum.FIRE:
            tile = [self._roll_red_dice(), self._roll_black_dice()]

        self.board.get_tile_at(tile[0], tile[1]).space_status = SpaceStatusEnum.FIRE
        self.board.get_tile_at(tile[0], tile[1]).hot_spot()

        advance_event.black_dice = tile[0]
        advance_event.red_dice = tile[1]

        advance_event.explosion(self.board.get_tile_at(tile[0], tile[1]))

        # third fire
        zero = ((tile[0] + 3) % 8) + 1
        tile = [self._roll_red_dice(), zero]
        while self.board.get_tile_at(tile[0], tile[1]).space_status == SpaceStatusEnum.FIRE:
            tile = [ self._roll_red_dice(), zero]
        self.board.get_tile_at(tile[0], tile[1]).space_status = SpaceStatusEnum.FIRE
        self.board.get_tile_at(tile[0], tile[1]).hot_spot()

        advance_event.black_dice = tile[0]
        advance_event.red_dice = tile[1]

        advance_event.explosion(self.board.get_tile_at(tile[0], tile[1]))

        # optional 4th fire
        if num_hazmat == 5:
            tile = [self._roll_red_dice(), self._roll_black_dice()]
            while self.board.get_tile_at(tile[0], tile[1]).space_status == SpaceStatusEnum.FIRE:
                tile = [self._roll_red_dice(), self._roll_black_dice()]

            self.board.get_tile_at(tile[0], tile[1]).space_status = SpaceStatusEnum.FIRE
            self.board.get_tile_at(tile[0], tile[1]).hot_spot()

            advance_event.black_dice = tile[0]
            advance_event.red_dice = tile[1]

            advance_event.explosion(self.board.get_tile_at(tile[0], tile[1]))

        for i in range(num_hazmat):
            tile = [ self._roll_red_dice(), self._roll_black_dice()]
            while self.board.get_tile_at(tile[0], tile[1]).space_status == SpaceStatusEnum.FIRE:
                tile = [self._roll_red_dice(), self._roll_black_dice()]

            self.board.get_tile_at(tile[0], tile[1]).set_hazmat()

    def _experienced_placement(self) -> Tuple[int, int]:

        roll = self._roll_black_dice()
        if roll == 1:
            self.board.get_tile_at(3, 3).space_status = SpaceStatusEnum.FIRE
            self.board.get_tile_at(3, 3).hot_spot()
            return 3, 3

        elif roll == 2:

            self.board.get_tile_at(3, 4).space_status = SpaceStatusEnum.FIRE
            self.board.get_tile_at(3, 4).hot_spot()
            return 3, 4

        elif roll == 3:

            self.board.get_tile_at(3, 5).space_status = SpaceStatusEnum.FIRE
            self.board.get_tile_at(3, 5).hot_spot()
            return 3, 5

        elif roll == 4:

            self.board.get_tile_at(3, 6).space_status = SpaceStatusEnum.FIRE
            self.board.get_tile_at(3, 6).hot_spot()
            return 3, 6

        elif roll == 5:

            self.board.get_tile_at(4, 6).space_status = SpaceStatusEnum.FIRE
            self.board.get_tile_at(4, 6).hot_spot()
            return 4, 6

        elif roll == 6:

            self.board.get_tile_at(4, 5).space_status = SpaceStatusEnum.FIRE
            self.board.get_tile_at(4, 5).hot_spot()
            return 4, 5

        elif roll == 7:

            self.board.get_tile_at(4, 4).space_status = SpaceStatusEnum.FIRE
            self.board.get_tile_at(4, 4).hot_spot()
            return 4, 4

        elif roll == 8:

            self.board.get_tile_at(4, 3).space_status = SpaceStatusEnum.FIRE
            self.board.get_tile_at(4, 3).hot_spot()
            return 4, 3

    @staticmethod
    def _roll_black_dice():
        return random.randint(1, 8)

    @staticmethod
    def _roll_red_dice():
        return random.randint(1, 6)
