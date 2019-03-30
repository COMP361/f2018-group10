import random
import logging
from typing import Tuple

from src.action_events.end_turn_advance_fire import EndTurnAdvanceFireEvent
from src.constants.state_enums import GameKindEnum, SpaceStatusEnum, DifficultyLevelEnum
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.action_events.action_event import ActionEvent

logger = logging.getLogger("FlashPoint")


class FirePlacementEvent(ActionEvent):
    """Event for placing fires at the beginning of the game."""

    def __init__(self):
        super().__init__()
        self.game: GameStateModel = GameStateModel.instance()
        self.board: GameBoardModel = self.game.game_board

    def execute(self):
        print()
        logger.info("Executing FirePlacementEvent")
        if self.game.rules == GameKindEnum.FAMILY:
            self.board.set_fires_family()
        else:
            self._set_fires_heroic_veteran_recruit(self.game.difficulty_level)

    def _set_fires_heroic_veteran_recruit(self, difficulty_lvl: DifficultyLevelEnum):
        advance_event = EndTurnAdvanceFireEvent()
        # First explosion:
        # Roll the black dice to determine where the
        # first explosion will take place. Set the tile on fire, turn
        # hotspot to true and cause an explosion on that tile.
        logger.info("First explosion")
        tile_pos = self._first_explosion_dice_roll()
        tile = self.board.get_tile_at(tile_pos[0], tile_pos[1])
        self._perform_fire_hotspot_explosion(tile, advance_event)

        # Second explosion:
        # Roll both dice to determine the target space. Keep rolling
        # until you get a non-fire space. Set the tile on fire, turn
        # hotspot to true and cause an explosion on that tile.
        logger.info("\nSecond explosion")
        tile_pos = [self.game.roll_red_dice(), self.game.roll_black_dice()]
        while self.board.get_tile_at(tile_pos[0], tile_pos[1]).space_status == SpaceStatusEnum.FIRE:
            tile_pos = [self.game.roll_red_dice(), self.game.roll_black_dice()]

        tile = self.board.get_tile_at(tile_pos[0], tile_pos[1])
        self._perform_fire_hotspot_explosion(tile, advance_event)

        # Third explosion:
        # Flip over the black dice from the previous roll to get
        # the new column. Roll the red dice. Keep rolling until you
        # get a non-fire space. Set the tile on fire, turn
        # hotspot to true and cause an explosion on that tile.
        logger.info("\nThird explosion")
        column = self._determine_black_dice_opposite_face(tile_pos[1])
        tile_pos = [self.game.roll_red_dice(), column]
        while self.board.get_tile_at(tile_pos[0], tile_pos[1]).space_status == SpaceStatusEnum.FIRE:
            tile_pos = [self.game.roll_red_dice(), column]

        tile = self.board.get_tile_at(tile_pos[0], tile_pos[1])
        self._perform_fire_hotspot_explosion(tile, advance_event)

        # Conditional fourth explosion:
        # Only happens if playing at the Heroic level. Roll both
        # dice to determine target space. Keep rolling until you
        # get a non-fire space. Set the tile on fire, turn
        # hotspot to true and cause an explosion on that tile.
        if difficulty_lvl == DifficultyLevelEnum.HEROIC:
            logger.info("\nFourth explosion")
            tile_pos = [self.game.roll_red_dice(), self.game.roll_black_dice()]
            while self.board.get_tile_at(tile_pos[0], tile_pos[1]).space_status == SpaceStatusEnum.FIRE:
                tile_pos = [self.game.roll_red_dice(), self.game.roll_black_dice()]

            tile = self.board.get_tile_at(tile_pos[0], tile_pos[1])
            self._perform_fire_hotspot_explosion(tile, advance_event)

    def _determine_black_dice_opposite_face(self, prev_roll: int) -> int:
        """
        Gives the opposite face on the black dice
        for the number prev_roll. (Based on the Koplow d8 -
        https://boardgamegeek.com/article/27926069#27926069)

        :param prev_roll: Number that the black dice rolled previously.
        :return: Number opposite to the previous roll.
        """
        if prev_roll == 1:
            return 6
        elif prev_roll == 2:
            return 5
        elif prev_roll == 3:
            return 8
        elif prev_roll == 4:
            return 7
        elif prev_roll == 5:
            return 2
        elif prev_roll == 6:
            return 1
        elif prev_roll == 7:
            return 4
        elif prev_roll == 8:
            return 3

    def _perform_fire_hotspot_explosion(self, tile: TileModel, advance_event: EndTurnAdvanceFireEvent):
        """
        Set the tile on fire, turn hotspot to true and
        cause an explosion on that tile.

        :param tile: Target tile
        :param advance_event: Advance event to access explosion
        :return:
        """
        tile.space_status = SpaceStatusEnum.FIRE
        tile.is_hotspot = True
        advance_event.explosion(tile)

    def _first_explosion_dice_roll(self) -> Tuple[int, int]:
        """
        Rolling the black dice to determine the
        location of the first explosion.

        :return: Location of first explosion
        """
        roll = self.game.roll_black_dice()
        if roll == 1:
            return 3, 3

        elif roll == 2:
            return 3, 4

        elif roll == 3:
            return 3, 5

        elif roll == 4:
            return 3, 6

        elif roll == 5:
            return 4, 6

        elif roll == 6:
            return 4, 5

        elif roll == 7:
            return 4, 4

        elif roll == 8:
            return 4, 3
